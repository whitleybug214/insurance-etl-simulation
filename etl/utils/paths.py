from pathlib import Path

BASE_DIR = Path("data")

RAW_DATA_DIR = BASE_DIR / "raw"
TRANSFORMED_DATA_DIR = BASE_DIR / "transformed"
REJECTED_DATA_DIR = BASE_DIR / "rejected"

def ensure_dir(path: str | Path) -> Path:
    """
    Ensures a directory exists. Creates it if missing.
    Args:
        path (str or Path): Path to the directory
    Returns:
        Path: The resolved Path object
    """

    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)

    return p