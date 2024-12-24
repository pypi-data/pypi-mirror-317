import contextvars
from typing import Optional, Dict
import json
from datetime import datetime
import uuid
import os
from pathlib import Path

from .base import BaseTracer
from .llm_tracer import LLMTracerMixin
from .tool_tracer import ToolTracerMixin
from .agent_tracer import AgentTracerMixin
from .network_tracer import NetworkTracer

from .data_structure import (
    Trace, Metadata, SystemInfo, OSInfo, EnvironmentInfo,
    Resources, CPUResource, MemoryResource, DiskResource, NetworkResource,
    ResourceInfo, MemoryInfo, DiskInfo, NetworkInfo,
    Component, LLMComponent, AgentComponent, ToolComponent,
    NetworkCall, Interaction, Error
)


from ...ragaai_catalyst import RagaAICatalyst
from ..upload_traces import UploadTraces

class AgenticTracing(BaseTracer, LLMTracerMixin, ToolTracerMixin, AgentTracerMixin):
    def __init__(self, user_detail, auto_instrument_llm: bool = True):
        # Initialize all parent classes
        LLMTracerMixin.__init__(self)
        ToolTracerMixin.__init__(self)
        AgentTracerMixin.__init__(self)
        
        self.project_name = user_detail["project_name"]
        self.project_id = user_detail["project_id"]
        self.dataset_name = user_detail["dataset_name"]
        self.trace_user_detail = user_detail["trace_user_detail"]
        self.base_url = f"{RagaAICatalyst.BASE_URL}"
        self.timeout = 10

        BaseTracer.__init__(self, user_detail)
        
        self.auto_instrument_llm = auto_instrument_llm
        self.tools: Dict[str, Tool] = {}
        self.call_depth = contextvars.ContextVar("call_depth", default=0)
        self.network_tracer = NetworkTracer()
        self.is_active = False
        self.current_agent_id = contextvars.ContextVar("current_agent_id", default=None)
        self.agent_children = contextvars.ContextVar("agent_children", default=[])
        self.component_network_calls = {}  # Store network calls per component
        
        # Create output directory if it doesn't exist
        self.output_dir = Path("./traces")  # Using default traces directory
        self.output_dir.mkdir(exist_ok=True)

    def start_component(self, component_id: str):
        """Start tracking network calls for a component"""
        self.component_network_calls[component_id] = []
        self.network_tracer.network_calls = []  # Reset network calls

    def end_component(self, component_id: str):
        """End tracking network calls for a component"""
        self.component_network_calls[component_id] = self.network_tracer.network_calls.copy()
        self.network_tracer.network_calls = []  # Reset for next component

    def start(self):
        """Start tracing"""
        # Start base tracer (includes system info and resource monitoring)
        super().start()
        self.is_active = True
        
        # Activate network tracing
        self.network_tracer.activate_patches()
        
        # Instrument calls from mixins
        if self.auto_instrument_llm:
            self.instrument_llm_calls()

    def stop(self):
        """Stop tracing and save results"""
        if self.is_active:
            # Calculate final metrics before stopping
            self._calculate_final_metrics()
            
            # Deactivate network tracing
            self.network_tracer.deactivate_patches()
            
            # Stop base tracer (includes saving to file)
            super().stop()
            
            # Cleanup
            self.unpatch_llm_calls()
            self.is_active = False


    def _calculate_final_metrics(self):
        """Calculate total cost and tokens from all components"""
        total_cost = 0.0
        total_tokens = 0
        
        def process_component(component):
            nonlocal total_cost, total_tokens
            # Convert component to dict if it's an object
            comp_dict = component.__dict__ if hasattr(component, '__dict__') else component
            
            if comp_dict.get('type') == "llm":
                info = comp_dict.get('info', {})
                if isinstance(info, dict):
                    # Extract cost
                    cost_info = info.get('cost', {})
                    if isinstance(cost_info, dict):
                        total_cost += cost_info.get('total_cost', 0)
                    
                    # Extract tokens
                    token_info = info.get('tokens', {})
                    if isinstance(token_info, dict):
                        total_tokens += token_info.get('total_tokens', 0)
                    else:
                        token_info = info.get('token_usage', {})
                        if isinstance(token_info, dict):
                            total_tokens += token_info.get('total_tokens', 0)
            
            # Process children if they exist
            data = comp_dict.get('data', {})
            if isinstance(data, dict):
                children = data.get('children', [])
                if children:
                    for child in children:
                        process_component(child)
        
        # Process all root components
        for component in self.components:
            process_component(component)
        
        # Update metadata in trace
        if hasattr(self, 'trace'):
            if isinstance(self.trace.metadata, dict):
                self.trace.metadata['total_cost'] = total_cost
                self.trace.metadata['total_tokens'] = total_tokens
            else:
                self.trace.metadata.total_cost = total_cost
                self.trace.metadata.total_tokens = total_tokens

    def add_component(self, component_data: dict):
        """Add a component to the trace data"""
        component_id = component_data["id"]
        
        # Convert dict to appropriate Component type
        if component_data["type"] == "llm":
            component = LLMComponent(**component_data)
            # Add network calls specific to this LLM component
            component_data["network_calls"] = self.component_network_calls.get(component_id, [])
            # Add user interaction for LLM calls
            component_data["interactions"] = [{
                "id": f"int_{uuid.uuid4()}",
                "interaction_type": "input",
                "content": component_data["data"]["input"]
            }, {
                "id": f"int_{uuid.uuid4()}",
                "interaction_type": "output",
                "content": component_data["data"]["output"]
            }]
        elif component_data["type"] == "agent":
            component = AgentComponent(**component_data)
            # Add network calls specific to this agent component
            component_data["network_calls"] = self.component_network_calls.get(component_id, [])
            # Add user interaction for agent
            component_data["interactions"] = [{
                "id": f"int_{uuid.uuid4()}",
                "interaction_type": "input",
                "content": component_data["data"]["input"]
            }, {
                "id": f"int_{uuid.uuid4()}",
                "interaction_type": "output",
                "content": component_data["data"]["output"]
            }]
        elif component_data["type"] == "tool":
            component = ToolComponent(**component_data)
            # Add network calls specific to this tool component
            component_data["network_calls"] = self.component_network_calls.get(component_id, [])
            # Add user interaction for tool
            component_data["interactions"] = [{
                "id": f"int_{uuid.uuid4()}",
                "interaction_type": "input",
                "content": component_data["data"]["input"]
            }, {
                "id": f"int_{uuid.uuid4()}",
                "interaction_type": "output",
                "content": component_data["data"]["output"]
            }]
        else:
            component = Component(**component_data)
        
        # Check if there's an active agent context
        current_agent_id = self.current_agent_id.get()
        if current_agent_id and component_data["type"] in ["llm", "tool"]:
            # Add this component as a child of the current agent
            current_children = self.agent_children.get()
            current_children.append(component_data)
            self.agent_children.set(current_children)
        else:
            # Add component to the main trace
            super().add_component(component)

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit"""
        self.stop()