# 프로젝트 Git 상황 매트릭스

## 목적과 수업 배치

학생은 오류가 나면 명령을 복사하기 전에 **현재 위치 → 현재 브랜치 → 보존할 변경 → 원격 차이**를 확인한다.

- **MUST**: 4시간 수업에서 직접 재현·복구
- **DRILL**: 쉬는 시간과 프로젝트 중 10분 반복
- **REFERENCE**: 프로젝트 중 상황 대응 사전에서 찾아 수행
- `reset --hard`, `clean -fd`, `push --force`는 학생용 정답으로 제시하지 않는다.

## 공통 진단

```powershell
Get-Location
git rev-parse --show-toplevel
git branch --show-current
git status
git diff
git diff --staged
git remote -v
git branch -vv
git log --oneline --graph --decorate --all -12
```

전부 기계적으로 실행하지 않는다. 증상에 맞는 확인 명령을 고르고 조치 뒤 같은 명령으로 검증한다.

## 42개 프로젝트 상황

| ID | 단계 | 증상 | 먼저 확인 | 안전한 대응 | 피할 행동 | 배치 |
|---|---|---|---|---|---|---|
| S01 | 시작 | not a git repository | 위치, 저장소 최상위 | 올바른 폴더로 이동. 새 프로젝트일 때만 init | 아무 폴더에서 init 반복 | MUST |
| S02 | 시작 | clone과 init 혼동 | .git, remote | 원격 프로젝트는 clone, 새 로컬 프로젝트만 init | clone 폴더에서 재-init | DRILL |
| S03 | 시작 | 작업 전 변경이 남음 | status, diff | 주인·목적 확인 후 commit, branch, stash 선택 | 바로 pull/reset | MUST |
| S04 | 상태 | 파일이 status에 없음 | 위치, ignore | 경로와 ignore 규칙 확인 | 파일 재생성 반복 | DRILL |
| S05 | stage | 관계없는 파일 포함 | diff --staged | restore --staged 후 필요한 파일만 add | 작업 파일 삭제 | MUST |
| S06 | stage | ignore 후에도 표시 | ls-files | rm --cached 후 ignore commit | 로컬 원본 삭제 | DRILL |
| S07 | commit | 여러 목적이 한 commit | staged diff | 목적별 stage와 작은 commit | 큰 commit 그대로 PR | MUST |
| S08 | commit | 직전 로컬 commit 수정 | push 여부 | 미공유일 때만 amend | 공유 이력 무단 변경 | DRILL |
| S09 | branch | main에서 미commit 작업 | branch, status | 현재 위치에서 feature branch 생성 | 변경 폐기 | MUST |
| S10 | branch | main에 로컬 commit | push 여부, log | commit을 가리킬 rescue branch부터 생성 | 먼저 reset | MUST |
| S11 | branch | 다른 branch commit 필요 | hash, 대상 branch | 합의 후 cherry-pick, 실패 시 abort | branch 전체 merge | REFERENCE |
| S12 | branch | 전환이 변경을 덮는다고 거절 | status, diff | commit 또는 이름 있는 stash | discard changes | MUST |
| S13 | branch | detached HEAD 작업 | current branch, log | rescue branch로 commit 보존 | 바로 다른 commit 이동 | DRILL |
| S14 | remote | 첫 push upstream 없음 | branch -vv, remote | push -u origin 현재branch | main으로 대체 push | MUST |
| S15 | remote | non-fast-forward | fetch 후 graph | 원격 변경 확인 후 팀 방식으로 통합 | force push | MUST |
| S16 | remote | ahead/behind/diverged | status -sb, graph | commit 관계를 읽고 통합 방식 선택 | pull 반복 | MUST |
| S17 | remote | repository not found | remote, 브라우저 권한 | URL, 초대, 로그인 계정 확인 | 토큰 노출 | DRILL |
| S18 | remote | 다른 저장소로 push | remote -v | 확인 후 remote set-url | 계속 push | REFERENCE |
| S19 | remote | 원격 branch만 존재 | branch -a, fetch | switch --track origin/branch | 무관한 branch 생성 | REFERENCE |
| S20 | remote | 삭제 branch가 계속 보임 | branch -r | 협업 확인 후 fetch --prune | 사용 중 branch 삭제 | REFERENCE |
| S21 | conflict | 같은 줄 충돌 | status, marker | 의도 합의, 편집, add, test, commit | ours/theirs 무조건 선택 | MUST |
| S22 | conflict | modify/delete | status, name-status | 요구사항으로 유지/삭제 결정 | marker만 제거 | DRILL |
| S23 | conflict | add/add | 양쪽 내용 | 합치거나 이름 분리 후 실행 검증 | 한쪽 덮기 | REFERENCE |
| S24 | conflict | merge를 취소하고 싶음 | merge 상태 | 보존 확인 후 merge --abort | pull/merge 반복 | MUST |
| S25 | conflict | marker가 코드에 남음 | marker 검색 | 모두 제거 후 test와 status | 빌드 없이 commit | MUST |
| S26 | conflict | lock 파일 충돌 | manifest, 도구 버전 | 같은 도구로 재생성 | 숫자 손편집 | REFERENCE |
| S27 | PR | base branch 오류 | base/head, commits | base 변경 후 전체 diff 재확인 | 이상한 diff 리뷰 | MUST |
| S28 | PR | 관련 없는 commits | base 대비 log/diff | 깨끗한 branch로 필요한 commit만 이동 | 무시 요청 | DRILL |
| S29 | PR | 뒤처짐/conflict | checks, base 상태 | base 통합, 로컬 test, push | 웹에서 의미 없이 해결 | MUST |
| S30 | PR | Changes requested | 요청, diff | 작은 수정 commit, 재검증, 답변 | 대화만 resolve | MUST |
| S31 | PR | 보호 규칙/check 차단 | check 상세, 승인 수 | 원인 수정 또는 승인 대기 | 관리자 우회 | DRILL |
| S32 | 팀 | 같은 feature branch 공유 | 담당자, 범위 | 개인 branch 또는 명확한 인계 규칙 | 상대 위에 force push | MUST |
| S33 | 복구 | 미commit 변경 취소 | diff, 보존 여부 | 정말 불필요할 때만 restore file | 전체 restore | DRILL |
| S34 | 복구 | 공유 commit 취소 | push 여부 | revert로 반대 commit 생성 | shared reset | MUST |
| S35 | 복구 | commit/branch 분실 | reflog, hash | rescue branch로 먼저 보존 | 확인 전 작업 반복 | DRILL |
| S36 | 복구 | stash pop 충돌 우려 | stash list/show | apply, 검증, 명시적 drop | pop 반복 | REFERENCE |
| S37 | 보안 | secret commit/push | 원격 여부, 노출 범위 | 즉시 폐기·교체, 보고, 이력 정리 판단 | 파일 삭제만 수행 | MUST |
| S38 | 파일 | 큰 파일 push 거절 | 크기, 추적 여부 | 산출물 제외 또는 팀 승인 LFS | 이름 바꿔 재시도 | REFERENCE |
| S39 | Windows | 모든 줄이 변경 표시 | diff, gitattributes | 팀 줄바꿈 규칙과 별도 정규화 commit | 기능 변경과 혼합 | DRILL |
| S40 | Windows | 대소문자 rename 미반영 | status, 실제 경로 | 임시 이름을 거쳐 git mv 두 번 | 탐색기 rename 반복 | REFERENCE |
| S41 | 파일 | binary 충돌 | 소유자, 원본 | 기준본 선택 또는 양쪽 별도 보존 | 텍스트 병합 | REFERENCE |
| S42 | 정책 | force push 필요해 보임 | 공유 branch, graph | 중단하고 목표·상태·graph를 팀 공유 | shared branch force | MUST |

## 4시간 핵심 운영

| 블록 | 상황 | 관찰 가능한 결과 |
|---|---|---|
| 상태·commit | S01, S03, S05, S07 | status와 diff로 commit 범위 설명 |
| branch | S09, S10, S12 | 작업·commit을 잃지 않고 올바른 branch로 이동 |
| 원격·충돌 | S14~S16, S21, S24, S25 | push 거절과 conflict를 force 없이 해결 |
| PR·복구 | S27, S29, S30, S34, S37, S42 | 리뷰 반영, 공유 이력 복구, 안전 중단 판단 |

## 완료 기준

- 42개 상황에 증상, 확인, 안전 대응, 금지 행동이 있다.
- MUST 상황은 기존 실습 또는 상황 대응 사전에 연결된다.
- 학생 페이지에는 제출 입력란이 없다.
- 공유 이력, secret, force push에는 안전 중단 기준이 있다.
- Windows 줄바꿈·대소문자 문제를 포함한다.
- 링크, HTML, 모바일 폭, Java starter, Git 충돌 리허설이 통과한다.

## 공식 참고

- [Git status](https://git-scm.com/docs/git-status)
- [Git branch](https://git-scm.com/docs/git-branch)
- [Git switch](https://git-scm.com/docs/git-switch)
- [Git stash](https://git-scm.com/docs/git-stash)
- [Git reflog](https://git-scm.com/docs/git-reflog)
- [GitHub non-fast-forward](https://docs.github.com/en/get-started/using-git/dealing-with-non-fast-forward-errors)
- [GitHub 줄바꿈 설정](https://docs.github.com/en/get-started/getting-started-with-git/configuring-git-to-handle-line-endings)

