import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent


def main():
    py = sys.executable
    manage = root / "manage.py"
    subprocess.run([py, str(manage), "migrate"], cwd=root, check=True)
    subprocess.run([py, str(manage), "seed_movies"], cwd=root, check=True)


if __name__ == "__main__":
    main()
