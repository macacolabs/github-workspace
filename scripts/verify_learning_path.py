"""Rehearse module 01 HTML commands in a copied starter; verify module 02 entry.
Run: python -B scripts/verify_learning_path.py. No existing repository is modified.
Inputs: learner HTML and starter. Outputs: PASS and preserved temporary folder.
"""
from html.parser import HTMLParser
from pathlib import Path
import shlex
import shutil
import tempfile
from zipfile import ZipFile
from recovery_lab import git, require

ROOT = Path(__file__).resolve().parents[1]
class Commands(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current = None
    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.current = ''
    def handle_data(self, text):
        if self.current is not None:
            self.current += text
    def handle_endtag(self, tag):
        if tag == 'pre' and self.current is not None:
            self.blocks.append(self.current)
            self.current = None

page = Commands()
page.feed((ROOT / 'labs/01-local-commits.html').read_text(encoding='utf-8-sig'))
repo = Path(tempfile.mkdtemp(prefix='git-learning-path-')) / 'student'
with ZipFile(ROOT / 'labs/team-profile-starter.zip') as starter:
    starter.extractall(repo)
git(repo, 'init', '-b', 'main')
git(repo, 'config', 'user.name', 'Path Test')
git(repo, 'config', 'user.email', 'path@example.invalid')
count = 0
for block in page.blocks:
    if 'git commit' not in block and 'git restore --staged' not in block:
        continue
    if 'git commit -m "docs: define team goal"' in block or 'git restore --staged' in block:
        # Simulate the explicit learner editing instructions before these commands.
        for name, text in [('README.md', '\nTeam goal refined.\n'), ('team.md', '\nTeam introduction revised.\n')]:
            with (repo / name).open('a', encoding='utf-8', newline='\n') as file:
                file.write(text)
    for line in block.splitlines():
        args = shlex.split(line)
        if args and args[0] == 'git':
            git(repo, *args[1:])
            count += 1
require(not git(repo, 'status', '--porcelain').stdout)
require(git(repo, 'ls-files', '.gitignore', 'members/.gitkeep').stdout.splitlines() == ['.gitignore', 'members/.gitkeep'])
clone = repo.parent / 'other-pc'
git(repo.parent, 'clone', str(repo), str(clone))
require((clone / '.gitignore').exists())
require(git(clone, 'check-ignore', '.env', '.env').returncode == 0)
git(repo, 'switch', '-c', 'feature/path-test')
require(not git(repo, 'status', '--porcelain').stdout)
print(f'PASS module01 HTML git commands={count}; clean module02 entry; clone ignore rules: {repo}')
