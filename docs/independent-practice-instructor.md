# 독립 진단 실습: 진행자 준비와 판정

학생 페이지: labs/recovery/07-independent.html. 이 문서는 학생에게 먼저 펼쳐 주지 않는다.
학생은 Git과 Markdown만 사용한다. 기존 git-markdown-practice.md의 공통 준비를 사용한다.
각 문제는 새로운 연습 폴더에서 준비한다. 실제 프로젝트·실제 비밀정보 사용 금지.
원격 D2/D3는 [ZIP 전달 운영안](remote-diagnosis-handoff.md)으로 준비 상태를 전달한다. D1은 오류 카드 진단과 안내형 실행을 구분한다.
원격이라면 학생이 준비 명령을 보게 되는 경우는 안내형으로 분류하고 독립 진단 PASS로 세지 않는다.
숨겨진 준비가 불가능하면 오류 출력 카드로 가설·확인 순서를 평가하되 실제 복구 수행과 구분한다.

## D1: push 실패, 원인은 비공개

아래 중 하나를 무작위 선택한다. 학생에게 유형명을 알리지 않는다.

- A: 기존 MD의 remote 상황. 별도로 `Set-Content draft.md "draft=keep"`를 실행한다.
  양쪽 커밋 통합과 notes.md·draft.md 보존이 목표. stash -u 등의 선택 근거를 확인한다.
- B: 공통 준비 후 아래 블록. 원격에는 쓰기 가능한 bare 저장소가 있지만 upstream이 없으며, 명시하지 않은 push를 거부하도록 연습 저장소에 설정한다.

```powershell
$remotePath = "$practiceRoot-upstream.git"
git init --bare -b main $remotePath
git remote add origin $remotePath
git config push.default nothing
git config push.autoSetupRemote false
git push
```

마지막 push는 push.default=nothing에 따라 전송 대상 미지정으로 실패해야 한다. 자동 upstream 설정이 켜진 PC에서도 같은 실패를 재현한다. URL·브랜치·권한 확인 후 `git push -u origin main`이 가능하다.
성공 후 `git branch -vv`와 `git rev-parse HEAD origin/main`으로 연결과 이력 일치를 확인한다.

- C: 실제 권한을 바꾸지 않고 아래 오류 카드를 제공한다.
  `remote: Permission to classroom/team.git denied to student-b.`
  `fatal: unable to access 'https://github.com/classroom/team.git/': The requested URL returned error: 403`
  이는 교육용 출력이며 실제 서버 관측값이 아니다. URL·로그인 계정·접근권한 확인을 제안하고 담당자에게 요청하면 통과.
  403만으로 비밀번호 오류라고 단정하거나 force push를 제안하면 재진단한다. 인증서 검증 해제 금지.

## D2: 임시 보관을 되살리다가 실패

공통 준비 후 실행한다. 마지막 apply는 충돌이 예상된다.

```powershell
Set-Content README.md "team=unfinished"
Set-Content draft.md "draft=keep"
git stash push -u -m "profile WIP"
Set-Content README.md "team=updated"
git add README.md
git commit -m "docs: updated requirement"
git stash apply 'stash@{0}'
```

학생 목표: updated와 unfinished의 의도를 함께 반영한 문서, draft 보존, 검증 전 stash 삭제 금지.
`git status`, `git stash list`, `git stash show -u -p 'stash@{0}'`, 파일 내용으로 진단한다.
합의 문장을 `team=updated+unfinished`로 결정하고 README를 편집·add한 뒤 commit한다.
stash apply는 진행 중인 merge가 아니므로 merge --abort를 일반 해법으로 안내하지 않는다.
완료: README 내용 일치, draft=keep, 미해결 index 없음, stash 항목 유지. drop은 검증 후 선택.

## D3: 공유 커밋 취소 도중 실패

공통 준비 후 실행한다. 마지막 revert는 충돌이 예상된다.

```powershell
Set-Content README.md "team=wrong"
git add README.md
git commit -m "docs: wrong value"
git tag cancel-target
Set-Content README.md "team=approved"
git add README.md
git commit -m "docs: later approved change"
git revert --no-edit cancel-target
```

공유 여부는 실제 전송이 아닌 가정이다. 목표: 잘못된 변경은 취소하되 나중에 승인된 approved 문장은 유지.
학생이 판단 근거가 부족하다고 하면 `git revert --abort`와 팀 확인도 정상적인 안전 선택이다.
계속하기로 합의하면 README를 team=approved로 편집하고 add 후 `git revert --continue`.
최종 내용이 기존 HEAD와 같아 빈 취소가 될 수 있다. 빈 작업 안내가 나오면 status 확인 후
`git revert --skip`으로 작업을 마무리한다. 새 커밋 개수만으로 통과를 판정하지 않는다.
완료: approved 보존, 기존 두 커밋이 이력에 남음, 진행 중 revert와 미해결 항목 없음.

## 시간과 힌트

- 1회 10~15분: D1 하나 또는 D2 하나. D3는 15~20분 심화.
- 안내형: 준비·해결을 함께 시연한다.
- 제한 힌트형: 학생 페이지의 접힌 힌트 1까지만 제공한다.
- 독립형: 카드와 저장소만 전달한다. 힌트 2를 봤다면 연습 성공으로 기록하되 독립 PASS와 구분한다.
- 다른 조건 3회 성공 및 실제 팀 작업 1회 관찰 후 독립 수행 판정.

## 반복 협업: 실제 GitHub 수업용 저장소

A/B가 기존 MD 팀 프로젝트를 clone한다. 원격 권한 확인 후 아래 라운드를 순서대로 진행.
1. A가 feature/contact에서 team.md에 연락 규칙을 추가하고 PR. B는 문장 모호성을 리뷰.
2. A가 수정하는 동안 B는 별도 feature/meeting으로 같은 문장의 회의 규칙 변경을 PR하고 A 승인 후 병합.
3. A는 자신의 리뷰 수정 커밋을 만든 뒤 fetch, origin/main을 자신의 feature로 병합.
4. 충돌이면 문장을 합의해 해결. README·team.md 내용과 diff를 재검토하고 push.
5. B가 새 diff를 재리뷰하고 승인한 뒤 병합. 두 학생 모두 main 최신화와 내용 일치를 확인.
6. 역할을 바꿔 다른 문장으로 반복. 각자 브랜치와 원격 변경을 먼저 진단한다.

팀당 25~35분, 기존 4시간에 추가로 숨겨 넣지 않는다. 혼자 로컬 bare로 수행하면 기술 연습이며 실제 리뷰 통과가 아니다.
승인·병합·권한 변경은 수업용 저장소에서만 한다. 제출 문서나 별도 입력란은 요구하지 않는다.
