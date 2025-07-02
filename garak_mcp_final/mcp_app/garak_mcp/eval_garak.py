"""
Garak Evaluation Integration
Enhanced Garak evaluation with better error handling and reporting
"""

import subprocess
import logging
import os
import sys
from typing import List, Dict, Any, Optional
import json
import tempfile
from datetime import datetime

logger = logging.getLogger(__name__)

class GarakEvaluator:
    """
    Enhanced Garak evaluation wrapper with better configuration and reporting
    """
    
    def __init__(self):
        self.garak_available = self._check_garak_availability()
        self.evaluation_history = []
    
    def _check_garak_availability(self) -> bool:
        """Check if Garak is available in the environment"""
        try:
            import garak
            return True
        except ImportError:
            logger.warning("Garak not found. Install with: pip install garak")
            return False
    
    def run_evaluation(self, 
                      model_string: str = "azure:gpt4",
                      plugins: List[str] = None,
                      parallel_attempts: int = 4,
                      parallel_requests: int = 4,
                      output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Run Garak evaluation with enhanced configuration and reporting
        """
        if not self.garak_available:
            return {
                "status": "error",
                "message": "Garak is not available. Please install it with: pip install garak",
                "timestamp": datetime.now().isoformat()
            }
        
        if plugins is None:
            plugins = ["promptinject"]
        
        # Parse model string
        try:
            model_type, model_name = model_string.split(":", 1)
        except ValueError:
            return {
                "status": "error", 
                "message": f"Invalid model string format: {model_string}. Expected 'type:name'",
                "timestamp": datetime.now().isoformat()
            }
        
        # Create output directory if specified
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="garak_eval_")
        
        # Prepare Garak arguments
        args = [
            "python", "-m", "garak",
            "--model_type", model_type,
            "--model_name", model_name,
            "--probes", ",".join(plugins),
            "--parallel_attempts", str(parallel_attempts),
            "--parallel_requests", str(parallel_requests),
            "--report_prefix", f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ]
        
        # Add Azure-specific environment variables if using Azure
        env = os.environ.copy()
        if model_type.lower() == "azure":
            required_vars = ["AZURE_API_KEY", "AZURE_ENDPOINT", "AZURE_MODEL_NAME"]
            missing_vars = [var for var in required_vars if not env.get(var)]
            
            if missing_vars:
                return {
                    "status": "error",
                    "message": f"Missing required environment variables for Azure: {', '.join(missing_vars)}",
                    "timestamp": datetime.now().isoformat()
                }
        
        logger.info(f"Starting Garak evaluation with args: {' '.join(args)}")
        
        try:
            # Run Garak evaluation
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
                env=env
            )
            
            evaluation_result = {
                "status": "completed" if result.returncode == 0 else "failed",
                "model_string": model_string,
                "plugins": plugins,
                "parallel_attempts": parallel_attempts,
                "parallel_requests": parallel_requests,
                "timestamp": datetime.now().isoformat(),
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
            # Try to parse any JSON reports generated in current directory
            try:
                report_files = [f for f in os.listdir(".") if f.endswith('.json') and f.startswith("eval_")]
                if report_files:
                    report_path = report_files[0]  # Use the most recent report
                    with open(report_path, 'r') as f:
                        evaluation_result["report"] = json.load(f)
            except Exception as e:
                logger.warning(f"Could not parse report files: {e}")
            
            # Add to history
            self.evaluation_history.append(evaluation_result)
            
            if result.returncode == 0:
                logger.info("Garak evaluation completed successfully")
            else:
                logger.error(f"Garak evaluation failed with return code {result.returncode}")
                logger.error(f"STDERR: {result.stderr}")
            
            return evaluation_result
            
        except subprocess.TimeoutExpired:
            logger.error("Garak evaluation timed out")
            return {
                "status": "timeout",
                "message": "Evaluation timed out after 1 hour",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error running Garak evaluation: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_evaluation_history(self) -> List[Dict[str, Any]]:
        """Get the history of evaluations run"""
        return self.evaluation_history
    
    def get_latest_evaluation(self) -> Optional[Dict[str, Any]]:
        """Get the most recent evaluation result"""
        return self.evaluation_history[-1] if self.evaluation_history else None

# Global evaluator instance
_garak_evaluator = None

def get_garak_evaluator() -> GarakEvaluator:
    """Get or create the global Garak evaluator"""
    global _garak_evaluator
    if _garak_evaluator is None:
        _garak_evaluator = GarakEvaluator()
    return _garak_evaluator

def run_garak(model_string: str = "azure:gpt4", 
              plugins: List[str] = None,
              **kwargs) -> Dict[str, Any]:
    """
    Legacy function for backwards compatibility
    Run Garak evaluation with the specified parameters
    """
    evaluator = get_garak_evaluator()
    return evaluator.run_evaluation(model_string, plugins, **kwargs)

def run_garak_cli(model_string: str = "azure:gpt4", 
                  plugins: List[str] = None) -> None:
    """
    Legacy CLI function for backwards compatibility
    """
    if plugins is None:
        plugins = ["promptinject"]
    
    try:
        from garak import cli
        
        # Parse model string
        model_type, model_name = model_string.split(":", 1)
        
        # Compose CLI arguments for garak
        args = [
            "--model_type", model_type,
            "--model_name", model_name,
            "--probes", ",".join(plugins),
            "--parallel_attempts", "8",
            "--parallel_requests", "8",
        ]
        
        logger.info(f"Running Garak CLI with args: {args}")
        cli.main(args)
        
    except Exception as e:
        logger.error(f"Error in run_garak_cli: {e}")
        print(f"Error running Garak evaluation: {e}")

def list_available_probes() -> List[str]:
    """List all available Garak probes"""
    try:
        result = subprocess.run(
            ["python", "-m", "garak", "--list_probes"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            probes = []
            for line in result.stdout.split('\n'):
                if line.strip() and 'probes:' in line:
                    probe_name = line.split('probes:')[1].strip()
                    probes.append(probe_name)
            return probes
        else:
            logger.error(f"Error listing probes: {result.stderr}")
            return []
            
    except Exception as e:
        logger.error(f"Error listing probes: {e}")
        return []

def list_probes_by_category(category: str = "") -> List[str]:
    """List Garak probes filtered by category"""
    all_probes = list_available_probes()
    
    if not category:
        return all_probes
    
    # Filter by category
    filtered_probes = []
    for probe in all_probes:
        if category.lower() in probe.lower():
            filtered_probes.append(probe)
    
    return filtered_probes

def get_evaluation_summary(evaluation_result: Dict[str, Any]) -> str:
    """Generate a human-readable summary of evaluation results"""
    if evaluation_result["status"] == "error":
        return f"Evaluation failed: {evaluation_result.get('message', 'Unknown error')}"
    
    if evaluation_result["status"] == "timeout":
        return "Evaluation timed out after 1 hour"
    
    summary = f"""
Garak Evaluation Summary
========================
Model: {evaluation_result['model_string']}
Plugins: {', '.join(evaluation_result['plugins'])}
Status: {evaluation_result['status']}
Timestamp: {evaluation_result['timestamp']}
Output Directory: {evaluation_result['output_dir']}
"""
    
    if "report" in evaluation_result:
        report = evaluation_result["report"]
        summary += f"\nReport Summary:\n"
        # Add key metrics from the report if available
        if isinstance(report, dict):
            for key, value in report.items():
                if isinstance(value, (int, float, str)):
                    summary += f"  {key}: {value}\n"
    
    if evaluation_result["status"] == "failed":
        summary += f"\nError Output:\n{evaluation_result.get('stderr', 'No error details available')}"
    
    return summary