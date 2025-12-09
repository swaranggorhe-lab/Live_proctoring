#!/usr/bin/env bash
# Usage:
# 1) If you have GitHub CLI: ./create_and_push_github.sh <repo-name>
# 2) Or set GITHUB_TOKEN and run: GITHUB_TOKEN=xxxx ./create_and_push_github.sh <repo-name>

set -euo pipefail
REPO_NAME=${1:-live-proctoring}
REMOTE_NAME=${2:-origin}
USER_REPO_URL="https://github.com/${REPO_NAME}.git"

echo "Preparing to push repository as public repo: ${REPO_NAME}"

if command -v gh >/dev/null 2>&1; then
  echo "Found gh CLI — creating repo via gh"
  gh repo create "$REPO_NAME" --public --source . --remote "$REMOTE_NAME" --push
  echo "Pushed via gh. URL: https://github.com/$(gh api user --jq .login)/${REPO_NAME}"
  exit 0
fi

if [ -z "${GITHUB_TOKEN:-}" ]; then
  cat <<EOF
Neither 'gh' CLI is available nor is GITHUB_TOKEN provided.
Please either:
  - Install and authenticate 'gh' (https://cli.github.com/) and re-run this script: 
      gh auth login
    then: ./create_and_push_github.sh ${REPO_NAME}
  - Or create a Personal Access Token on GitHub with 'repo' scope and run:
      GITHUB_TOKEN=YOUR_TOKEN ./create_and_push_github.sh ${REPO_NAME}
EOF
  exit 1
fi

# Create the repository via GitHub API
LOGIN=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/user | jq -r .login)
if [ -z "$LOGIN" ] || [ "$LOGIN" = "null" ]; then
  echo "Unable to read GitHub login from API. Check GITHUB_TOKEN." >&2
  exit 1
fi

# Create repo (idempotent if already exists will return message)
REPO_PAYLOAD=$(jq -n --arg name "$REPO_NAME" '{name: $name, private: false, auto_init: false}')
resp=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" -d "$REPO_PAYLOAD" https://api.github.com/user/repos)
repo_url=$(echo "$resp" | jq -r .html_url // empty)
if [ -n "$repo_url" ]; then
  echo "Created repo: $repo_url"
else
  echo "Repo might already exist or creation returned non-standard response. Continuing..."
fi

# Ensure git remote and push
git branch -M main
REMOTE_URL="https://github.com/${LOGIN}/${REPO_NAME}.git"
if git remote | grep -q "$REMOTE_NAME"; then
  git remote remove "$REMOTE_NAME"
fi
# Use HTTPS remote; user can change to SSH later
git remote add "$REMOTE_NAME" "$REMOTE_URL"
# Push
GIT_TERMINAL_PROMPT=0 git push -u "$REMOTE_NAME" main

echo "Pushed to: $REMOTE_URL"

echo "Done. If you want the repo under a different org or name, adjust arguments."