import shutil
import subprocess
from pathlib import Path

"""
git config --global user.name <name>
git config --global user.email <email>
git config --global credential.helper store
"""


class GitSimple:
    def __init__(self, path: str | None = None, exist_ok: bool = True):
        """
        path: local target repository path
        """
        self.path = Path(path or ".").resolve()
        if exist_ok and not self.path.exists():
            self.path.mkdir(exist_ok=True, parents=True)

    def cmd(
        self, opts: str | list[str], capture: bool = False, path: str = None, raise_err: bool = True
    ) -> subprocess.CompletedProcess | None:
        path = path or self.path

        error_, retcode = None, None
        try:
            retcode = subprocess.run(opts, text=True, check=True, shell=True, cwd=path, capture_output=capture)
        except subprocess.CalledProcessError as e:
            error_ = (opts, e)

        if raise_err and error_:
            raise ValueError(f"{error_}")

        return retcode

    def exists(self, path: str = None) -> bool:
        path = path or self.path
        return (Path(path) / ".git").exists()

    def remove(self, path: str):
        shutil.rmtree(path)

    def clone(self, repo: str, branch: str | None = None, exists_ok: bool = False, path: str | None = None) -> bool:
        """
        git clone <repo>
        git clone <repo> -b <branch>
        """
        path = path or self.path
        args = f"git clone {repo} {path}"
        if branch is not None:
            args += f" -b {branch}"
        if exists_ok and self.exists(path=path):
            return False

        rtn = self.cmd(args)

        return rtn is not None

    def status(self) -> list[tuple[str, str]]:
        """
        git status
        git status --porcelain
            XY <file>

            State Code            XY
            --------------        --
            ' ': Unchanged
            'M': Modified       # MM
            'A': Added          # A
            'D': Deleted        # DD
            'R': Renamed        # R
            'C': Copied         # C
            'U': Unmerged       # UU
            '?': Untracked      # ??
            '!': Ignored        # !!
        """
        args = r"git status --porcelain"

        content = self.cmd(args, capture=True).stdout.strip()

        changes = []
        for line in content.split("\n"):
            if not line.strip():
                continue

            status_code, file = line[:2], line[3:]
            changes.append((status_code, file))

        return changes

    def branch(self, current: bool = False, remote: bool = False) -> str | list[str]:
        """
        git branch
        git branch --all
        git rev-parse --abbrev-ref HEAD
        """
        if current:
            return self.cmd(r"git rev-parse --abbrev-ref HEAD", capture=True).stdout.strip()

        args = r"git branch"
        if remote:
            args += r" -a"  # --all
        content = self.cmd(args, capture=True).stdout.strip()

        branches = []
        for line in content.split("\n"):
            line = line.strip()

            if line.startswith("*"):
                branches = [line[2:]] + branches
            else:
                if remote:
                    if "HEAD ->" in line:
                        continue
                    line = line.split(r"/", 1)[-1]
                branches.append(line)

        return branches

    def del_branch(self, branch: str, remote: bool = False, force: bool = False, not_exist_ok: bool = False) -> str | None:
        """
        git branch -d <branch>
        git branch -D <branch>
        git push origin --delete <branch>
        """
        if not_exist_ok:
            b = f"origin/{branch}" if remote else branch
            if b not in self.branch(remote=remote):
                return None

        if remote:
            args = f"git push origin --delete {branch}"
        else:
            args = r"git branch"
            args += " -D" if force else " -d"
            args += f" {branch}"

        content = self.cmd(args, capture=True).stdout.strip()

        return content

    def fetch(self, prune: bool = False, branch: str = None) -> str | None:
        """
        git fetch
        git fetch --all
        git fetch --tags
        git fetch --prune
        git fetch origin <branch>
        """
        args = "git fetch"
        if prune:
            args += " --prune"
        if branch:
            args += f" origin {branch}"

        content = self.cmd(args, capture=True).stdout.strip()

        return content

    def switch(self, branch: str, create: bool = True, exist_ok: bool = False) -> str | None:
        """
        git switch <branch>
        git switch -c <branch>
        """
        args = r"git switch"
        if create and (not exist_ok or branch not in self.branch()):
            args += " -c"
        args += f" {branch}"

        content = self.cmd(args, capture=True).stdout.strip()

        return content

    def checkout(self, target: str):
        """
        git checkout <branch|commit|tag>
        """
        args = r"git checkout"
        args += f" {target}"

        content = self.cmd(args, capture=True).stdout.strip()

        return content

    def add(self, files: list[str] = None) -> bool:
        """
        git add .
        git add <file1> <file2>
        """
        files = " ".join(str(f) for f in files) if files else "."

        args = f"git add {files}"

        rtn = self.cmd(args)

        return rtn is not None

    def commit(self, message: str, no_change_ok: bool = False) -> str | None:
        """
        git commit -m <message>
        """
        if no_change_ok and len(self.status()) == 0:
            return None

        args = f'git commit -m "{message}"'

        content = self.cmd(args, capture=True).stdout.strip()

        return content

    def push(self, branch: str = None, no_commit_ok: bool = True) -> str | None:
        """
        git push
        git push origin <branch>
        """
        args = r"git push"
        if branch:
            args += f" origin {branch}"

        content = self.cmd(args, capture=True).stdout.strip()

        return content

    def pull(self, branch: str = None) -> str | None:
        """
        git pull
        git pull origin <branch>
        """
        args = r"git pull"
        if branch:
            args += f" origin {branch}"

        content = self.cmd(args, capture=True).stdout.strip()

        return content

    def reset(self, commit: str = None, mode: str = "hard") -> str | None:
        """
        git reset
        git reset --hard
        """
        args = f"git reset --{mode}"
        if commit:
            args += f" {commit}"

        content = self.cmd(args, capture=True).stdout.strip()

        return content

    def tags(self, remote: bool = False) -> list[str]:
        """
        git tag
        git ls-remote --tags
        """
        args = "git tag" if not remote else "git ls-remote --tags"

        content = self.cmd(args, capture=True).stdout.strip()
        if remote:
            tags = content.split("\n")
            tags = [t.split("refs/tags/")[-1] for t in tags]
            tags = [t for t in tags if len(t) > 4 and t[-3:] != r"^{}"]
        else:
            tags = content.split("\n")

        return tags
