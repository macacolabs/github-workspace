$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$errors = [System.Collections.Generic.List[string]]::new()

Write-Host '[1/4] Local links'
$htmlFiles = Get-ChildItem $repo -Recurse -Filter '*.html'
foreach ($file in $htmlFiles) {
    $content = Get-Content -Raw $file.FullName
    foreach ($match in [regex]::Matches($content, '(?:href|src)="([^"#]+)"')) {
        $ref = $match.Groups[1].Value
        if ($ref -match '^(https?:|mailto:|data:)') { continue }
        $target = Join-Path $file.DirectoryName $ref
        if (-not (Test-Path -LiteralPath $target)) {
            $errors.Add("Broken reference: $($file.FullName) -> $ref")
        }
    }
}

Write-Host '[2/4] SVG XML and accessibility'
$svgFiles = Get-ChildItem (Join-Path $repo 'assets\visuals') -Filter '*.svg'
foreach ($file in $svgFiles) {
    [xml]$svg = Get-Content -Raw $file.FullName
    if (-not $svg.svg.title -or -not $svg.svg.desc) {
        $errors.Add("SVG requires title and desc: $($file.Name)")
    }
}

Write-Host '[3/4] Java starter'
$javaSource = Join-Path $repo 'labs\team-profile-starter\src\HelloTeam.java'
$javac = Get-Command javac -ErrorAction SilentlyContinue
if ($javac) {
    $build = Join-Path ([System.IO.Path]::GetTempPath()) ('git-course-java-' + [guid]::NewGuid())
    New-Item -ItemType Directory -Path $build | Out-Null
    try {
        & $javac.Source -d $build $javaSource
        if ($LASTEXITCODE -ne 0) { $errors.Add('Starter Java compile failed') }
        $java = Get-Command java -ErrorAction SilentlyContinue
        if ($java) {
            $output = & $java.Source -cp $build HelloTeam
            if ($output -notmatch 'Team Profile') { $errors.Add('Starter Java output mismatch') }
        }
    } finally {
        Remove-Item -LiteralPath $build -Recurse -Force
    }
} else {
    Write-Host 'SKIP: javac not found'
}

Write-Host '[4/4] Git branch and conflict rehearsal'
$temp = Join-Path ([System.IO.Path]::GetTempPath()) ('git-course-flow-' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $temp | Out-Null
try {
    git -C $temp init -b main | Out-Null
    git -C $temp config user.name 'Course Validator'
    git -C $temp config user.email 'validator@example.invalid'
    Set-Content -LiteralPath (Join-Path $temp 'README.md') -Value 'team=base'
    git -C $temp add README.md
    git -C $temp commit -m 'docs: add team base' | Out-Null
    git -C $temp switch -c feature/student-a | Out-Null
    Set-Content -LiteralPath (Join-Path $temp 'README.md') -Value 'team=student-a'
    git -C $temp commit -am 'feat: add student a choice' | Out-Null
    git -C $temp switch main | Out-Null
    git -C $temp switch -c feature/student-b | Out-Null
    Set-Content -LiteralPath (Join-Path $temp 'README.md') -Value 'team=student-b'
    git -C $temp commit -am 'feat: add student b choice' | Out-Null
    git -C $temp merge feature/student-a 2>$null
    if ($LASTEXITCODE -eq 0) { $errors.Add('Expected merge conflict did not occur') }
    $status = git -C $temp status --short
    if ($status -notmatch '^UU README.md') { $errors.Add('Conflict status mismatch') }
    Set-Content -LiteralPath (Join-Path $temp 'README.md') -Value 'team=student-a+student-b'
    git -C $temp add README.md
    git -C $temp commit -m 'merge: resolve team choice conflict' | Out-Null
    if (git -C $temp status --porcelain) { $errors.Add('Repository not clean after conflict resolution') }
} finally {
    Remove-Item -LiteralPath $temp -Recurse -Force
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}
Write-Host "PASS: html=$($htmlFiles.Count) svg=$($svgFiles.Count) links, visuals, starter, conflict flow"

