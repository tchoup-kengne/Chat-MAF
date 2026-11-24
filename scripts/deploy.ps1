param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroupName,
    [string]$Location = "eastus",
    [string]$AzureOpenAIEndpoint,
    [string]$AzureOpenAIChatModel,
    [string]$AzureOpenAIApiVersion = "2025-04-01-preview"
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($AzureOpenAIEndpoint)) {
    throw "Provide -AzureOpenAIEndpoint"
}
if ([string]::IsNullOrWhiteSpace($AzureOpenAIChatModel)) {
    throw "Provide -AzureOpenAIChatModel"
}

$unique = (Get-Random -Minimum 10000 -Maximum 99999)
$acrName = "chatmaf$unique"
$jobName = "chat-maf-job"
$imageName = "chat-maf"
$imageTag = "latest"

az group create --name $ResourceGroupName --location $Location | Out-Null
az acr create --resource-group $ResourceGroupName --name $acrName --sku Basic --admin-enabled false | Out-Null
az acr login --name $acrName | Out-Null

$acrServer = az acr show --name $acrName --query loginServer -o tsv
docker build -t "$acrServer/$imageName`:$imageTag" .
docker push "$acrServer/$imageName`:$imageTag"

$acrId = az acr show --name $acrName --query id -o tsv
$environmentName = "chat-maf-env"

az containerapp env create --name $environmentName --resource-group $ResourceGroupName --location $Location | Out-Null

az containerapp job create `
    --name $jobName `
    --resource-group $ResourceGroupName `
    --environment $environmentName `
    --image "$acrServer/$imageName`:$imageTag" `
    --registry-server $acrServer `
    --registry-identity system `
    --cpu 0.25 --memory 0.5Gi `
    --trigger-type Manual `
    --replica-timeout 300 `
    --replica-retry-limit 1 `
    --env-vars `
        AZURE_OPENAI_ENDPOINT=$AzureOpenAIEndpoint `
        AZURE_OPENAI_CHAT_MODEL=$AzureOpenAIChatModel `
        AZURE_OPENAI_API_VERSION=$AzureOpenAIApiVersion `
        CHAT_MAF_MESSAGE="What time is it in UTC?" `
    --system-assigned

Write-Host "Job created: $jobName"
Write-Host "Image: $acrServer/$imageName`:$imageTag"
