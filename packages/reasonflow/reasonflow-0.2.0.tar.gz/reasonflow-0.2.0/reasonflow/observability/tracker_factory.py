from typing import Dict, Any, Optional
from .basic_tracker import BasicTracker
from .reasontrack_adapter import ReasonTrackAdapter
from .tracking_interface import TrackingInterface

class TrackerFactory:
    @staticmethod
    def validate_config(tracker_type: str, config: Optional[Dict[str, Any]] = None) -> None:
        """Validate tracker configuration"""
        if tracker_type == "reasontrack":
            if not config:
                raise ValueError("ReasonTrack requires configuration")
            
            required_configs = {
                "event_manager": {
                    "backend": str,
                    "kafka_config": ["bootstrap_servers", "topic_prefix"]
                },
                "metric_manager": {
                    "backend": str,
                    "prometheus_config": ["gateway_url", "job_name"]
                },
                "alert_manager": {
                    "storage": ["path", "retention_days"],
                    "notification_backends": dict
                },
                "state_manager": {
                    "storage": ["path", "backend", "prefix", "ttl"]
                }
            }
            
            for section, requirements in required_configs.items():
                if section not in config:
                    raise ValueError(f"Missing required section: {section}")
                
                for key, value in requirements.items():
                    if key not in config[section]:
                        raise ValueError(f"Missing required field '{key}' in {section}")
                    
                    if isinstance(value, type):
                        if not isinstance(config[section][key], value):
                            raise ValueError(f"Field '{key}' in {section} must be of type {value.__name__}")
                    elif isinstance(value, list):
                        if key not in config[section] or not isinstance(config[section][key], dict):
                            raise ValueError(f"Missing or invalid {key} configuration in {section}")
                        for field in value:
                            if field not in config[section][key]:
                                raise ValueError(f"Missing required field '{field}' in {section}.{key}")

    @staticmethod
    def create_tracker(tracker_type: str = "basic", config: Optional[Dict[str, Any]] = None) -> TrackingInterface:
        """Create appropriate tracker based on type with validation"""
        try:
            TrackerFactory.validate_config(tracker_type, config)
            
            if tracker_type == "basic":
                return BasicTracker()
            elif tracker_type == "reasontrack":
                return ReasonTrackAdapter(config or {})
            else:
                raise ValueError(f"Unknown tracker type: {tracker_type}")
                
        except Exception as e:
            print(f"Error creating tracker: {str(e)}")
            print("Falling back to basic tracker...")
            return BasicTracker() 