import os
from dotenv import load_dotenv
from reasonflow.orchestrator.workflow_builder import WorkflowBuilder
from reasonflow.orchestrator.workflow_engine import WorkflowEngine
from reasonflow.tasks.task_manager import TaskManager
from reasonflow.integrations.rag_integrations import RAGIntegration
from reasonflow.integrations.llm_integrations import LLMIntegration
from reasonflow.agents.data_retrieval_agent import DataRetrievalAgent
from reasonflow.agents.custom_task_agent import CustomTaskAgent
from reasonchain.memory import SharedMemory
import json
import time
import psutil
import configparser
# Load environment variables from .env file
load_dotenv()

# Initialize ReasonFlow components
def get_reasontrack_config():
    """Get ReasonTrack configuration"""
    config_path = os.path.join(os.path.dirname(__file__), "config", "reasontrack.ini")
    print(f"Loading config from: {config_path}")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    # Create config parser with basic interpolation
    config = configparser.ConfigParser(interpolation=configparser.BasicInterpolation())
    config.read(config_path)
    
    # Convert INI to dict format and handle environment variables
    config_dict = {}
    for section in config.sections():
        if "." in section:
            # Handle nested sections (e.g., alert_manager.slack)
            main_section, sub_section = section.split(".")
            if main_section not in config_dict:
                config_dict[main_section] = {}
            if "notification_backends" not in config_dict[main_section]:
                config_dict[main_section]["notification_backends"] = {}
            
            # Process section values and handle environment variables
            section_dict = {}
            for key, value in config[section].items():
                if value.startswith("${") and value.endswith("}"):
                    env_var = value[2:-1]
                    section_dict[key] = os.getenv(env_var, "")
                else:
                    section_dict[key] = value
            
            config_dict[main_section]["notification_backends"][sub_section] = section_dict
        else:
            # Process section values and handle environment variables
            section_dict = {}
            for key, value in config[section].items():
                if value.startswith("${") and value.endswith("}"):
                    env_var = value[2:-1]
                    section_dict[key] = os.getenv(env_var, "")
                else:
                    section_dict[key] = value
            config_dict[section] = section_dict
    
    return config_dict

def build_workflow(llm_extractor, llm_analyzer, llm_summarizer, shared_memory):
    """Build workflow configuration"""
    workflow_config = {
        "tasks": {
            "ingest-document": {
                "type": "data_retrieval",
                "config": {
                    "agent_config": {
                        "db_path": "vector_db_tesla.index",
                        "db_type": "faiss",
                        "embedding_provider": "sentence_transformers",
                        "embedding_model": "all-MiniLM-L6-v2",
                        "use_gpu": True,
                        "shared_memory": shared_memory
                    },
                    "params": {
                        "query": "Retrieve Tesla financial data",
                        "top_k": 20
                    }
                }
            },
            "extract-highlights": {
                "type": "llm",
                "config": {
                    "agent": llm_extractor,
                    "params": {
                        "prompt": """Extract key financial highlights from the following data: 
                        {{ingest-document.output}}
                        
                        Format your response as a bulleted list of the most important financial metrics and findings."""
                    }
                }
            },
            "analyze-trends": {
                "type": "llm",
                "config": {
                    "agent": llm_analyzer,
                    "params": {
                        "prompt": """Analyze the financial trends from these highlights:
                        {{extract-highlights.output}}
                        
                        Focus on:
                        - Revenue growth trends
                        - Profitability metrics
                        - Cash flow patterns
                        - Key business segments performance"""
                    }
                }
            },
            "summarize-insights": {
                "type": "llm",
                "config": {
                    "agent": llm_summarizer,
                    "params": {
                        "prompt": """Provide a concise executive summary of these financial trends:
                        {{analyze-trends.output}}
                        
                        Include:
                        1. Overall financial health
                        2. Key growth indicators
                        3. Risk factors
                        4. Future outlook"""
                    }
                }
            }
        },
        "dependencies": [
             {"from": "ingest-document", "to": "extract-highlights"},
            {"from": "extract-highlights", "to": "analyze-trends"},
            {"from": "analyze-trends", "to": "summarize-insights"}
        ]
    }
    return workflow_config

def main():
    shared_memory = SharedMemory()
    task_manager = TaskManager(shared_memory=shared_memory)
    workflow_builder = WorkflowBuilder(task_manager=task_manager, tracker_type="reasontrack", tracker_config=get_reasontrack_config())
        
    # Add document to the vector database
    rag_integration = RAGIntegration(
            db_path="vector_db_tesla.index",
            db_type="faiss",
            embedding_provider="sentence_transformers",
            embedding_model="all-MiniLM-L6-v2",
            shared_memory=shared_memory
    )
    rag_integration.add_documents(file_path="tsla-20240930-gen.pdf")
    print("Document added to vector database.")
    
    # Create agents
    llm_extractor = LLMIntegration(provider="openai", model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    llm_analyzer = LLMIntegration(provider="ollama", model="llama3.1:latest", api_key=None)
    llm_summarizer = LLMIntegration(provider="groq", model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

    # Build workflow
    workflow_config = build_workflow(llm_extractor, llm_analyzer, llm_summarizer, shared_memory)
    print(json.dumps(workflow_config, indent=2, default=str))
    workflow_id = workflow_builder.create_workflow(workflow_config)
    print(f"Workflow created with ID: {workflow_id}")

    # Execute workflow
    try:
        start_time = time.time()
        
        # Track workflow start
        workflow_builder.engine.tracker.track_workflow(
            workflow_id=workflow_id,
            event_type="started",
            data={"status": "started", "start_time": start_time}
        )
        
        results = workflow_builder.execute_workflow(workflow_id)
        end_time = time.time()
        duration = end_time - start_time
        
        # Track workflow completion
        workflow_builder.engine.tracker.track_workflow(
            workflow_id=workflow_id,
            event_type="completed",
            data={
                "status": "success",
                "duration": duration,
                "results": results
            }
        )
        
        # Get workflow metrics
        metrics = workflow_builder.engine.tracker.get_workflow_status(workflow_id)
        print("\nWorkflow Status and Metrics:")
        print(json.dumps(metrics, indent=2))
        
        # Track and get task-specific metrics
        for task_id in workflow_config["tasks"]:
            task_start = time.time()
            task_result = results.get(task_id, {})
            task_end = time.time()
            task_duration = task_end - task_start
            
            # Track task metrics
            workflow_builder.engine.tracker.track_task(
                task_id=task_id,
                workflow_id=workflow_id,
                event_type="completed",
                data={
                    "name": task_id,  # Added name for basic tracker
                    "status": "success" if task_result.get("status") != "error" else "failed",
                    "duration": task_duration,
                    "memory_usage": psutil.Process().memory_info().rss / 1024 / 1024,  # MB
                    "cpu_usage": psutil.Process().cpu_percent(),
                    "output": task_result.get("output", ""),
                    "error": task_result.get("error")
                }
            )
            
            # Get task metrics
            task_metrics = workflow_builder.engine.tracker.get_task_metrics(task_id)
            print(f"\nMetrics for task {task_id}:")
            print(json.dumps(task_metrics, indent=2))
        
        print("\n=== Workflow Execution Results ===")
        for task_id, result in results.items():
            print(f"\nTask {task_id}:")
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        
        # Track workflow failure
        workflow_builder.engine.tracker.track_workflow(
            workflow_id=workflow_id,
            event_type="failed",
            data={
                "status": "failed",
                "duration": duration,
                "error": str(e)
            }
        )
        print(f"Error executing workflow: {str(e)}")
        return

if __name__ == "__main__":
    main()
