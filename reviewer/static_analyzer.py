import subprocess
import json

def analyze_code(file_path:str):
    try:

        result=subprocess.run(
        ["ruff","check",file_path,"--output-format","json"],
        capture_output=True,
        text=True,
        timeout=30
        )
        if result.returncode == 2:
            raise RuntimeError(f"Ruff Error:{result.stderr}")
        findings=json.loads(result.stdout)
        return findings
    except FileNotFoundError:
        raise RuntimeError("Ruff is not installed")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Ruff analysis Timed out")
        
    
    



        
