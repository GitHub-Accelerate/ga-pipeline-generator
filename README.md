# GitHub Actions Pipeline Generator

This project looks at the repository contents and generates a new specialized workflow for this specific repo.

Creating an access token: 

- Select fine _grained access token_
- Name it `GH_WORKFLOW_WRITE`
- Give it repo access to _Only select repositories_ and select the right repo
- Under Repository permissions, give it _read and write_ access to Contents
- Under Repository permissions, give it _read and write_ access to Workflows
