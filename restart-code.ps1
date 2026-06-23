# restart-code.ps1
# Run this after install to ensure Claude Code picks up the new MCP config.
# Kills Claude Code (CLI) and ppt-mcp cleanly. Does not affect the Cowork desktop app.
# After running: reopen Claude Code manually.

$stopped = 0

# Kill ppt-mcp (all instances)
$pptmcp = Get-Process -Name "ppt-mcp" -ErrorAction SilentlyContinue
if ($pptmcp) {
    $pptmcp | Stop-Process -Force
    $stopped += $pptmcp.Count
    Write-Host "Stopped $($pptmcp.Count) ppt-mcp process(es)."
} else {
    Write-Host "ppt-mcp: not running."
}

# Kill Claude Code CLI only (AppData\Roaming path) — leaves Cowork desktop app untouched
$code = Get-Process -Name "claude" -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -like "*AppData*Roaming*Claude*claude-code*"
}
if ($code) {
    $code | Stop-Process -Force
    $stopped += $code.Count
    Write-Host "Stopped $($code.Count) Claude Code process(es)."
} else {
    Write-Host "Claude Code: not running."
}

if ($stopped -gt 0) {
    Write-Host "`nDone. Reopen Claude Code now, then test with 'ppt'."
} else {
    Write-Host "`nNothing was running. Open Claude Code and test with 'ppt'."
}
