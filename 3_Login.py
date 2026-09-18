import runpy
from pathlib import Path

target = Path(__file__).parent / "pages" / "3_Login.py"
runpy.run_path(str(target), run_name="__main__")
