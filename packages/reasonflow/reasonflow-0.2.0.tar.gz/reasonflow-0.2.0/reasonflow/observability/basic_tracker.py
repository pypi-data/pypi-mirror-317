from .tracking_interface import TrackingInterface
from .tracker import TaskTracker
from ..orchestrator.state_manager import StateManager
from reasonchain.memory import SharedMemory
from typing import Dict, Any
from datetime import datetime
from .metrics import Metrics

class BasicTracker(TrackingInterface):
    def __init__(self):
        self.shared_memory = SharedMemory()
        self.task_tracker = TaskTracker(shared_memory=self.shared_memory)
        self.state_manager = StateManager()
        self.metrics = Metrics(shared_memory=self.shared_memory)
    
    def track_workflow(self, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Use existing state management for workflows"""
        print(f"Tracking workflow {workflow_id}: {event_type}")
        state = self.state_manager.load_state(workflow_id) or {}
        state.update({
            "status": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        self.state_manager.save_state(workflow_id, state)
        
        # Record workflow metrics
        if event_type == "completed":
            duration = data.get("duration", 0)
            success = data.get("status") == "success"
            self.metrics.record_workflow_metrics(workflow_id, duration, success)
    
    def track_task(self, task_id: str, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Use existing task tracker and record metrics"""
        self.task_tracker.log(task_id, data.get("name", ""), event_type)
        
        # Record task metrics
        if event_type == "completed":
            duration = data.get("duration", 0)
            success = data.get("status") == "success"
            self.metrics.record_task_metrics(task_id, duration, success)

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status from state manager"""
        state = self.state_manager.load_state(workflow_id) or {}
        metrics = self.metrics.get_workflow_metrics(workflow_id)
        return {
            "status": state.get("status", "unknown"),
            "data": state.get("data", {}),
            "timestamp": state.get("timestamp"),
            "metrics": metrics
        }

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status from task tracker"""
        logs = self.task_tracker.get_logs()
        task_logs = [log for log in logs if log["task_id"] == task_id]
        metrics = self.metrics.get_task_metrics(task_id)
        return {
            "status": task_logs[-1]["status"] if task_logs else "unknown",
            "history": task_logs,
            "last_update": task_logs[-1]["timestamp"] if task_logs else None,
            "metrics": metrics
        }
        
    def get_task_metrics(self, task_id: str) -> Dict[str, Any]:
        """Get task metrics"""
        return {
            "duration": self.metrics.get_task_metrics(task_id).get("total_duration", 0),
            "memory_usage": 0,  # Not tracked in basic implementation
            "cpu_usage": 0,     # Not tracked in basic implementation
            "error_rate": self.metrics.get_task_metrics(task_id).get("failure_count", 0) / 
                         max(1, self.metrics.get_task_metrics(task_id).get("execution_count", 1)),
            "retry_count": 0    # Not tracked in basic implementation
        } 