"""Instructor QA: run preparation blocks from the instructor MD in isolated repos."""
from pathlib import Path
import re
from checked_powershell import run
from recovery_lab import git, require

root = Path(__file__).resolve().parents[1]
common = re.search(r'```powershell\n(.*?)\n```', (root / 'labs/recovery/git-markdown-practice.md').read_text(encoding='utf-8'), re.S).group(1)
blocks = re.findall(r'```powershell\n(.*?)\n```', (root / 'docs/independent-practice-instructor.md').read_text(encoding='utf-8'), re.S)
require(len(blocks) == 3)
for index, block in enumerate(blocks):
    code = common + '\n' + block + '\nWrite-Output ("REPO=" + $practiceRoot)'
    expected = [('git push',), ("git stash apply 'stash@{0}'",), ('git revert --no-edit cancel-target',)][index]
    output = run(code, expected_failures=expected)
    repo = Path(next(line[5:] for line in output.splitlines() if line.startswith('REPO=')).strip())
    if index > 0:
        archive, received = Path(str(repo) + '-case.zip'), Path(str(repo) + '-received')
        run("Add-Type -AssemblyName System.IO.Compression.FileSystem\n"
            + f"[IO.Compression.ZipFile]::CreateFromDirectory('{repo}', '{archive}')\n"
            + f"[IO.Compression.ZipFile]::ExtractToDirectory('{archive}', '{received}')")
        for args in [('status', '--porcelain'), ('ls-files', '-u'), ('stash', 'list'), ('reflog', '--format=%H')]:
            require(git(repo, *args).stdout == git(received, *args).stdout)
        if index == 2:
            require(git(repo, 'rev-parse', 'REVERT_HEAD').stdout == git(received, 'rev-parse', 'REVERT_HEAD').stdout)
        repo = received
        print('PASS remote ZIP state preserved', index + 1, flush=True)
    if index == 0:
        require(git(repo, 'push', ok=False).returncode != 0)
        git(repo, 'push', '-u', 'origin', 'main')
        require(git(repo, 'rev-parse', 'HEAD').stdout == git(repo, 'rev-parse', 'origin/main').stdout)
    elif index == 1:
        require('UU README.md' in git(repo, 'status', '--short').stdout)
        require(git(repo, 'stash', 'list').stdout)
        (repo / 'README.md').write_text('team=updated+unfinished\n', encoding='utf-8')
        git(repo, 'add', 'README.md')
        git(repo, 'commit', '-m', 'docs: preserve both intentions')
        require((repo / 'draft.md').read_text().strip() == 'draft=keep')
        require(git(repo, 'stash', 'list').stdout)
    else:
        require('UU README.md' in git(repo, 'status', '--short').stdout)
        git(repo, 'revert', '--abort')
        require((repo / 'README.md').read_text().strip() == 'team=approved')
        require(git(repo, 'revert', '--no-edit', 'cancel-target', ok=False).returncode != 0)
        (repo / 'README.md').write_text('team=approved\n', encoding='utf-8')
        git(repo, 'add', 'README.md')
        continued = git(repo, 'revert', '--continue', ok=False)
        if continued.returncode:
            diagnostic = (continued.stdout + continued.stderr).lower()
            require('empty' in diagnostic or 'nothing to commit' in diagnostic)
            require(not git(repo, 'diff', '--cached').stdout)
            require(not git(repo, 'ls-files', '-u').stdout)
            git(repo, 'revert', '--skip')
        git(repo, 'merge-base', '--is-ancestor', 'cancel-target', 'HEAD')
        require((repo / 'README.md').read_text().strip() == 'team=approved')
        require(not git(repo, 'status', '--porcelain').stdout)
    require(not git(repo, 'ls-files', '-u').stdout)
    print('PASS independent', index + 1, repo, flush=True)
