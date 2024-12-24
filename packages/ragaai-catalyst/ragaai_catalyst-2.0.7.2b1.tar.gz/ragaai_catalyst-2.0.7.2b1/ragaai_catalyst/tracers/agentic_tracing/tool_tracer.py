import functools
import uuid
from datetime import datetime
import psutil
from typing import Optional, Any, Dict, List
from .unique_decorator import mydecorator
import contextvars
import asyncio

class ToolTracerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_tool_name = contextvars.ContextVar("tool_name", default=None)
        self.current_tool_id = contextvars.ContextVar("tool_id", default=None)
        self.component_network_calls = {}
        self._trace_sync_tool_execution = mydecorator(self._trace_sync_tool_execution)
        self._trace_tool_execution = mydecorator(self._trace_tool_execution)


    def trace_tool(self, name: str, tool_type: str = "generic", version: str = "1.0.0"):
        def decorator(func):
            # Check if the function is async
            is_async = asyncio.iscoroutinefunction(func)

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await self._trace_tool_execution(
                    func, name, tool_type, version, *args, **kwargs
                )

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                return self._trace_sync_tool_execution(
                    func, name, tool_type, version, *args, **kwargs
                )

            return async_wrapper if is_async else sync_wrapper

        return decorator

    def _trace_sync_tool_execution(self, func, name, tool_type, version, *args, **kwargs):
        """Synchronous version of tool tracing"""
        if not self.is_active:
            return func(*args, **kwargs)

        start_time = datetime.now().astimezone()
        start_memory = psutil.Process().memory_info().rss
        component_id = str(uuid.uuid4())
        hash_id = self._trace_sync_tool_execution.hash_id

        # Start tracking network calls for this component
        self.start_component(component_id)

        try:
            # Execute the tool
            result = func(*args, **kwargs)

            # Calculate resource usage
            end_time = datetime.now().astimezone()
            end_memory = psutil.Process().memory_info().rss
            memory_used = max(0, end_memory - start_memory)

            # End tracking network calls for this component
            self.end_component(component_id)

            # Create tool component
            tool_component = self.create_tool_component(
                component_id=component_id,
                hash_id=hash_id,
                name=name,
                tool_type=tool_type,
                version=version,
                memory_used=memory_used,
                start_time=start_time,
                end_time=end_time,
                input_data=self._sanitize_input(args, kwargs),
                output_data=self._sanitize_output(result)
            )

            self.add_component(tool_component)
            return result

        except Exception as e:
            error_component = {
                "code": 500,
                "type": type(e).__name__,
                "message": str(e),
                "details": {}
            }
            
            # End tracking network calls for this component
            self.end_component(component_id)
            
            end_time = datetime.now().astimezone()
            
            tool_component = self.create_tool_component(
                component_id=component_id,
                hash_id=hash_id,
                name=name,
                tool_type=tool_type,
                version=version,
                memory_used=0,
                start_time=start_time,
                end_time=end_time,
                input_data=self._sanitize_input(args, kwargs),
                output_data=None,
                error=error_component
            )

            self.add_component(tool_component)
            raise

    async def _trace_tool_execution(self, func, name, tool_type, version, *args, **kwargs):
        """Asynchronous version of tool tracing"""
        if not self.is_active:
            return await func(*args, **kwargs)

        start_time = datetime.now().astimezone()
        start_memory = psutil.Process().memory_info().rss
        component_id = str(uuid.uuid4())
        hash_id = self._trace_tool_execution.hash_id

        try:
            # Execute the tool
            result = await func(*args, **kwargs)

            # Calculate resource usage
            end_time = datetime.now().astimezone()
            end_memory = psutil.Process().memory_info().rss
            memory_used = max(0, end_memory - start_memory)

            # Create tool component
            tool_component = self.create_tool_component(
                component_id=component_id,
                hash_id=hash_id,
                name=name,
                tool_type=tool_type,
                version=version,
                start_time=start_time,
                end_time=end_time,
                memory_used=memory_used,
                input_data=self._sanitize_input(args, kwargs),
                output_data=self._sanitize_output(result)
            )

            self.add_component(tool_component)
            return result

        except Exception as e:
            error_component = {
                "code": 500,
                "type": type(e).__name__,
                "message": str(e),
                "details": {}
            }
            
            end_time = datetime.now().astimezone()
            
            tool_component = self.create_tool_component(
                component_id=component_id,
                hash_id=hash_id,
                name=name,
                tool_type=tool_type,
                version=version,
                start_time=start_time,
                end_time=end_time,
                memory_used=0,
                input_data=self._sanitize_input(args, kwargs),
                output_data=None,
                error=error_component
            )

            self.add_component(tool_component)
            raise

    def create_tool_component(self, **kwargs):
        """Create a tool component according to the data structure"""
        start_time = kwargs["start_time"]
        component = {
            "id": kwargs["component_id"],
            "hash_id": kwargs["hash_id"],
            "source_hash_id": None,
            "type": "tool",
            "name": kwargs["name"],
            "start_time": start_time.isoformat(),
            "end_time": kwargs["end_time"].isoformat(),
            "error": kwargs.get("error"),
            "parent_id": self.current_agent_id.get(),
            "info": {
                "tool_type": kwargs["tool_type"],
                "version": kwargs["version"],
                "memory_used": kwargs["memory_used"]
            },
            "data": {
                "input": kwargs["input_data"],
                "output": kwargs["output_data"],
                "memory_used": kwargs["memory_used"]
            },
            "network_calls": self.component_network_calls.get(kwargs["component_id"], []),
            "interactions": [{
                "id": f"int_{uuid.uuid4()}",
                "interaction_type": "input",
                "timestamp": start_time.isoformat(),
                "content": kwargs["input_data"]
            }, {
                "id": f"int_{uuid.uuid4()}",
                "interaction_type": "output",
                "timestamp": kwargs["end_time"].isoformat(),
                "content": kwargs["output_data"]
            }]
        }

        return component

    def start_component(self, component_id):
        self.component_network_calls[component_id] = []

    def end_component(self, component_id):
        pass

    def _sanitize_input(self, args: tuple, kwargs: dict) -> Dict:
        """Sanitize and format input data"""
        return {
            "args": [str(arg) if not isinstance(arg, (int, float, bool, str, list, dict)) else arg for arg in args],
            "kwargs": {
                k: str(v) if not isinstance(v, (int, float, bool, str, list, dict)) else v 
                for k, v in kwargs.items()
            }
        }

    def _sanitize_output(self, output: Any) -> Any:
        """Sanitize and format output data"""
        if isinstance(output, (int, float, bool, str, list, dict)):
            return output
        return str(output)