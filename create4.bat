@echo off
set GITHUB_TOKEN=github_pat_11BKSINYA0iMS7dxTSBkhx
set GITHUB_TOKEN2=_ZxpOWCSWzO3hjwqRwDEPtRQQE9cm8ZvlgyytZsNL9mrMRVDAT5N8sQtoYWq
set REPO_OWNER=philifandem
set REPO_NAME=mando

set WORKFLOW_FILE=revisio4.yml

curl -X POST -H "Accept: application/vnd.github.v3+json" ^
-H "Authorization: token %GITHUB_TOKEN%%GITHUB_TOKEN2%" ^
https://api.github.com/repos/%REPO_OWNER%/%REPO_NAME%/actions/workflows/%WORKFLOW_FILE%/dispatches ^
-d "{\"ref\":\"main\"}"

pause
