# 원격 독립 진단: 준비 상태 ZIP 전달

운영 확정안: 진행자가 D2/D3의 새 연습 저장소를 만들고 .git을 포함한 ZIP을 수업 채널로 전달한다.
학생은 압축을 새 폴더에 풀고 원인 이름이 없는 문제 카드만 받는다. 추가 프로그램 설치는 없다.
실제 수업 채널 전달과 학생 소요시간은 별도 리허설 대상이다.

## 범위와 안전

- 허용: 공통 준비로 만든 git-md-* 임시 폴더, 가상 작성자, README/notes/draft 문서, D2/D3 상태.
- 금지: 실제 프로젝트, 실명·이메일·토큰, 원격 URL, 실제 hooks·외부 경로를 포함하는 저장소.
- D1의 로컬 원격 경로는 PC마다 달라진다. 이 ZIP 방식으로 D1을 전달하지 않는다.
  D1은 오류 카드 기반 진단과 별도 안내형 실행으로 구분한다.
- Git clone은 미커밋 충돌·stash·reflog를 그대로 전달하지 않으므로 사용하지 않는다.
- PowerShell Compress-Archive는 숨김 항목 누락 가능성이 있어 사용하지 않는다.

## 진행자: 준비 직후 포장

D2 또는 D3 준비 후 $practiceRoot가 그 새 저장소를 가리키는지 확인한다.
Get-ChildItem -Force와 .git/config를 확인하고 학생에게 보여줄 문제만 남긴다.
생성기는 사용하지 않으며 아래 Windows 기본 .NET 압축 기능은 .git도 보존한다.

```powershell
Get-Location
Get-Content (Join-Path $practiceRoot '.git/config')
git -C $practiceRoot remote -v
# remote 출력은 없어야 한다. 실제 정보가 있으면 배포 중단.
Add-Type -AssemblyName System.IO.Compression.FileSystem
$caseZip = "$practiceRoot-case.zip"
[IO.Compression.ZipFile]::CreateFromDirectory($practiceRoot, $caseZip)
Get-FileHash $caseZip -Algorithm SHA256
```

내용을 미리 풀어 git status --short의 UU, D2의 stash 목록·draft,
D3의 REVERT_HEAD가 원래와 같은지 확인한 뒤 배포한다.
ZIP 파일명은 case-01.zip 등 중립적인 이름으로 바꾸고 문제의 원인명은 전달하지 않는다.
수업 채널에는 ZIP, SHA256, 학생 문제 카드 번호만 전달한다. 준비·정답 문서는 별도로 보관한다.

## 학생: 전달받은 파일 열기

진행자에게서 직접 받은 파일만 사용한다. 아래 경로를 실제 다운로드 경로로 바꾼다.
SHA256이 진행자가 알려준 값과 다르면 중단한다. 기존 작업 폴더에 덮어 풀지 않는다.

```powershell
$caseZip = "C:\Users\학생\Downloads\case-01.zip"
Get-FileHash $caseZip -Algorithm SHA256
# 일치 확인 후 다음 줄부터 실행
$caseRoot = Join-Path ([IO.Path]::GetTempPath()) ("git-case-" + [guid]::NewGuid())
Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::ExtractToDirectory($caseZip, $caseRoot)
Set-Location $caseRoot
Test-Path .git
Get-Location
git status
```

Test-Path가 True여야 한다. 상태가 문제 카드와 다르면 복구 명령을 실행하지 말고 진행자에게 알린다.
준비 문서를 열지 않은 상태에서 진단·선택·복구를 수행하고 화면 공유로 설명한다.
다시 연습할 때는 원본 ZIP을 새 고유 경로에 풀고 이전 작업은 남긴다.

## 판정

ZIP 전달은 독립 수행을 가능하게 하는 준비 방법일 뿐 학생 능력을 자동 판정하지 않는다.
준비나 정답을 봤다면 안내형으로 분류한다. 다른 조건 3회와 실제 팀 작업 1회는 별도 확인한다.
