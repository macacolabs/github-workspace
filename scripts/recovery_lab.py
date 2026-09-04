"""Git recovery lab fixtures, never a student's existing repository.
Run: python scripts/recovery_lab.py staged
Inputs: one scenario name. Output: new temporary practice folder with simulated Git state.
Observe: status, index, refs, remote history. No network, real credentials, or deletion.
Run --verify to rehearse every prescribed recovery in separate disposable folders.
"""
import argparse
import pathlib
import subprocess
import tempfile

MODES = ("staged", "branch", "committed", "remote", "conflict", "delete-conflict", "stash", "lost", "shared")

def git(path, *args, ok=True):
    result = subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false",
                             "-c", "core.hooksPath=" + str(path / ".no-hooks"),
                             "-C", str(path), *args], text=True, capture_output=True, encoding="utf-8")
    if ok and result.returncode:
        raise RuntimeError(result.stderr + result.stdout)
    return result

def require(condition):
    """Checks remain active even with python -O; never hide fixture operations."""
    if not condition:
        raise RuntimeError("Recovery scenario expectation failed")


def write(path, name, text):
    (path / name).write_text(text, encoding="utf-8")

def commit(path, message):
    git(path, "add", ".")
    git(path, "commit", "-m", message)

def prepare(mode):
    root = pathlib.Path(tempfile.mkdtemp(prefix="git-recovery-" + mode + "-"))
    repo = root / "student"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.name", "Practice Student")
    git(repo, "config", "user.email", "practice@example.invalid")
    # Persist isolation so student commands use the same settings as the fixture.
    git(repo, "config", "core.autocrlf", "false")
    git(repo, "config", "commit.gpgsign", "false")
    git(repo, "config", "core.hooksPath", str(repo / ".no-hooks"))
    write(repo, "README.md", "team=base\n")
    write(repo, "notes.md", "note=base\n")
    write(repo, ".gitignore", "build/\n")
    commit(repo, "docs: base")
    base = git(repo, "rev-parse", "HEAD").stdout.strip()
    if mode == "staged":
        write(repo, "README.md", "team=profile\n")
        git(repo, "add", "README.md")
        write(repo, "README.md", "team=profile-v2\n")
        write(repo, "notes.md", "note=unrelated\n")
        git(repo, "add", "notes.md")
        write(repo, "draft.md", "draft=keep\n")
    elif mode == "branch":
        git(repo, "switch", "-c", "feature/profile")
        write(repo, "README.md", "team=feature\n")
        commit(repo, "feat: profile")
        write(repo, "README.md", "team=unfinished\n")
        require(git(repo, "switch", "main", ok=False).returncode != 0)
    elif mode == "committed":
        write(repo, "README.md", "team=accidental-main\n")
        commit(repo, "feat: committed on wrong branch")
        git(repo, "tag", "practice-base", base)
    elif mode == "remote":
        remote = root / "remote.git"
        remote.mkdir()
        git(remote, "init", "--bare", "-b", "main")
        git(repo, "remote", "add", "origin", str(remote))
        git(repo, "push", "-u", "origin", "main")
        peer = root / "peer"
        git(root, "clone", str(remote), str(peer))
        git(peer, "config", "user.name", "Practice Peer")
        git(peer, "config", "user.email", "peer@example.invalid")
        write(peer, "peer.md", "peer=keep\n")
        commit(peer, "docs: peer update")
        git(peer, "push")
        write(repo, "local.md", "local=keep\n")
        commit(repo, "docs: local update")
        write(repo, "notes.md", "note=unfinished\n")
        require(git(repo, "push", ok=False).returncode != 0)
    elif mode in ("conflict", "delete-conflict"):
        git(repo, "switch", "-c", "feature/a")
        write(repo, "README.md", "team=A\n")
        commit(repo, "docs: A")
        git(repo, "switch", "main")
        git(repo, "switch", "-c", "feature/b")
        if mode == "conflict":
            write(repo, "README.md", "team=B\n")
        else:
            git(repo, "rm", "README.md")
        commit(repo, "docs: B")
        require(git(repo, "merge", "feature/a", ok=False).returncode != 0)
    elif mode == "stash":
        write(repo, "notes.md", "note=unfinished\n")
        write(repo, "draft.md", "draft=keep\n")
    elif mode == "lost":
        git(repo, "switch", "--detach", "HEAD")
        write(repo, "README.md", "team=lost-work\n")
        commit(repo, "feat: detached work")
        git(repo, "switch", "main")
    elif mode == "shared":
        write(repo, "README.md", "team=wrong\n")
        commit(repo, "docs: wrong value")
        git(repo, "tag", "practice-shared-tip")
    return repo

def verify(mode):
    repo = prepare(mode)
    if mode == "staged":
        require(git(repo, "status", "--short").stdout.startswith("MM README.md"))
        git(repo, "restore", "--staged", "notes.md")
        git(repo, "add", "README.md")
        git(repo, "commit", "-m", "docs: profile only")
        require("notes.md" not in git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").stdout)
        require((repo / "draft.md").exists())
        require((repo / "notes.md").read_text() == "note=unrelated\n")
    elif mode == "branch":
        git(repo, "stash", "push", "-m", "profile WIP")
        git(repo, "switch", "main")
        git(repo, "switch", "feature/profile")
        git(repo, "stash", "apply", "stash@{0}")
        require((repo / "README.md").read_text() == "team=unfinished\n")
        require(git(repo, "stash", "list").stdout)
    elif mode == "committed":
        tip = git(repo, "rev-parse", "HEAD").stdout.strip()
        git(repo, "switch", "-c", "feature/rescued")
        git(repo, "branch", "-f", "main", "practice-base")
        require(git(repo, "rev-parse", "main").stdout == git(repo, "rev-parse", "practice-base").stdout)
        require(git(repo, "rev-parse", "HEAD").stdout.strip() == tip)
    elif mode == "remote":
        git(repo, "stash", "push", "-m", "local WIP")
        git(repo, "fetch", "origin")
        require(git(repo, "rev-list", "--left-right", "--count", "HEAD...origin/main").stdout.strip() == "1\t1")
        git(repo, "merge", "--no-edit", "origin/main")
        git(repo, "push")
        git(repo, "stash", "apply", "stash@{0}")
        require((repo / "peer.md").exists() and (repo / "local.md").exists())
        require((repo / "notes.md").read_text() == "note=unfinished\n")
        require(git(repo, "rev-parse", "HEAD").stdout == git(repo, "rev-parse", "origin/main").stdout)
    elif mode == "conflict":
        tip = git(repo, "rev-parse", "HEAD").stdout
        git(repo, "merge", "--abort")
        require(git(repo, "rev-parse", "HEAD").stdout == tip)
        require(not git(repo, "status", "--porcelain").stdout)
        require(git(repo, "merge", "feature/a", ok=False).returncode != 0)
        write(repo, "README.md", "team=A+B\n")
        commit(repo, "merge: agreed team")
        require(len(git(repo, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()) == 3)
    elif mode == "delete-conflict":
        # Team decides the file is still required, so retain A's content.
        require((repo / "README.md").read_text() == "team=A\n")
        git(repo, "add", "README.md")
        git(repo, "commit", "-m", "merge: retain team description")
        require(not git(repo, "status", "--porcelain").stdout)
    elif mode == "stash":
        git(repo, "stash", "push", "-u", "-m", "profile WIP")
        require(not (repo / "draft.md").exists())
        git(repo, "stash", "apply", "stash@{0}")
        require((repo / "draft.md").read_text() == "draft=keep\n")
        require((repo / "notes.md").read_text() == "note=unfinished\n")
        git(repo, "stash", "drop", "stash@{0}")
        require(not git(repo, "stash", "list").stdout)
    elif mode == "lost":
        entries = git(repo, "reflog", "--format=%H %gs").stdout.splitlines()
        found = next(line.split()[0] for line in entries if "feat: detached work" in line)
        git(repo, "switch", "-c", "rescue/recovered", found)
        require((repo / "README.md").read_text() == "team=lost-work\n")
    elif mode == "shared":
        old = git(repo, "rev-parse", "HEAD").stdout.strip()
        git(repo, "revert", "--no-edit", "HEAD")
        require((repo / "README.md").read_text() == "team=base\n")
        git(repo, "merge-base", "--is-ancestor", old, "HEAD")
    print("PASS", mode, repo)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=MODES, nargs="?")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        for scenario in MODES:
            verify(scenario)
    elif args.scenario:
        folder = prepare(args.scenario)
        print("Practice folder:", folder)
        print('Set-Location "' + str(folder) + '"')
        print(git(folder, "status", "--short", "--branch").stdout)
    else:
        parser.error("Choose a scenario or --verify")
