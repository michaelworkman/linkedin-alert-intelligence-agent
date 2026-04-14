#!/usr/bin/env bash

set -euo pipefail

MODE="${1:-}"
ROOT_DIR="${ROOT_DIR:-$(git rev-parse --show-toplevel)}"
STATE_REMOTE="${STATE_REMOTE:-origin}"
STATE_BRANCH="${STATE_BRANCH:-linkedin-digest-state}"
DATABASE_PATH="${DATABASE_PATH:-data/linkedin_alerts.sqlite3}"
BOT_NAME="${BOT_NAME:-github-actions[bot]}"
BOT_EMAIL="${BOT_EMAIL:-41898282+github-actions[bot]@users.noreply.github.com}"

if [[ -z "$MODE" ]]; then
  echo "Usage: $0 <restore|persist>" >&2
  exit 1
fi

STATE_WORKTREE_DIR=""

cleanup() {
  if [[ -n "$STATE_WORKTREE_DIR" && -d "$STATE_WORKTREE_DIR" ]]; then
    git -C "$ROOT_DIR" worktree remove --force "$STATE_WORKTREE_DIR" >/dev/null 2>&1 || rm -rf "$STATE_WORKTREE_DIR"
  fi
}

trap cleanup EXIT

remote_branch_exists() {
  git -C "$ROOT_DIR" ls-remote --exit-code --heads "$STATE_REMOTE" "$STATE_BRANCH" >/dev/null 2>&1
}

ensure_existing_branch_worktree() {
  git -C "$ROOT_DIR" fetch --no-tags "$STATE_REMOTE" "$STATE_BRANCH" >/dev/null 2>&1
  STATE_WORKTREE_DIR="$(mktemp -d)"
  git -C "$ROOT_DIR" worktree add --detach "$STATE_WORKTREE_DIR" FETCH_HEAD >/dev/null 2>&1
  git -C "$STATE_WORKTREE_DIR" switch -C "$STATE_BRANCH" >/dev/null 2>&1
}

ensure_new_branch_worktree() {
  STATE_WORKTREE_DIR="$(mktemp -d)"
  git -C "$ROOT_DIR" worktree add --detach "$STATE_WORKTREE_DIR" HEAD >/dev/null 2>&1
  git -C "$STATE_WORKTREE_DIR" switch --orphan "$STATE_BRANCH" >/dev/null 2>&1
  find "$STATE_WORKTREE_DIR" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
}

restore_state() {
  if ! remote_branch_exists; then
    echo "No state branch found at ${STATE_REMOTE}/${STATE_BRANCH}; starting with an empty database."
    return 0
  fi

  ensure_existing_branch_worktree

  if [[ ! -f "$STATE_WORKTREE_DIR/$DATABASE_PATH" ]]; then
    echo "State branch exists but ${DATABASE_PATH} is missing; starting with an empty database."
    return 0
  fi

  mkdir -p "$ROOT_DIR/$(dirname "$DATABASE_PATH")"
  cp "$STATE_WORKTREE_DIR/$DATABASE_PATH" "$ROOT_DIR/$DATABASE_PATH"
  echo "Restored ${DATABASE_PATH} from ${STATE_REMOTE}/${STATE_BRANCH}."
}

persist_state() {
  if [[ ! -f "$ROOT_DIR/$DATABASE_PATH" ]]; then
    echo "No ${DATABASE_PATH} file exists; nothing to persist."
    return 0
  fi

  if remote_branch_exists; then
    ensure_existing_branch_worktree
  else
    ensure_new_branch_worktree
  fi

  mkdir -p "$STATE_WORKTREE_DIR/$(dirname "$DATABASE_PATH")"
  cp "$ROOT_DIR/$DATABASE_PATH" "$STATE_WORKTREE_DIR/$DATABASE_PATH"
  cat >"$STATE_WORKTREE_DIR/README.md" <<'EOF'
# LinkedIn Digest State

This branch is maintained automatically by the weekday LinkedIn digest workflow.
It stores the SQLite state file used to keep digest history and dedupe context
between GitHub Actions runs.
EOF

  git -C "$STATE_WORKTREE_DIR" config user.name "$BOT_NAME"
  git -C "$STATE_WORKTREE_DIR" config user.email "$BOT_EMAIL"
  git -C "$STATE_WORKTREE_DIR" add README.md "$DATABASE_PATH"

  if git -C "$STATE_WORKTREE_DIR" diff --cached --quiet; then
    echo "No state changes to persist."
    return 0
  fi

  git -C "$STATE_WORKTREE_DIR" commit -m "Update LinkedIn digest state (${GITHUB_RUN_ID:-manual})" >/dev/null 2>&1
  git -C "$STATE_WORKTREE_DIR" push "$STATE_REMOTE" "HEAD:${STATE_BRANCH}" >/dev/null 2>&1
  echo "Persisted ${DATABASE_PATH} to ${STATE_REMOTE}/${STATE_BRANCH}."
}

case "$MODE" in
  restore)
    restore_state
    ;;
  persist)
    persist_state
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    echo "Usage: $0 <restore|persist>" >&2
    exit 1
    ;;
esac
