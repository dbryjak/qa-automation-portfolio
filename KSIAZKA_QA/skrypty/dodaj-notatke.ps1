param(
    [string]$Tytul = "",
    [string]$Tresc = ""
)

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$journal = Join-Path $root "notatki\dziennik_2026.md"
$date = Get-Date -Format "yyyy-MM-dd HH:mm"

if (-not $Tytul) { $Tytul = Read-Host "Tytul notatki" }
if (-not $Tresc) {
    Write-Host "Tresc (zakoncz pusta linia + Enter dwa razy lub Ctrl+Z):"
    $lines = @()
    while ($true) {
        $line = Read-Host
        if ($line -eq "" -and $lines.Count -gt 0) { break }
        if ($line -ne "") { $lines += $line }
    }
    $Tresc = $lines -join "`n"
}

$entry = @"

## $date — $Tytul

$Tresc

---

"@

if (-not (Test-Path $journal)) {
    $header = @"
# Dziennik pracy QA — 2026

Automatycznie dopisywany przez ``dodaj-notatke.ps1``.

"@
    Set-Content -Path $journal -Value $header -Encoding UTF8
}

Add-Content -Path $journal -Value $entry -Encoding UTF8
Write-Host "Zapisano w: $journal" -ForegroundColor Green
