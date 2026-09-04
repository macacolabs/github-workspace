# Git + Markdown 직접 실습

학생 필수: Git, 기본 텍스트 편집기. Windows에서는 기본 PowerShell을 사용합니다. 별도 언어 런타임이나 생성 스크립트는 필요하지 않습니다. HTML 교안은 설명·도식용이며 이 MD만 내려받아 시작 상태를 직접 만들 수도 있습니다.

## 안전하게 시작하기

각 시나리오는 아래 공통 준비를 먼저 새로 실행합니다. 실제 프로젝트에서는 실행하지 마세요. 현재 폴더를 먼저 기록하고 종료 후 돌아갑니다. 명령을 한 줄씩 실행하고, 명시한 예상 오류 외에는 멈추고 원인을 확인합니다. 새 창을 열거나 중간에 놓치면 기존 폴더를 삭제하지 말고 공통 준비부터 새 폴더를 만듭니다.

Set-Content는 지정 파일을 덮어씁니다. 이 안내에서는 새 연습 저장소의 파일에만 사용합니다. 직접 편집기로 같은 한 줄을 작성해도 됩니다. 영문 예시 내용은 쉘 인코딩 차이를 줄이기 위한 것입니다.

```powershell
# Windows PowerShell. 한 줄씩 실행하고 실패하면 멈춥니다.
$practiceRoot = Join-Path ([IO.Path]::GetTempPath()) ("git-md-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $practiceRoot -ErrorAction Stop
Set-Location $practiceRoot
git init -b main
git config user.name "Practice Student"
git config user.email "practice@example.invalid"
# 아래 설정은 이 새 연습 저장소에만 적용합니다.
git config commit.gpgsign false
git config core.autocrlf false
git config core.whitespace cr-at-eol
git config core.hooksPath .no-hooks
Set-Content README.md "team=base"
Set-Content notes.md "note=base"
git add README.md notes.md
git commit -m "docs: base"
git status --short
```

공통 준비 마지막 status 출력이 비어 있어야 합니다. 기본 커밋은 README.md와 notes.md를 기록합니다. 각 단계는 명령 실행 전 무엇이 달라질지 예측하고 실행 후 파일과 이력을 비교합니다.

## staged

공통 준비를 새로 실행한 다음 아래 명령을 실행합니다.

```powershell
Set-Content README.md "team=profile"
git add README.md
Set-Content README.md "team=profile-v2"
Set-Content notes.md "note=unrelated"
git add notes.md
Set-Content draft.md "draft=keep"
git status --short
```

예상 결과: MM README.md, 첫 열 M인 notes.md, ?? draft.md. add 시점과 현재 파일이 다릅니다.

### staged 복구 — 먼저 방법을 선택한 뒤 읽으세요

```powershell
git restore --staged notes.md
git add README.md
git commit -m "docs: profile only"
git show --stat HEAD
Get-Content README.md
Get-Content notes.md
Get-Content draft.md
git status --short
```

검증: 새 커밋은 README만 포함합니다. README는 profile-v2, notes는 unrelated, draft는 keep. 남은 수정과 새 파일 때문에 clean이 아니어야 합니다.

## branch

공통 준비를 새로 실행한 다음 아래 명령을 실행합니다.

```powershell
git switch -c feature/profile
Set-Content README.md "team=feature"
git add README.md
git commit -m "feat: profile"
Set-Content README.md "team=unfinished"
# 이 전환은 덮어쓰기 위험 때문에 거절되어야 합니다.
git switch main
git status --short
```

예상 결과: main 전환이 거절되고 feature/profile에 남습니다. README의 unfinished 내용은 보존됩니다.

### branch 복구 — 먼저 방법을 선택한 뒤 읽으세요

```powershell
git stash push -m "profile WIP"
git switch main
Get-Content README.md
git switch feature/profile
git stash apply 'stash@{0}'
Get-Content README.md
git stash list
```

검증: main에서는 base, feature로 돌아와서는 unfinished. stash 항목도 남습니다. apply 실패 시 반복하거나 drop하지 말고 상태를 확인합니다.

## committed

공통 준비를 새로 실행한 다음 아래 명령을 실행합니다.

```powershell
git tag practice-base
Set-Content README.md "team=accidental-main"
git add README.md
git commit -m "feat: committed on wrong branch"
git log --oneline --decorate -2
```

예상 결과: main의 새 커밋과 그 부모의 practice-base가 보입니다. 아직 공유하지 않은 상태입니다.

### committed 복구 — 먼저 방법을 선택한 뒤 읽으세요

```powershell
git switch -c feature/rescued
# 오직 이 미공유 연습 main에만 적용합니다. feature가 현재 끝 커밋을 보존합니다.
git branch -f main practice-base
git show main:README.md
git show feature/rescued:README.md
git status
```

검증: main은 base, feature/rescued는 accidental-main. clean 상태이며 원래 커밋은 feature가 보존합니다.

## remote

공통 준비를 새로 실행한 다음 아래 명령을 실행합니다.

```powershell
# 같은 PC의 두 폴더가 학생과 동료 PC 역할을 합니다.
# 원격과 동료 폴더도 고유한 경로를 사용합니다.
$remotePath = "$practiceRoot-remote.git"
$peerPath = "$practiceRoot-peer"
git init --bare -b main $remotePath
git remote add origin $remotePath
git push -u origin main
git clone $remotePath $peerPath
git -C $peerPath config user.name "Practice Peer"
git -C $peerPath config user.email "peer@example.invalid"
git -C $peerPath config commit.gpgsign false
git -C $peerPath config core.hooksPath .no-hooks
Set-Content (Join-Path $peerPath peer.md) "peer=keep"
git -C $peerPath add peer.md
git -C $peerPath commit -m "docs: peer update"
git -C $peerPath push
Set-Content local.md "local=keep"
git add local.md
git commit -m "docs: local update"
Set-Content notes.md "note=unfinished"
# 동료가 먼저 push했으므로 아래 push는 거절되어야 합니다.
git push
git status --short
```

예상 결과: push가 거절됩니다. fetch 후 HEAD...origin/main의 양쪽 전용 커밋 수는 각각 1입니다. notes.md 변경은 남습니다.

### remote 복구 — 먼저 방법을 선택한 뒤 읽으세요

```powershell
git stash push -m "local WIP"
git fetch origin
git rev-list --left-right --count HEAD...origin/main
git merge --no-edit origin/main
git push
git stash apply 'stash@{0}'
Get-Content notes.md
Get-Content peer.md
Get-Content local.md
git status --short
```

검증: 비교는 1 1, 통합 뒤 양쪽 파일이 남고 notes는 unfinished. 원격에는 미완성 notes를 올리지 않습니다.

## conflict

공통 준비를 새로 실행한 다음 아래 명령을 실행합니다.

```powershell
git switch -c feature/a
Set-Content README.md "team=A"
git add README.md
git commit -m "docs: A"
git switch main
git switch -c feature/b
Set-Content README.md "team=B"
git add README.md
git commit -m "docs: B"
# 같은 줄을 다르게 수정했으므로 충돌이 나야 합니다.
git merge feature/a
git status --short
```

예상 결과: UU README.md. feature/b에서 병합이 진행 중이며 아직 병합 커밋은 없습니다.

### conflict 복구 — 먼저 방법을 선택한 뒤 읽으세요

```powershell
git merge --abort
git status
# 다시 같은 병합을 하면 충돌이 발생합니다.
git merge feature/a
# 양쪽 내용을 모두 유지하기로 합의한 경우에만 다음 문장으로 편집합니다.
Set-Content README.md "team=A+B"
git add README.md
git diff --staged
git diff --check
git commit -m "merge: agree team"
git ls-files -u
git log -1 --format='%h %p %s'
Get-Content README.md
```

검증: README는 A+B, ls-files -u는 비어 있고 최신 커밋의 부모는 2개입니다.

## delete-conflict

공통 준비를 새로 실행한 다음 아래 명령을 실행합니다.

```powershell
git switch -c feature/a
Set-Content README.md "team=A"
git add README.md
git commit -m "docs: A"
git switch main
git switch -c feature/b
git rm README.md
git commit -m "docs: B"
# 한쪽 삭제와 다른 쪽 수정이 충돌합니다.
git merge feature/a
git status --short
```

예상 결과: DU README.md. 현재 쪽은 삭제, 상대 쪽은 수정했습니다. 파일을 유지할지 팀의 판단이 필요합니다.

### delete-conflict 복구 — 먼저 방법을 선택한 뒤 읽으세요

```powershell
# 팀이 문서를 유지하기로 합의했다고 가정합니다.
Get-Content README.md
git add README.md
git commit -m "merge: retain team description"
git ls-files -u
git status
```

검증: README는 A, 미해결 index 항목이 없고 clean입니다. 삭제가 제품 요구사항이면 임의로 이 답을 적용하지 않습니다.

## stash

공통 준비를 새로 실행한 다음 아래 명령을 실행합니다.

```powershell
Set-Content notes.md "note=unfinished"
Set-Content draft.md "draft=keep"
git status --short
```

예상 결과: 수정된 notes.md와 ?? draft.md. 새 파일도 보존 대상입니다.

### stash 복구 — 먼저 방법을 선택한 뒤 읽으세요

```powershell
git stash push -u -m "profile WIP"
git stash list
git stash show -u -p 'stash@{0}'
git stash apply 'stash@{0}'
Get-Content notes.md
Get-Content draft.md
# 두 파일이 원래 내용으로 돌아왔는지 확인한 뒤에만 drop합니다.
git stash drop 'stash@{0}'
git status --short
```

검증: notes는 unfinished, draft는 keep. 보존 확인 후에만 stash를 삭제하며 작업 파일의 변경은 남습니다.

## lost

공통 준비를 새로 실행한 다음 아래 명령을 실행합니다.

```powershell
git switch --detach HEAD
Set-Content README.md "team=lost-work"
git add README.md
git commit -m "feat: detached work"
git switch main
git reflog -5
```

예상 결과: 현재 main에는 lost-work 커밋이 안 보이지만 reflog에는 detached 작업이 남습니다.

### lost 복구 — 먼저 방법을 선택한 뒤 읽으세요

```powershell
git reflog --format='%H %gs'
# 위 출력에서 feat: detached work에 해당하는 해시를 직접 찾습니다.
# 아래 두 명령의 찾은해시는 그 실제 값으로 바꿉니다.
git show 찾은해시
git switch -c rescue/recovered 찾은해시
Get-Content README.md
```

검증: 구조 브랜치에서 README는 lost-work입니다. reflog는 미커밋 변경의 백업이 아니며 보관 기간도 영구가 아닙니다.

## shared

공통 준비를 새로 실행한 다음 아래 명령을 실행합니다.

```powershell
Set-Content README.md "team=wrong"
git add README.md
git commit -m "docs: wrong value"
# 공유됐다고 가정한 커밋에 표시만 붙입니다. 네트워크 전송은 없습니다.
git tag practice-shared-tip
git log --oneline --decorate -2
```

예상 결과: README는 wrong, practice-shared-tip은 잘못된 커밋을 가리킵니다. 실제 공유 없이 revert 판단을 연습합니다.

### shared 복구 — 먼저 방법을 선택한 뒤 읽으세요

```powershell
git revert --no-edit HEAD
Get-Content README.md
git merge-base --is-ancestor practice-shared-tip HEAD
$LASTEXITCODE
git log --oneline -3
```

검증: README는 base, 조상 검사 종료 코드는 0. wrong 커밋을 지우지 않고 취소 커밋을 추가했습니다.

## 복구 성공 확인

상태·브랜치·공유 여부 진단 → 보존 대상 확인 → 복구 선택 → 파일 내용·이력 검증 순서입니다. 상세 원리와 해결 절차는 같은 폴더의 HTML 교안에서 확인하세요. 오류가 사라졌다는 사실만으로 성공으로 판단하지 않습니다. 미완성 작업 복원 뒤에는 변경이 남는 것이 정상입니다. 기본 파일 내용은 `Get-Content`, stage 범위는 `git diff --staged`, 미해결 충돌은 `git ls-files -u`, 이력은 `git log --oneline --graph --all`로 확인합니다.
