"""Instructor QA for single-line lesson commands; never hides intermediate Git failures."""
import base64
import subprocess

def run(code, cwd=None, expected_failures=()):
    expected = list(expected_failures)
    lines = ["$ErrorActionPreference = 'Stop'"]
    for line in code.splitlines():
        lines.append(line)
        command = line.strip()
        if command.startswith('git '):
            if command in expected:
                expected.remove(command)
                lines.append('if ($LASTEXITCODE -eq 0) { throw "Expected Git failure did not occur" }')
            else:
                lines.append('if ($LASTEXITCODE -ne 0) { throw "Unexpected Git failure: stopped before next command" }')
    if expected:
        raise ValueError('Expected failure command missing from lesson: ' + repr(expected))
    encoded = base64.b64encode('\n'.join(lines).encode('utf-16le')).decode('ascii')
    result = subprocess.run(['powershell', '-NoProfile', '-EncodedCommand', encoded], cwd=cwd,
                            capture_output=True, text=True, errors='replace')
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout
