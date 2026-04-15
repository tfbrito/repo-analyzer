import shutil
import subprocess
import tempfile
from pathlib import Path


class RepoCloner:
    """Context manager that clones a git repo to a temp directory and cleans up on exit."""

    def __init__(self, url: str):
        self.url = url
        self.tmp_dir = None

    def __enter__(self) -> Path:
        self.tmp_dir = tempfile.mkdtemp(prefix="repo-analyzer-")
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", self.url, self.tmp_dir],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            shutil.rmtree(self.tmp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to clone {self.url}: {e.stderr.strip()}") from e
        return Path(self.tmp_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tmp_dir:
            shutil.rmtree(self.tmp_dir, ignore_errors=True)
        return False
