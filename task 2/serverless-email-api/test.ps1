# test.ps1
$body = @{
    receiver_email = "your-email@gmail.com"  # Change this!
    subject = "Test Email from Serverless"
    body_text = "This is a test email sent from the serverless email API."
} | ConvertTo-Json

Write-Host "Sending request to API..." -ForegroundColor Yellow
Write-Host "Body: $body" -ForegroundColor Cyan

$response = Invoke-RestMethod -Uri "http://localhost:3000/dev/send-email" -Method POST -Body $body -ContentType "application/json"

Write-Host "`nResponse:" -ForegroundColor Green
$response | ConvertTo-Json -Depth 5