import os
from langfuse.callback import CallbackHandler as LangfuseCallbackHandler
from langfuse import Langfuse

class TracingManager:
    def __init__(self, config):
        self.config = config
        self.handlers = []
        self.initialize_tracing()

    def initialize_tracing(self):
        tracing_enabled = self.config.get('tracing', False)
        providers = self.config.get('tracing_providers', ['langsmith'])

        if not tracing_enabled:
            return

        if 'langsmith' in providers:
            self._setup_langsmith()

        if 'langfuse' in providers:
            handler = self._setup_langfuse()
            if handler:
                self.handlers.append(handler)

    def _setup_langsmith(self):
        api_key = os.getenv("LANGCHAIN_API_KEY") or os.getenv("LANGSMITH_API_KEY")
        if api_key:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"

    def _setup_langfuse(self):
        required_vars = ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_HOST"]
        if not all(os.getenv(var) for var in required_vars):
            print("Warning: Missing Langfuse environment variables")
            return None
            
        Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST")
        )
        return LangfuseCallbackHandler()

    def get_callbacks(self):
        return self.handlers if self.handlers else None
