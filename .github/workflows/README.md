# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the nginx.org repository.

## Workflows

### 1. Deploy nginx.org (`build.yml`)
Deploys the nginx.org website to AWS staging or production environments.

**Triggers:**
- Push to any branch
- Manual workflow dispatch with environment selection

**Permissions:**
- `contents: read` - Read repository contents
- `id-token: write` - Write ID tokens for AWS authentication

### 2. Generate Markdown from XML (`generate-markdown.yml`)
Automatically regenerates markdown documentation files when XML sources are updated.

**Triggers:**
- Push to `master` or `main` branch when XML files or the converter script changes
- Pull requests that modify XML files or the converter script
- Manual workflow dispatch

**Behavior:**
- **On push to main/master:** Automatically commits and pushes updated markdown files
- **On pull request:** Creates a separate PR with the updated markdown files
- **Manual trigger:** Can be run manually from the Actions tab

**Permissions:**
- `contents: write` - Write repository contents to commit changes
- `pull-requests: write` - Create pull requests for PR-triggered runs

**What it does:**
1. Checks out the repository
2. Sets up Python 3.12
3. Runs `python3 tools/xml2md.py xml/ -o markdown/ --preserve-structure` to regenerate all markdown files
4. Checks if any markdown files were changed
5. If changes detected:
   - On push events: Commits and pushes changes directly
   - On PR events: Creates a new PR with the changes

**Note:** This workflow ensures that markdown files always stay in sync with their XML sources without manual intervention.

## Manual Workflow Execution

You can manually trigger the markdown generation workflow:

1. Go to the Actions tab in the GitHub repository
2. Select "Generate Markdown from XML" workflow
3. Click "Run workflow"
4. Select the branch to run on
5. Click "Run workflow" button

This is useful when you want to regenerate all markdown files without making changes to XML sources.
