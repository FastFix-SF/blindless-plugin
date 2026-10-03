---
name: blindless-setup
description: Connect an AI host to Blindless, reuse the owner's board, and report real bot work, saved response drafts, and calendar changes. Use for Blindless setup or reporting recovery.
---

# Blindless setup (Grok Bot)

## Product locks

- Blindless organizes and monitors work. Board controls can assign or remove tasks; source actions such as sending email/SMS stay in the host.
- To request source work, copy the task prompt or open Grok Bot via its actual `app_url` / `web_url`.
- No Blindless `/setup` web page — connectors (Gmail, Calendar) are added in this chat.
- Magic links are one-time; redeem on `https://blindless.ai` (host-bound cookie). Never share bare `?install=` URLs.

## Connect and reuse

- Add the hosted MCP at `https://blindless.ai/api/mcp` and complete the host's browser authorization. Credentials belong in the host's secure connector store, never prompts or URLs.
- Call `get_connector_status` first. Its `install_id` is the board authorized by the owner; use it on every report. An install id alone is not authentication.
- Reuse the owner's existing bots and provider connections. Reading this skill is not a request to create bots, rename an existing bot, send mail, or edit a calendar. Provision foundation bots only when the owner requests setup and the host supports bot creation; reuse matching bots instead of duplicating them.
- For an owner dashboard link call `ensure_install` with that same id and send its one-time `open_url`. If the browser already has a board, authorize that board rather than creating a separate empty one. A read-only connection cannot mint owner links or write reports.
- Apply `reporting_rules` returned by `get_connector_status` or `ensure_install` to the existing fleet within the owner's requested scope. The server supplies the current contract; prefer it over remembered instructions.
- Connect missing Email/Calendar providers through the host. Report connected only after authorization succeeds; never ask for provider passwords or tokens.

## Keep boards alive

- **Bots list:** call `bot_checkin` with `id`, `name`, `role`, `status` (`working` | `idle` | `needs_you`), `doing_now`. Seeded roster without check-in stays invisible.
- **Start work:** `bot_checkin` with `status: working` and a short `doing_now`.
- **Activity:** use `report_bot_activity` for run start, meaningful progress, completion, failure, and approval pauses. Reuse the same `event_ref`, `occurred_at`, and content on retries. Verify through `list_bot_activity` before advancing a checkpoint. An activity completion does not finish a numbered task.
- **Open the right chat:** include the bot's real `app_url` / `web_url` when available. Never invent links.
- **Tasks:** use `list_tasks` / `get_task` before acting. Copying or opening the agent leaves a task Open. Call `report_task_progress` with `working` only when work actually starts; use `needs_you` when approval is required.
- **Draft review:** use `report_task_draft` for the complete saved response body, recipient, subject, actual provider draft URL, and stable `revision_ref`. This field deliberately stores the response draft; never substitute incoming email context or a summary. New content requires a new revision reference. Verify with `get_task`. Do not truncate drafts beyond the advertised limit; report the gap.
- **Finish:** use `post_task_proof` only for a real result, including the actual sent-email permalink when available. Then `bot_checkin` with the actual next state. Blindless never sends the email.
- **Files:** pass `library[]` metadata on check-in, including the real relative `folder_path` when known, or rely on automatic ingest append for Email/Calendar.
- A supplied `library[]` replaces the retained list (up to 40 items). Omit it on status-only check-ins. Never claim reporting succeeded if MCP returned an error.
- **Email → Tasks:** use `ingest_email_task` for actionable items, with account-qualified stable `message_ref` and the actual received-email link. Report saved responses separately through `report_task_draft`.
- **Calendar → Schedule:** use `ingest_calendar_stop` with stable account/calendar-qualified `event_ref`, local day/time, and real event URL. Reuse the reference for edits. Use `cancel_calendar_item` only after an authoritative source cancellation/deletion, never because an event is missing from a partial scan.

## Automatic reporting and recovery

- Blindless receives reports; it does not independently read Grok Bot, email, or calendars. Never claim continuous synchronization from a successful connection alone.
- Enumerate the host's currently authorized accounts at each reconciliation. Preserve pagination/delta checkpoints in host state. Call `report_sync_run` with `running` before each account scan, then `complete` only after all item writes were acknowledged, including zero-item scans. Missing access or unresolved writes require `failed` with a safe summary.
- Reuse `run_id` for retries of the same scan; use a new id for a new scan. Keep `account_ref` stable across reconnects. Retain item references and set `include_board_link: false` during bulk ingest.
- When the owner requests automatic updates, create a recurring reconciliation only if the host supports routines. State the actual cadence and limitations. Report Calendar writes immediately after source confirmation and reconcile later to catch missed reports.
- On failed or uncertain reporting, retain the work and retry with the same references. Inspect `get_connector_status` for failed, stalled, overdue, or unknown accounts. Never invent a successful scan or mark work done to conceal a reporting failure.

## Do not

- Put passwords, tokens, incoming mail bodies, file bytes, or private command contents in reporting fields. Saved response text belongs only in `report_task_draft`.
- Send mail/SMS from Blindless tools (they cannot).
- Invent sample data in production boards.
