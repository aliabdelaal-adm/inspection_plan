# Smart auto-push script for plan-data.json (PowerShell version)
# Watches for changes and pushes only when actual updates occur

$File = "plan-data.json"
$Sleep = 30  # seconds
$LastHash = ""

function Get-FileHashString($path) {
    if (Test-Path $path) {
        return (Get-FileHash $path -Algorithm MD5).Hash
    } else {
        return ""
    }
}

$LastHash = Get-FileHashString $File

while ($true) {
    Start-Sleep -Seconds $Sleep
    $CurrentHash = Get-FileHashString $File
    if ($LastHash -ne $CurrentHash -and $CurrentHash -ne "") {
        Write-Host "Detected change in $File. Pushing to GitHub..."
        git add $File
        git commit -m "Auto-update plan-data.json"
        git push
        $LastHash = $CurrentHash
    } else {
        Write-Host "No change in $File. Monitoring..."
    }
}