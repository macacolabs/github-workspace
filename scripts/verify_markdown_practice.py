"""Instructor-only regression check: execute the actual Markdown PowerShell blocks.
Students do not run this Python file. Run: python -B scripts/verify_markdown_practice.py
Creates isolated temporary repositories, preserves them, and never contacts GitHub.
"""
from pathlib import Path
from checked_powershell import run as powershell
import re
from recovery_lab import git, require

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'labs/recovery/git-markdown-practice.md').read_text(encoding='utf-8')
common = re.search(r'```powershell\n(.*?)\n```', text, re.S).group(1)

def content(repo, name):
    return (repo / name).read_text(encoding='utf-8-sig').strip()

for mode in ('staged', 'branch', 'committed', 'remote', 'conflict', 'delete-conflict', 'stash', 'lost', 'shared'):
    section = re.search(r'^## ' + re.escape(mode) + r'\n(.*?)(?=^## |\Z)', text, re.S | re.M).group(1)
    setup, recover = re.findall(r'```powershell\n(.*?)\n```', section, re.S)
    expected = {'branch': ('git switch main',), 'remote': ('git push',), 'conflict': ('git merge feature/a',), 'delete-conflict': ('git merge feature/a',)}.get(mode, ())
    output = powershell(common + '\n' + setup + '\nWrite-Output ("REPO=" + $practiceRoot)', expected_failures=expected)
    repo = Path(re.search(r'^REPO=(.+)$', output, re.M).group(1).strip())
    status = git(repo, 'status', '--short').stdout
    if mode == 'staged':
        require('MM README.md' in status and '?? draft.md' in status)
    if mode == 'branch':
        require(git(repo, 'branch', '--show-current').stdout.strip() == 'feature/profile')
        require(content(repo, 'README.md') == 'team=unfinished')
        require(git(repo, 'switch', 'main', ok=False).returncode != 0)
    if mode == 'remote':
        require(git(repo, 'push', ok=False).returncode != 0)
        git(repo, 'fetch', 'origin')
        require(git(repo, 'rev-list', '--left-right', '--count', 'HEAD...origin/main').stdout.strip() == '1\t1')
    if mode in ('conflict', 'delete-conflict'):
        require(('UU' if mode == 'conflict' else 'DU') + ' README.md' in status)
    if mode == 'lost':
        entries = git(repo, 'reflog', '--format=%H %gs').stdout.splitlines()
        found = next(line.split()[0] for line in entries if 'feat: detached work' in line)
        recover = recover.replace('찾은해시', found)
    powershell(recover, repo, expected_failures=('git merge feature/a',) if mode == 'conflict' else ())
    target = {'staged':'team=profile-v2', 'branch':'team=unfinished',
              'committed':'team=accidental-main', 'remote':'team=base',
              'conflict':'team=A+B', 'delete-conflict':'team=A',
              'stash':'team=base', 'lost':'team=lost-work', 'shared':'team=base'}[mode]
    require(content(repo, 'README.md') == target)
    require(not git(repo, 'ls-files', '-u').stdout)
    if mode in ('staged', 'stash'):
        require(content(repo, 'draft.md') == 'draft=keep')
        require(content(repo, 'notes.md') == ('note=unrelated' if mode == 'staged' else 'note=unfinished'))
    if mode == 'remote':
        require(content(repo, 'peer.md') == 'peer=keep' and content(repo, 'local.md') == 'local=keep')
        require(content(repo, 'notes.md') == 'note=unfinished')
        require(git(repo, 'rev-parse', 'HEAD').stdout == git(repo, 'rev-parse', 'origin/main').stdout)
    if mode == 'conflict':
        require(len(git(repo, 'rev-list', '--parents', '-n', '1', 'HEAD').stdout.split()) == 3)
    if mode == 'committed':
        require(git(repo, 'show', 'main:README.md').stdout.strip() == 'team=base')
    if mode == 'shared':
        git(repo, 'merge-base', '--is-ancestor', 'practice-shared-tip', 'HEAD')
    if mode in ('committed', 'conflict', 'delete-conflict', 'lost', 'shared'):
        require(not git(repo, 'status', '--porcelain').stdout)
    print('PASS markdown', mode, repo, flush=True)
