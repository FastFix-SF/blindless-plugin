# Blindless (Cursor / Grok Bot plugin)

Public marketplace package for the Blindless owner control plane.

- **MCP:** `https://blindless.ai/api/mcp`
- **Dashboard:** https://blindless.ai
- **Product code** (server + web) is private — this repo is the installable connector only.

## Install

1. Cursor Marketplace (when listed), or
2. Local: copy this folder to `~/.cursor/plugins/local/blindless/` and reload, or
3. Manual MCP URL: `https://blindless.ai/api/mcp`

## Connect to your board

Complete the host's browser authorization. If you already use Blindless, open your existing board in that browser before connecting so the consent page selects the same board. Authorizing a new board creates a separate empty board.

Ask your bot:

> Connect to my Blindless board, call get_connector_status, reuse my existing bots, and follow its reporting_rules. Open my dashboard using ensure_install on that same board.

The owner approves the connector's board access. Each account authorizes its own connection. Credentials stay in the host connector store; never paste them into tasks, prompts, or URLs. Connections can be revoked from dashboard Settings.

## What appears on the board

- **Tasks:** reported work, actual response drafts, progress, and result links. Copying an instruction leaves a task Open. Real work reports move it to Active; a real proof completes it.
- **Bots:** checked-in bots, recent activity, chat links, and file metadata with folders. Stale status is shown as unconfirmed.
- **Schedule:** reported events, changes, and authoritative cancellations, preserving calendar-local dates and times.
- **Team:** shared board access; owner-private bots stay private.

Blindless does not read a host account or provider calendar by itself. Automatic updates require the host to execute the reporting rules and supported routines. Ask for the cadence you want; verify account scan receipts in Settings. Connection status alone is not evidence that every source item has synchronized.

## Reporting and troubleshooting

The packaged `blindless-setup` skill covers initial setup, saved drafts, account scans, retries, and recovery. The MCP server returns the current reporting contract through `get_connector_status`.

- **Empty board:** confirm the install id matches the owner's existing board, then check provider authorization and account scan receipts.
- **Missing event:** verify its calendar, local date, source reference, and acknowledged `ingest_calendar_stop` report. Draft/unsent source events can be reported without sending invitations.
- **Delayed updates:** check failed or overdue accounts; inspect whether the host routine is enabled. Reconcile with the same provider references to avoid duplicates.
- **Expired dashboard link:** ask for a fresh `ensure_install` link using the same board. Magic links are one-time and must be opened on `blindless.ai`.
- **Authorization failure:** reconnect through the host's normal OAuth flow. An install id is not a credential. Revoked access must be reapproved by the owner.

Saved response drafts are intentionally stored for owner review. Incoming email bodies, provider credentials, file contents, and command contents are not part of ordinary reporting. Keep report summaries brief and include only the information needed for the owner's board.

Current advertised limits include 100 items per read page, 8,000 characters per saved response body, and 40 retained file metadata entries per bot. Read the server's diagnostics for current limits and truncated-inventory flags.

Support and vulnerability reports: **sebastian@fastfix.ai**. Do not include credentials in a report.

## Package checks

Run `python -m pip install -r scripts/requirements.txt`, then `python scripts/validate_plugin.py`. GitHub Actions runs the same preflight on pushes and pull requests. This validates packaging; it does not certify provider uptime or end-to-end host synchronization.
