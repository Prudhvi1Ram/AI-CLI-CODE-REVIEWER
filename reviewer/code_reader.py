from pathlib import Path

def read_code(file_path:str):
    path=Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found:{file_path}")
    if not path.is_file():
        raise ValueError("The path is not a file")
    if path.suffix != ".py":
        raise ValueError("Only python files are supported")
    code = path.read_text(encoding="utf-8")

    return code