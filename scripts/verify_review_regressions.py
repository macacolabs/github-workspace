"""Regression checks for wrong-branch sync, settings drift, strict failures and ZIP state."""
from pathlib import Path
import tempfile
from checked_powershell import run
from recovery_lab import git, prepare, require

# Intermediate failure must not be hidden by a successful last command.
try:
    run('git --invalid-course-option\nWrite-Output SHOULD_NOT_RUN')
except RuntimeError:
    pass
else:
    raise RuntimeError('Intermediate Git failure was ignored')
try:
    run('git --version', expected_failures=('git --version',))
except RuntimeError:
    pass
else:
    raise RuntimeError('Expected failure unexpectedly succeeded')
print('PASS strict unexpected-failure and unexpected-success guards')

# Enter from a feature branch, then use the corrected main-only instructions.
repo = prepare('remote')
git(repo, 'stash', 'push', '-m', 'preserve exercise work')
git(repo, 'switch', '-c', 'feature/remote-practice')
git(repo, 'switch', 'main')
git(repo, 'pull', '--no-rebase', '--no-edit', 'origin', 'main')
git(repo, 'push', 'origin', 'main')
require(git(repo, 'rev-parse', 'HEAD').stdout == git(repo, 'rev-parse', 'origin/main').stdout)
require(git(repo, 'stash', 'list').stdout)
print('PASS feature to main synchronization with work preserved')

# Simulate inherited autoSetupRemote=true without touching real global settings.
repo = prepare('shared')
remote = repo.parent / 'target.git'
remote.mkdir()
git(remote, 'init', '--bare', '-b', 'main')
git(repo, 'remote', 'add', 'origin', str(remote))
git(repo, 'config', 'push.default', 'nothing')
git(repo, 'config', 'push.autoSetupRemote', 'false')
import os
old = dict(os.environ)
fake_global = repo.parent / 'test-global-config'
git(repo, 'config', '--file', str(fake_global), 'push.autoSetupRemote', 'true')
try:
    os.environ['GIT_CONFIG_GLOBAL'] = str(fake_global)
    require(git(repo, 'push', ok=False).returncode != 0)
finally:
    os.environ.clear()
    os.environ.update(old)
require(git(repo, 'push', ok=False).returncode != 0)
print('PASS explicit push-target exercise despite autoSetupRemote=true')

# Windows packaging/extraction preserves hidden .git, conflict index and reflog.
repo = prepare('conflict')
archive = repo.parent / 'case.zip'
target = repo.parent / 'received'
code = "Add-Type -AssemblyName System.IO.Compression.FileSystem\n"
code += f"[IO.Compression.ZipFile]::CreateFromDirectory('{repo}', '{archive}')\n"
code += f"[IO.Compression.ZipFile]::ExtractToDirectory('{archive}', '{target}')"
run(code)
require(git(repo, 'status', '--porcelain').stdout == git(target, 'status', '--porcelain').stdout)
require(git(repo, 'ls-files', '-u').stdout == git(target, 'ls-files', '-u').stdout)
require(git(repo, 'reflog', '--format=%H').stdout == git(target, 'reflog', '--format=%H').stdout)
print('PASS Windows ZIP transfer of conflict state')
