# Aurora P2P Discovery Server - CloudFormation Deployment Script (PowerShell)

param(
    [string]$Environment = "dev",
    [string]$Region = "us-east-1",
    [string]$StackName = "aurora-p2p-discovery"
)

$ErrorActionPreference = "Stop"

Write-Host "🐹 Aurora P2P Discovery Server Deployment" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host "Environment: $Environment"
Write-Host "Region: $Region"
Write-Host "Stack Name: $StackName"
Write-Host ""

$TemplateFile = "cloudformation.yaml"

# Validate template
Write-Host "Validating CloudFormation template..." -ForegroundColor Yellow
try {
    aws cloudformation validate-template `
        --template-body file://$TemplateFile `
        --region $Region
    Write-Host "✓ Template validation passed" -ForegroundColor Green
} catch {
    Write-Host "✗ Template validation failed" -ForegroundColor Red
    exit 1
}

# Check if stack exists
Write-Host "Checking if stack exists..." -ForegroundColor Yellow
try {
    aws cloudformation describe-stacks `
        --stack-name $StackName `
        --region $Region 2>$null
    $StackExists = $true
    $Action = "update-stack"
    Write-Host "Stack exists. Will update." -ForegroundColor Yellow
} catch {
    $StackExists = $false
    $Action = "create-stack"
    Write-Host "Stack does not exist. Will create." -ForegroundColor Yellow
}

# Deploy stack
Write-Host "Deploying CloudFormation stack..." -ForegroundColor Yellow
aws cloudformation $Action `
    --stack-name $StackName `
    --template-body file://$TemplateFile `
    --parameters ParameterKey=Environment,ParameterValue=$Environment `
    --capabilities CAPABILITY_NAMED_IAM `
    --region $Region `
    --tags Key=Project,Value=Aurora Key=ManagedBy,Value=CloudFormation

if ($Action -eq "create-stack") {
    Write-Host "Waiting for stack creation to complete..." -ForegroundColor Yellow
    aws cloudformation wait stack-create-complete `
        --stack-name $StackName `
        --region $Region
} else {
    Write-Host "Waiting for stack update to complete..." -ForegroundColor Yellow
    aws cloudformation wait stack-update-complete `
        --stack-name $StackName `
        --region $Region 2>$null
}

# Get outputs
Write-Host ""
Write-Host "✓ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Stack Outputs:" -ForegroundColor Green
aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' `
    --output table

# Save outputs to file
$OutputFile = "outputs-$Environment.json"
aws cloudformation describe-stacks `
    --stack-name $StackName `
    --region $Region `
    --query 'Stacks[0].Outputs' `
    --output json | Out-File -FilePath $OutputFile

Write-Host ""
Write-Host "Outputs saved to: $OutputFile" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 Aurora P2P Discovery Server is ready!" -ForegroundColor Green
