from typing import Dict, Any
from datetime import datetime, UTC
import logging
import asyncio
import configparser
import os
from .tracking_interface import TrackingInterface

from reasontrack import (
    EventManager,
    MetricsCollector,
    AlertManager,
    StateStorage,
    AlertSeverity,
    EventType,
    HealthChecker,
    MetricType,
)
from reasontrack.storage.event_store import EventStorage
from reasontrack.core.event_manager import Event
from reasontrack.storage.state_store import StateStorageConfig
from reasontrack.core.alert_manager import Alert

logger = logging.getLogger(__name__)

class ReasonTrackAdapter(TrackingInterface):
    def __init__(self, config: Dict[str, Any]):
        try:
            # Convert dict config to INI format
            config_parser = configparser.ConfigParser()
            
            # Event Manager Section
            config_parser["event_manager"] = {
                "backend": config.get("event_manager", {}).get("backend", "kafka"),
                "broker_url": config.get("event_manager", {}).get("broker_url", "localhost:9092"),
                "topic_prefix": config.get("event_manager", {}).get("topic_prefix", "reasonflow_events_"),
                "client_id": config.get("event_manager", {}).get("client_id", "reasonflow"),
                "batch_size": str(config.get("event_manager", {}).get("batch_size", 100)),
                "flush_interval": str(config.get("event_manager", {}).get("flush_interval", 10))
            }
            
            # Metrics Collector Section
            config_parser["metrics_collector"] = {
                "backend": config.get("metrics_collector", {}).get("backend", "prometheus"),
                "pushgateway_url": config.get("metrics_collector", {}).get("pushgateway_url", "localhost:9091"),
                "job_name": config.get("metrics_collector", {}).get("job_name", "reasonflow_metrics"),
                "push_interval": str(config.get("metrics_collector", {}).get("push_interval", 15))
            }
            
            # Alert Manager Section
            config_parser["alert_manager"] = {
                "storage_path": config.get("alert_manager", {}).get("storage_path", "alerts"),
                "retention_days": str(config.get("alert_manager", {}).get("retention_days", 30)),
                "severity_levels": ",".join(config.get("alert_manager", {}).get("severity_levels", ["INFO", "WARNING", "ERROR", "CRITICAL"]))
            }
            
            # Alert Manager Slack Section
            config_parser["alert_manager.slack"] = {
                "webhook_url": config.get("alert_manager", {}).get("notification_backends", {}).get("slack", {}).get("webhook_url", "")
            }
            
            # Alert Manager Email Section
            email_config = config.get("alert_manager", {}).get("notification_backends", {}).get("email", {})
            config_parser["alert_manager.email"] = {
                "smtp_host": email_config.get("smtp_host", "smtp.gmail.com"),
                "smtp_port": str(email_config.get("smtp_port", 587)),
                "username": email_config.get("username", ""),
                "password": email_config.get("password", ""),
                "from_address": email_config.get("from_address", ""),
                "to_addresses": ",".join(email_config.get("to_addresses", [])),
                "use_tls": str(email_config.get("use_tls", True)).lower()
            }
            
            # State Manager Section
            config_parser["state_manager"] = {
                "storage_path": config.get("state_manager", {}).get("storage_path", "workflow_states"),
                "backend": config.get("state_manager", {}).get("backend", "memory"),
                "prefix": config.get("state_manager", {}).get("prefix", "reasonflow_state_"),
                "ttl": str(config.get("state_manager", {}).get("ttl", 3600))
            }
            
            # Telemetry Section
            config_parser["telemetry"] = {
                "service_name": config.get("telemetry", {}).get("service_name", "reasonflow"),
                "endpoint": config.get("telemetry", {}).get("endpoint", "localhost:4317"),
                "enable_metrics": str(config.get("telemetry", {}).get("enable_metrics", True)).lower(),
                "enable_tracing": str(config.get("telemetry", {}).get("enable_tracing", True)).lower()
            }
            
            # Logging Section
            config_parser["logging"] = {
                "level": config.get("logging", {}).get("level", "INFO"),
                "format": config.get("logging", {}).get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
                "file": config.get("logging", {}).get("file", "logs/reasontrack.log")
            }
            
            # Initialize components with INI config
            self.event_manager = EventManager(
                backend=config_parser.get("event_manager", "backend"),
                broker_url=config_parser.get("event_manager", "broker_url"),
                topic_prefix=config_parser.get("event_manager", "topic_prefix"),
                client_id=config_parser.get("event_manager", "client_id"),
                batch_size=config_parser.getint("event_manager", "batch_size"),
                flush_interval=config_parser.getint("event_manager", "flush_interval")
            )
            
            self.metrics_collector = MetricsCollector(
                backend=config_parser.get("metrics_collector", "backend"),
                pushgateway_url=config_parser.get("metrics_collector", "pushgateway_url"),
                job_name=config_parser.get("metrics_collector", "job_name"),
                push_interval=config_parser.getint("metrics_collector", "push_interval")
            )
            
            self.alert_manager = AlertManager(
                storage_path=config_parser.get("alert_manager", "storage_path"),
                retention_days=config_parser.getint("alert_manager", "retention_days"),
                severity_levels=config_parser.get("alert_manager", "severity_levels").split(","),
                notification_backends={
                    "slack": {
                        "webhook_url": config_parser.get("alert_manager.slack", "webhook_url")
                    },
                    "email": {
                        "smtp_host": config_parser.get("alert_manager.email", "smtp_host"),
                        "smtp_port": config_parser.getint("alert_manager.email", "smtp_port"),
                        "username": config_parser.get("alert_manager.email", "username"),
                        "password": config_parser.get("alert_manager.email", "password"),
                        "from_address": config_parser.get("alert_manager.email", "from_address"),
                        "to_addresses": config_parser.get("alert_manager.email", "to_addresses").split(","),
                        "use_tls": config_parser.getboolean("alert_manager.email", "use_tls")
                    }
                }
            )
            
            self.state_storage = StateStorage(
                storage_path=config_parser.get("state_manager", "storage_path"),
                backend=config_parser.get("state_manager", "backend"),
                prefix=config_parser.get("state_manager", "prefix"),
                ttl=config_parser.getint("state_manager", "ttl")
            )
            
            self.health_checker = HealthChecker()
            
            # Configure logging
            logging.basicConfig(
                level=getattr(logging, config_parser.get("logging", "level")),
                format=config_parser.get("logging", "format"),
                filename=config_parser.get("logging", "file")
            )
            
        except ImportError:
            raise ImportError("ReasonTrack is not installed. Install it with: pip install reasontrack")
        except Exception as e:
            logger.error(f"Error initializing ReasonTrack: {str(e)}")
            raise

    def track_workflow(self, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Track workflow events with enhanced metadata"""
        event_type_map = {
            "started": EventType.WORKFLOW_START,
            "completed": EventType.WORKFLOW_COMPLETE,
            "failed": EventType.WORKFLOW_FAIL,
            "paused": EventType.WORKFLOW_PAUSE,
            "resumed": EventType.WORKFLOW_RESUME
        }
        
        try:
            # Create and track event
            event = Event(
                event_id=f"workflow_{event_type}_{workflow_id}",
                event_name=f"workflow_{workflow_id}",
                event_type=event_type_map.get(event_type, event_type).name,
                source="reasonflow",
                metadata={
                    "workflow_id": workflow_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                    **data
                }
            )
            
            # Run event tracking in event loop
            asyncio.create_task(self.event_manager.track_event(event))
            
            # Update state for completed workflows
            if event_type == "completed":
                state_data = {
                    "status": "completed",
                    "end_time": datetime.now(UTC).isoformat(),
                    **data
                }
                asyncio.create_task(self.state_storage.set_state(f"workflow_{workflow_id}", state_data))
                
            # Update state for started workflows
            elif event_type == "started":
                state_data = {
                    "status": "running",
                    "start_time": datetime.now(UTC).isoformat(),
                    **data
                }
                asyncio.create_task(self.state_storage.set_state(f"workflow_{workflow_id}", state_data))
                
        except Exception as e:
            logger.error(f"Error tracking workflow event: {str(e)}")
            # Trigger error alert
            alert = Alert(
                alert_id=f"workflow_{workflow_id}_error",
                alert_name="Workflow Tracking Error",
                alert_message=f"Failed to track workflow {workflow_id}: {str(e)}",
                alert_source="reasonflow",
                severity=AlertSeverity.ERROR.name,
                metadata={"workflow_id": workflow_id}
            )
            asyncio.create_task(self.alert_manager.trigger_alert(alert))

    def track_task(self, task_id: str, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Track task events with metrics collection"""
        event_type_map = {
            "started": EventType.TASK_START,
            "completed": EventType.TASK_COMPLETE,
            "failed": EventType.TASK_FAIL,
            "retrying": EventType.TASK_RETRY,
            "skipped": EventType.TASK_SKIP
        }
        
        try:
            # Create and track event
            event = Event(
                event_id=f"task_{event_type}_{task_id}",
                event_name=f"task_{task_id}",
                event_type=event_type_map.get(event_type, event_type).name,
                source="reasonflow",
                metadata={
                    "task_id": task_id,
                    "workflow_id": workflow_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                    **data
                }
            )
            
            # Run event tracking in event loop
            asyncio.create_task(self.event_manager.track_event(event))
            
            # Record metrics for completed tasks
            if event_type == "completed":
                metrics = {
                    "task_duration": data.get("duration", 0),
                    "task_memory_usage": data.get("memory_usage", 0),
                    "task_cpu_usage": data.get("cpu_usage", 0),
                    "task_error_rate": 0 if data.get("status") == "success" else 1,
                    "task_retry_count": data.get("retries", 0)
                }
                
                for metric_name, value in metrics.items():
                    asyncio.create_task(self.metrics_collector.record_metric(
                        name=metric_name,
                        value=value,
                        metric_type=MetricType.TASK_DURATION if "duration" in metric_name else MetricType.GAUGE,
                        labels={
                            "task_id": task_id,
                            "workflow_id": workflow_id
                        }
                    ))
                    
                # Trigger completion alert
                alert = Alert(
                    alert_id=f"task_{task_id}_completion",
                    alert_name="Task Completion",
                    alert_message=f"Task {task_id} completed successfully",
                    alert_source="reasonflow",
                    severity=AlertSeverity.INFO.name,
                    metadata={
                        "workflow_id": workflow_id,
                        "task_id": task_id
                    }
                )
                asyncio.create_task(self.alert_manager.trigger_alert(alert))
                
        except Exception as e:
            logger.error(f"Error tracking task event: {str(e)}")
            # Trigger error alert
            alert = Alert(
                alert_id=f"task_{task_id}_error",
                alert_name="Task Tracking Error",
                alert_message=f"Failed to track task {task_id}: {str(e)}",
                alert_source="reasonflow",
                severity=AlertSeverity.ERROR.name,
                metadata={
                    "workflow_id": workflow_id,
                    "task_id": task_id
                }
            )
            asyncio.create_task(self.alert_manager.trigger_alert(alert))

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get comprehensive workflow status"""
        try:
            # Get all workflow data asynchronously
            loop = asyncio.get_event_loop()
            metrics = loop.run_until_complete(self.metrics_collector.get_metrics(f"workflow_{workflow_id}"))
            events = loop.run_until_complete(self.event_manager.get_events(workflow_id=workflow_id))
            state = loop.run_until_complete(self.state_storage.get_state(f"workflow_{workflow_id}"))
            health = loop.run_until_complete(self.health_checker.check_overall_health())
            
            return {
                "metrics": metrics,
                "events": events,
                "state": state,
                "health": health
            }
        except Exception as e:
            logger.error(f"Error getting workflow status: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    def get_task_metrics(self, task_id: str) -> Dict[str, Any]:
        """Get comprehensive task metrics"""
        try:
            loop = asyncio.get_event_loop()
            metrics = {}
            metric_names = [
                "task_duration",
                "task_memory_usage", 
                "task_cpu_usage",
                "task_error_rate",
                "task_retry_count"
            ]
            
            for name in metric_names:
                value = loop.run_until_complete(self.metrics_collector.get_metric(
                    name=name,
                    labels={"task_id": task_id}
                ))
                metrics[name.replace("task_", "")] = value
                
            return metrics
        except Exception as e:
            logger.error(f"Error getting task metrics: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }