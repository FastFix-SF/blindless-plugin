---
name: blindless-setup
description: >-
  use this when setting up Blindless on a Grok Bot account, opening the owner
  dashboard, checking in bots, connecting Email/Calendar for Tasks/Schedule, or
  explaining Blindless view-only rules
---

# Blindless setup (Grok Bot)

## Product locks

- Blindless UI is **view / monitor only** — do not send email, SMS, or take actions from Blindless.
- Actions = copy-paste asks or open Grok Bot via `app_url` / `web_url`.
- No Blindless `/setup` web page — connectors (Gmail, Calendar) are added in this chat.
- Magic links are one-time; redeem on `https://blindless.ai` (host-bound cookie). Never share bare `?install=` URLs.

## First install

1. Call `ensure_install` (pass stored `install_id` if you have one; otherwise omit).
2. Store returned `install_id` on this bot.
3. Send the user the `open_url` magic link so they can open the cream dashboard.
4. Follow `next_setup_steps` for Email then Calendar (provider question → connector paste → `report_connection`).

## Keep boards alive

- **Bots list:** call `bot_checkin` with `id`, `name`, `role`, `status` (`working` | `idle` | `needs_you`), `doing_now`. Seeded roster without check-in stays invisible.
- **Start work:** `bot_checkin` with `status: working` and a short `doing_now`.
- **Standing rules:** install `reporting_rules` returned by `ensure_install` into every bot's standing instructions. Report at creation, run start, status changes, owner decisions (`needs_you`), and run finish. Report during long runs at least once per minute when the host supports it. Reuse the install id and each bot's stable id.
- **Open the right chat:** include the bot's real `app_url` / `web_url` when available. Never invent links.
- **Finish:** `post_task_proof` when a numbered task is done; then `bot_checkin` with `status: idle`.
- **Library:** pass `library[]` on check-in, or rely on `ingest_email_task` / `ingest_calendar_stop` append for Email/Calendar.
- A supplied `library[]` replaces the retained list (up to 40 items). Omit it on status-only check-ins. Never claim reporting succeeded if MCP returned an error.
- **Email → Tasks:** after email connected, `ingest_email_task` (metadata only, no body/tokens).
- **Calendar → Schedule:** after calendar connected, `ingest_calendar_stop`.

## Do not

- Put passwords, tokens, or mail bodies in MCP calls.
- Send mail/SMS from Blindless tools (they cannot).
- Invent sample data in production boards.
