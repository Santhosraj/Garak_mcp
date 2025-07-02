from garak import cli

def run_garak(model_string="ollama:llama2", plugins=["probe.prompt_injection"]):
    # Compose CLI arguments for garak
    args = [
        "--model_type", model_string.split(":")[0],
        "--model_name", model_string.split(":")[1],
        "--probes", ",".join(plugins),
        "--parallel_attempts", "8",  # Increase for speed, adjust as needed
        "--parallel_requests", "8",  # Increase for speed, adjust as needed
    ]
    cli.main(args)
