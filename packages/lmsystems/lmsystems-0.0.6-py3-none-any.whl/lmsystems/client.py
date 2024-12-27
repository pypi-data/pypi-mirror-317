import httpx
from typing import Optional, Any, AsyncIterator, Union, Iterator
import jwt
from langgraph_sdk import get_client, get_sync_client
from .exceptions import AuthenticationError, GraphError, APIError
from .config import Config

class LmsystemsClient:
    """
    Async client for the Lmsystems API that wraps LangGraph functionality.

    Attributes:
        graph_name: Name of the purchased graph
        client: Underlying LangGraph client instance
    """

    def __init__(
        self,
        graph_name: str,
        api_key: str,
        base_url: str = Config.DEFAULT_BASE_URL,
    ) -> None:
        """
        Initialize the Lmsystems client.

        Args:
            graph_name: The name of the purchased graph
            api_key: The Lmsystems API key
            base_url: Base URL for the Lmsystems API
        """
        self.graph_name = graph_name
        self.api_key = api_key

        # Validate and set base URL
        if not base_url:
            base_url = "https://api.lmsystems.ai"
        if not base_url.startswith(("http://", "https://")):
            base_url = f"https://{base_url}"
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present

        self.client = None
        self.default_assistant_id = None

    @classmethod
    async def create(
        cls,
        graph_name: str,
        api_key: str,
        base_url: str = Config.DEFAULT_BASE_URL,
    ) -> "LmsystemsClient":
        """Async factory method to create and initialize the client."""
        client = cls(graph_name, api_key, base_url)
        await client.setup()
        return client

    async def setup(self) -> None:
        """Initialize the client asynchronously."""
        try:
            # Store graph info for later use of configurables
            self.graph_info = await self._get_graph_info()

            # Store default assistant_id and use lgraph_api_key directly
            self.default_assistant_id = self.graph_info.get('assistant_id')

            self.client = get_client(
                url=self.graph_info['graph_url'],
                api_key=self.graph_info['lgraph_api_key']
            )
        except Exception as e:
            raise APIError(f"Failed to initialize client: {str(e)}")

    async def _get_graph_info(self) -> dict:
        """Authenticate and retrieve graph connection details."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/get_graph_info",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={"graph_name": self.graph_name}
                )

                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                elif response.status_code == 403:
                    raise GraphError(f"Graph '{self.graph_name}' has not been purchased")
                elif response.status_code == 404:
                    raise GraphError(f"Graph '{self.graph_name}' not found")
                elif response.status_code != 200:
                    raise APIError(f"Backend API error: {response.text}")

                return response.json()
        except httpx.RequestError as e:
            raise APIError(f"Failed to communicate with server: {str(e)}")

    def _extract_api_key(self, access_token: str) -> str:
        """Extract LangGraph API key from JWT token."""
        try:
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            lgraph_api_key = decoded.get("lgraph_api_key")
            if not lgraph_api_key:
                raise AuthenticationError("LangGraph API key not found in token")
            return lgraph_api_key
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid access token: {str(e)}")

    # Helper method to handle thread ID format
    def _get_thread_id(self, thread: dict) -> str:
        """Extract thread ID from response, handling both formats."""
        if "thread_id" in thread:
            return thread["thread_id"]
        elif "id" in thread:
            return thread["id"]
        raise APIError("Invalid thread response format")

    # Delegate methods with improved error handling
    async def create_thread(self, **kwargs) -> dict:
        """Create a new thread with error handling."""
        try:
            return await self.client.threads.create(**kwargs)
        except Exception as e:
            raise APIError(f"Failed to create thread: {str(e)}")

    async def create_run(self, thread: dict, *, assistant_id: Optional[str] = None, **kwargs) -> dict:
        """Create a run with proper thread ID handling."""
        try:
            thread_id = self._get_thread_id(thread)

            # Use default assistant_id if none provided
            if assistant_id is None:
                if self.default_assistant_id is None:
                    raise APIError("No assistant_id provided and no default available")
                assistant_id = self.default_assistant_id

            # Get stored configurables from graph info
            stored_config = self.graph_info.get('configurables', {})

            # Get user-provided config from kwargs
            user_config = kwargs.pop('config', {})

            # Merge configs, with user-provided values taking precedence
            merged_config = stored_config.copy()
            if user_config:
                if 'configurable' in user_config and 'configurable' in stored_config:
                    merged_config['configurable'].update(user_config['configurable'])
                else:
                    merged_config.update(user_config)

            # Add merged config back to kwargs
            kwargs['config'] = merged_config

            return await self.client.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                **kwargs
            )
        except Exception as e:
            raise APIError(f"Failed to create run: {str(e)}")

    async def stream_run(self, thread: dict, run: dict, **kwargs) -> AsyncIterator:
        """Stream existing run results with error handling."""
        try:
            thread_id = self._get_thread_id(thread)
            run_id = run.get("run_id") or run.get("id")
            if not run_id:
                raise APIError("Invalid run response format")

            async for chunk in self.client.runs.join_stream(
                thread_id=thread_id,
                run_id=run_id,
                **kwargs
            ):
                yield chunk
        except Exception as e:
            raise APIError(f"Failed to stream run: {str(e)}")

    @property
    def assistants(self):
        """Access the assistants API."""
        return self.client.assistants

    @property
    def threads(self):
        """Access the threads API."""
        return self.client.threads

    @property
    def runs(self):
        """Access the runs API."""
        return self.client.runs

    @property
    def crons(self):
        """Access the crons API."""
        return self.client.crons

    @property
    def store(self):
        """Access the store API."""
        return self.client.store


class SyncLmsystemsClient:
    """
    Synchronous client for the Lmsystems API that wraps LangGraph functionality.

    This provides the same interface as LmsystemsClient but in a synchronous form.
    """

    def __init__(
        self,
        graph_name: str,
        api_key: str,
        base_url: str = Config.DEFAULT_BASE_URL,
        stream_mode: bool = True
    ) -> None:
        """
        Initialize the synchronous Lmsystems client.

        Args:
            graph_name: The name of the purchased graph
            api_key: The Lmsystems API key
            base_url: Base URL for the Lmsystems API (defaults to https://api.lmsystems.ai)
            stream_mode: Stream mode preference
        """
        self.graph_name = graph_name
        self.api_key = api_key

        # Validate and set base URL
        if not base_url:
            base_url = "https://api.lmsystems.ai"
        if not base_url.startswith(("http://", "https://")):
            base_url = f"https://{base_url}"
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present

        self.stream_mode = stream_mode

        # Synchronous initialization
        self.graph_info = self._get_graph_info()
        self.default_assistant_id = self.graph_info.get('assistant_id')
        self.client = get_sync_client(
            url=self.graph_info['graph_url'],
            api_key=self.graph_info['lgraph_api_key']
        )

    def _get_graph_info(self) -> dict:
        """Authenticate and retrieve graph connection details."""
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/api/get_graph_info",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={"graph_name": self.graph_name}
            )

            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 403:
                raise GraphError(f"Graph '{self.graph_name}' has not been purchased")
            elif response.status_code == 404:
                raise GraphError(f"Graph '{self.graph_name}' not found")
            elif response.status_code != 200:
                raise APIError(f"Backend API error: {response.text}")

            return response.json()

    def _extract_api_key(self, access_token: str) -> str:
        """Extract LangGraph API key from JWT token."""
        try:
            decoded = jwt.decode(access_token, options={"verify_signature": False})
            if 'lgraph_api_key' not in decoded:
                raise AuthenticationError("Invalid token format")
            return decoded['lgraph_api_key']
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid access token: {str(e)}")

    @property
    def assistants(self):
        """Access the assistants API."""
        return self.client.assistants

    @property
    def threads(self):
        """Access the threads API."""
        return self.client.threads

    @property
    def runs(self):
        """Access the runs API."""
        return self.client.runs

    @property
    def crons(self):
        """Access the crons API."""
        return self.client.crons

    @property
    def store(self):
        """Access the store API."""
        return self.client.store

    def create_run(self, thread: dict, *, assistant_id: Optional[str] = None, **kwargs) -> dict:
        """Create a run with proper thread ID handling."""
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            if not thread_id:
                raise APIError("Invalid thread response format")

            # Use default assistant_id if none provided
            if assistant_id is None:
                if self.default_assistant_id is None:
                    raise APIError("No assistant_id provided and no default available")
                assistant_id = self.default_assistant_id

            # Get stored configurables from graph info
            stored_config = self.graph_info.get('configurables', {})

            # Get user-provided config from kwargs
            user_config = kwargs.pop('config', {})

            # Merge configs, with user-provided values taking precedence
            merged_config = stored_config.copy()
            if user_config:
                if 'configurable' in user_config and 'configurable' in stored_config:
                    merged_config['configurable'].update(user_config['configurable'])
                else:
                    merged_config.update(user_config)

            # Add merged config back to kwargs
            kwargs['config'] = merged_config

            return self.client.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                **kwargs
            )
        except Exception as e:
            raise APIError(f"Failed to create run: {str(e)}")

    def join_run(self, thread: dict, run: dict, **kwargs) -> Union[dict, Iterator]:
        """Join a run and wait for completion with error handling."""
        try:
            thread_id = thread.get("thread_id") or thread.get("id")
            if not thread_id:
                raise APIError("Invalid thread response format")

            run_id = run.get("run_id") or run.get("id")
            if not run_id:
                raise APIError("Invalid run response format")

            if self.stream_mode:
                # Use join_stream for streaming mode
                return self.client.runs.join_stream(
                    thread_id=thread_id,
                    run_id=run_id,
                    **kwargs
                )
            else:
                # Use join for non-streaming mode
                return self.client.runs.join(
                    thread_id=thread_id,
                    run_id=run_id,
                    **kwargs
                )
        except Exception as e:
            raise APIError(f"Failed to join run: {str(e)}")
