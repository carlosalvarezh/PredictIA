# examples/scripts/test_predict.ps1
# Este script envía el JSON al endpoint /predict

$uri = "http://127.0.0.1:8000/predict"
$body = Get-Content -Raw -Path "..\payload_predict.json"
$response = Invoke-RestMethod -Uri $uri -Method Post -ContentType "application/json" -Body $body
$response | ConvertTo-Json -Depth 6
