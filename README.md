# Blindless (Cursor / Grok Bot plugin)

Public marketplace package for the Blindless owner control plane.

- **MCP:** `https://blindless.ai/api/mcp`
- **Dashboard:** https://blindless.ai
- **Product code** (server + web) is private — this repo is the installable connector only.

## Install

1. Cursor Marketplace (when listed), or
2. Local: copy this folder to `~/.cursor/plugins/local/blindless/` and reload, or
3. Manual MCP URL: `https://blindless.ai/api/mcp`

## First run

Ask your bot: call Blindless `ensure_install`, save `install_id`, open the magic `open_url` on **blindless.ai**.

View-only: Blindless never sends email or SMS — actions stay in Grok Bot.
