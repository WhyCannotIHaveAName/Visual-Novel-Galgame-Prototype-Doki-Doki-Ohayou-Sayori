param([Parameter(Mandatory = $true)][string]$Sdk, [string[]]$Stages = @('lint', 'update21', 'shortcut', 'routes', 'persistence', 'smoke'))
$ErrorActionPreference = 'Stop'
$projectPath = Split-Path $PSScriptRoot -Parent
$sdkPath = (Resolve-Path -LiteralPath $Sdk).Path
$enginePath = Join-Path $sdkPath 'lib\py3-windows-x86_64\python.exe'
$entryPath = Join-Path $sdkPath 'renpy.py'
$resultPath = Join-Path (Join-Path $projectPath 'qa-results') (Get-Date -Format 'yyyyMMdd-HHmmssfff')
New-Item -ItemType Directory -Force -Path $resultPath | Out-Null
# Ren'Py also writes game/saves even when its user save directory is redirected.
# Run a copied project so the author's local playthrough cannot be reset by QA.
$testProject = Join-Path $resultPath 'test-project'
$sourceGame = Join-Path $projectPath 'game'
$testGame = Join-Path $testProject 'game'
foreach ($sourceFile in Get-ChildItem -LiteralPath $sourceGame -Recurse -File) {
    $relativeFile = $sourceFile.FullName.Substring($sourceGame.Length + 1)
    if ($relativeFile -like 'saves\*' -or $relativeFile -like 'cache\*' -or $sourceFile.Extension -eq '.rpyc') { continue }
    $copiedFile = Join-Path $testGame $relativeFile
    New-Item -ItemType Directory -Force -Path (Split-Path $copiedFile -Parent) | Out-Null
    Copy-Item -LiteralPath $sourceFile.FullName -Destination $copiedFile
}
$previousSaves = $env:RENPY_PATH_TO_SAVES
$previousResults = $env:OHAYOU_QA_DIR
$env:RENPY_PATH_TO_SAVES = Join-Path $resultPath 'isolated-saves'
$env:OHAYOU_QA_DIR = $resultPath
try {
    foreach ($stage in $Stages) {
        $started = Get-Date
        $runArgs = if ($stage -eq 'lint') { @($entryPath, $testProject, 'lint') } else { @($entryPath, $testProject, 'test', $stage) }
        $resultText = (& $enginePath @runArgs 2>&1 | Out-String)
        $processExit = $LASTEXITCODE
        $resultText | Set-Content -LiteralPath (Join-Path $resultPath "$stage-output.txt") -Encoding utf8
        $newTrace = Get-Item -LiteralPath (Join-Path $testProject 'traceback.txt') -ErrorAction SilentlyContinue
        if ($processExit -ne 0 -or $resultText -match 'Full traceback:|assertion .* failed|uncaught exception|error detected|not loadable|not defined|is not a keyword' -or ($newTrace -and $newTrace.LastWriteTime -ge $started)) {
            throw "The $stage check failed. See $resultPath."
        }
        Write-Host "PASS: $stage"
    }
} finally {
    $env:RENPY_PATH_TO_SAVES = $previousSaves
    $env:OHAYOU_QA_DIR = $previousResults
}
