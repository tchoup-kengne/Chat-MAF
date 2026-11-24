# Chat-MAF

A Python console chatbot built with Microsoft Agent Framework and Azure OpenAI.

Features:

- Streaming assistant responses
- In-process conversation history
- Azure OpenAI API-key or `DefaultAzureCredential` authentication
- Automatic Agent Framework function-tool invocation
- Docker and Azure Container Apps Job deployment configuration

## Prerequisites

- Python 3.10 or later
- An Azure OpenAI resource and deployed chat model
- Azure CLI for Azure deployment

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Set these values in `.env`:

```dotenv
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
AZURE_OPENAI_CHAT_MODEL=<deployment-name>
AZURE_OPENAI_API_VERSION=2025-04-01-preview
# Optional; if omitted, Azure DefaultAzureCredential is used.
AZURE_OPENAI_API_KEY=
```

Authenticate locally with your Azure account when not using an API key:

```powershell
az login
```

Run the chatbot:

```powershell
python -m chat_maf
```

Type `exit`, `quit`, or `q` to end the session. Use `clear` to start a fresh
conversation.

The app can also run once, which is useful in Azure:

```powershell
$env:CHAT_MAF_MESSAGE = "What time is it in UTC?"
python -m chat_maf
```

## Run tests

```powershell
python -m pytest
```

## Azure deployment

The included script builds the container, pushes it to Azure Container Registry,
and creates or updates an Azure Container Apps Job.

```powershell
az login
.\scripts\deploy.ps1 -ResourceGroupName rg-chat-maf -Location eastus
```

The script uses Azure Managed Identity for Azure OpenAI access. Grant the job
identity the Azure OpenAI **Cognitive Services OpenAI User** role on the Azure
OpenAI resource.

Run the deployed job once:

```powershell
az containerapp job start --name chat-maf-job --resource-group rg-chat-maf --wait
```
