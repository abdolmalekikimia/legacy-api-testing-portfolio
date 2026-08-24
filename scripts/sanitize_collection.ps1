param(
    [Parameter(Mandatory = $true)]
    [string]$Source
)

$ErrorActionPreference = "Stop"
$destination = Join-Path (Get-Location) "postman\complaint-test.sanitized.json"
$collection = Get-Content -LiteralPath $Source -Raw | ConvertFrom-Json

function Sanitize([object]$Value) {
    if ($null -eq $Value) { return $null }
    if ($Value -is [System.Management.Automation.PSCustomObject]) {
        $result = [ordered]@{}
        foreach ($property in $Value.PSObject.Properties) {
            $result[$property.Name] = Sanitize $property.Value
        }
        return [PSCustomObject]$result
    }
    if ($Value -is [System.Collections.IEnumerable] -and $Value -isnot [string]) {
        $result = @()
        foreach ($item in $Value) { $result += ,(Sanitize $item) }
        return $result
    }
    if ($Value -isnot [string]) { return $Value }

    $text = $Value
    $text = [regex]::Replace($text, '(?:(?:https?://)?(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[0-1])\.\d+\.\d+))(?::\d+)?', '{{base_url}}')
    $text = [regex]::Replace($text, '\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b', '{{api_token}}')
    $text = [regex]::Replace($text, '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', 'demo@example.test', 'IgnoreCase')
    $text = [regex]::Replace($text, '(?<!\d)(?:\+98|0098|0)?9\d{9}(?!\d)', '09120000000')
    $text = [regex]::Replace($text, '(?<!\d)\d{10}(?!\d)', '0000000000')
    $text = [regex]::Replace($text, '"password"\s*:\s*"[^"]*"', '"password": "{{password}}"', 'IgnoreCase')
    $text = [regex]::Replace($text, 'password=[^&"]+', 'password={{password}}', 'IgnoreCase')
    $text = [regex]::Replace($text, 'username=(?:real_user|pedram|chief_officer)', 'username={{username}}', 'IgnoreCase')
    $text = [regex]::Replace($text, 'authorizationCode=[^&"]+', 'authorizationCode={{authorization_code}}', 'IgnoreCase')
    return $text
}

New-Item -ItemType Directory -Force (Split-Path $destination) | Out-Null
(Sanitize $collection) | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $destination -Encoding UTF8
Write-Output "Wrote $destination"
