# Azure Environment Auditor

A Python-based Azure auditing tool that inventories resources in a Microsoft Azure environment, evaluates selected configuration details, and generates structured audit reports.

The project also includes GitHub Actions automation using OpenID Connect (OIDC) authentication with Microsoft Entra ID, allowing audits to run in the cloud without storing long-lived Azure credentials in GitHub.

> **Project Status:** Active development. This project will continue to expand as additional Azure services, auditing checks, reporting capabilities, and automation features are added.

## Features

- Authenticates to Microsoft Azure using `DefaultAzureCredential`
- Queries Azure Resource Groups
- Queries Azure Static Web Apps
- Converts Azure SDK responses into structured Python data
- Generates basic configuration findings
- Exports audit results to JSON during local execution
- Runs through GitHub Actions
- Uses OIDC federation for GitHub-to-Azure authentication
- Uses Azure RBAC with read-only permissions
- Limits public GitHub Actions output to non-sensitive audit summary data

## Architecture

```text
GitHub Actions
      ↓
OIDC Authentication
      ↓
Microsoft Entra ID
      ↓
Azure Reader RBAC
      ↓
Azure SDK for Python
      ↓
Azure Resource Manager
      ↓
Environment Audit
      ↓
Safe CI Summary
```

Local execution follows a slightly different path:

```text
Local Machine
      ↓
Azure CLI Authentication
      ↓
DefaultAzureCredential
      ↓
Azure SDK for Python
      ↓
Azure Resource Manager
      ↓
Detailed Audit
      ↓
Local JSON Report
```

## Technologies

- Python
- Microsoft Azure
- Azure SDK for Python
- Azure CLI
- Microsoft Entra ID
- Azure Resource Manager
- Azure RBAC
- OpenID Connect (OIDC)
- GitHub Actions
- Git
- JSON

## Project Structure

```text
Azure-Environment-Auditor/
├── .github/
│   └── workflows/
│       └── azure-audit.yml
├── azure_auth.py
├── checks.py
├── main.py
├── reporting.py
├── resources.py
├── static_web_apps.py
├── requirements.txt
└── reports/
```

## Example Output

The values below are examples and do not represent a real Azure environment.

```text
AZURE ENVIRONMENT AUDIT
==================================================
Resource Groups: 1
Static Web Apps: 1
Findings: 2

RESOURCE GROUPS
--------------------------------------------------
Name: example-resource-group
Location: westus2
Tags: {}

STATIC WEB APPS
--------------------------------------------------
Name: example-portfolio
Resource Group: example-resource-group
Location: westus2
SKU: Free
Hostname: example.azurestaticapps.net
Tags: {}

FINDINGS
--------------------------------------------------
[INFO] example-resource-group: Resource group has no tags
[INFO] example-portfolio: Static Web App has no tags
```

When the same auditor runs through GitHub Actions, the workflow intentionally prints only a limited summary:

```text
AZURE ENVIRONMENT AUDIT
==================================================
Resource Groups: 1
Static Web Apps: 1
Findings: 2
Audit completed successfully.
```

This prevents detailed Azure resource information from being exposed through public workflow logs.

## Installation

The auditor can be used against another Azure environment as long as the user has an Azure subscription and sufficient permissions to read the resources being queried.

### 1. Clone the Repository

```powershell
git clone https://github.com/RiceyPNW/Azure-Environment-Auditor.git
cd Azure-Environment-Auditor
```

### 2. Create a Python Virtual Environment

```powershell
python -m venv .venv
```

Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Authenticate with Azure CLI

Verify that Azure CLI is installed:

```powershell
az --version
```

Authenticate:

```powershell
az login
```

If browser authentication is unavailable:

```powershell
az login --use-device-code
```

Verify the active subscription:

```powershell
az account show
```

### 5. Configure the Subscription

Set the Azure subscription ID as an environment variable.

Windows PowerShell:

```powershell
$env:AZURE_SUBSCRIPTION_ID="YOUR_SUBSCRIPTION_ID"
```

Linux or macOS:

```bash
export AZURE_SUBSCRIPTION_ID="YOUR_SUBSCRIPTION_ID"
```

The subscription ID should not be hardcoded into the source code.

### 6. Run the Auditor

```powershell
python main.py
```

The application will query the configured Azure environment and display the detailed audit locally.

A JSON report will also be created at:

```text
reports/azure_report.json
```

Generated reports are excluded from Git.

## Local Authentication

The project uses `DefaultAzureCredential` from the Azure Identity SDK.

During local execution:

```text
Python Application
        ↓
DefaultAzureCredential
        ↓
Azure CLI Authentication
        ↓
Microsoft Entra ID
        ↓
Azure Resource Manager
```

This allows the application to use the Azure identity currently authenticated through Azure CLI.

## GitHub Actions Automation

The repository contains a GitHub Actions workflow that can execute the auditor using a temporary GitHub-hosted Linux runner.

The workflow:

1. Checks out the repository
2. Configures Python
3. Installs dependencies from `requirements.txt`
4. Authenticates to Azure using OIDC
5. Runs the Python auditor
6. Queries Azure using the Azure SDK
7. Prints a limited audit summary
8. Destroys the temporary runner when the workflow completes

The workflow currently runs when:

- Code is pushed to the `main` branch
- It is manually started with `workflow_dispatch`

## GitHub Actions Authentication

GitHub Actions does not use a stored Azure client secret.

Instead, the project uses workload identity federation:

```text
GitHub Actions
        ↓
GitHub OIDC Token
        ↓
Microsoft Entra ID
        ↓
Federated Credential Validation
        ↓
Azure Service Principal
        ↓
Azure RBAC
        ↓
Azure Resources
```

The Microsoft Entra federated credential is configured to trust the expected GitHub repository and branch.

Azure then authorizes the resulting identity using RBAC.

The current implementation uses the **Reader** role so the workflow can inspect Azure resources without receiving permission to modify or delete them.

## GitHub Repository Configuration

Someone using their own fork or copy of this project should create their own Microsoft Entra application and federated credential.

The general process is:

1. Create a Microsoft Entra App Registration
2. Add a GitHub federated credential
3. Configure the expected GitHub repository
4. Restrict the credential to the appropriate branch
5. Assign the Azure service principal the `Reader` role
6. Add the required values as GitHub repository secrets
7. Run the workflow

The workflow expects the following GitHub Actions secrets:

```text
AZURE_CLIENT_ID
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
```

These values should correspond to the user's own Azure environment.

No Azure client secret is required.

## Security

The project is designed to avoid storing long-lived Azure credentials in source control or GitHub Actions.

The GitHub workflow uses:

```yaml
permissions:
  id-token: write
  contents: read
```

This allows the workflow to request an OIDC identity token while keeping repository permissions limited.

Azure identifiers used by the workflow are stored as GitHub repository secrets so they are masked from workflow logs.

The workflow also intentionally avoids printing detailed resource information during GitHub Actions runs.

Detailed inventory output remains available during local execution.

### Files and Values That Should Not Be Committed

Do not commit:

- Azure client secrets
- Access tokens
- Deployment tokens
- Passwords
- API keys
- Authentication certificates
- Private keys
- `.env` files containing environment-specific values
- Generated audit reports containing infrastructure details

The `.gitignore` should include:

```gitignore
.venv/
__pycache__/
*.pyc
.env
reports/*.json
```

### Audit Data

Azure inventory data can reveal infrastructure details even when it does not contain passwords or tokens.

Depending on future features, reports may contain information such as:

- Resource names
- Hostnames
- Resource group names
- Locations
- Tags
- IP addresses
- Network configurations
- Azure resource IDs

For this reason, detailed reports are currently generated locally rather than uploaded through the public GitHub Actions workflow.

## Current Report Data

The current version can inspect:

- Resource Group names
- Resource Group locations
- Resource Group tags
- Static Web App names
- Associated Resource Groups
- Static Web App locations
- Static Web App SKU
- Static Web App hostnames
- Static Web App tags
- Basic configuration findings

The auditor stores selected properties rather than serializing complete Azure SDK responses.

## Current Scope

The current version focuses on a small Azure environment and establishes the foundation for a larger cloud auditing tool.

The architecture allows additional Azure resource collectors to be added independently as the project grows.

```text
Current
├── Resource Groups
└── Static Web Apps

Future
├── Virtual Machines
├── VNets
├── Subnets
├── Network Security Groups
├── Public IP Addresses
├── Storage Accounts
├── Container Apps
└── Container Registries
```

## Roadmap

This project is under continued development.

Planned and potential improvements include:

- Azure Virtual Machine inventory
- VNet and subnet inventory
- Network Security Group analysis
- Public IP exposure detection
- Storage account auditing
- Container Apps support
- Azure Container Registry support
- Severity-based configuration findings
- Security and configuration checks
- HTML report generation
- Environment health scoring
- Comparison between audit runs
- Scheduled audits
- Infrastructure change detection
- Sanitized reporting for CI/CD
- Additional GitHub Actions validation

## Version

### v1.0.0

Initial Azure Environment Auditor implementation featuring:

- Azure SDK resource inventory
- Resource Group collection
- Static Web App collection
- Structured Python reporting
- Local JSON export
- Basic configuration findings
- GitHub Actions automation
- OIDC authentication
- Microsoft Entra ID integration
- Azure Reader RBAC
- GitHub Secrets for environment identifiers
- Sanitized GitHub Actions logging

## Repository

```text
https://github.com/RiceyPNW/Azure-Environment-Auditor
```