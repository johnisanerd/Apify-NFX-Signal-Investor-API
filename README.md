# NFX Signal Investor API: find investors, check sizes, and VC firms

Python and MCP examples for the [NFX Signal Investor API](https://apify.com/johnvc/nfx-signal-investor-api?fpr=9n7kx3) on Apify. It turns [Signal by NFX](https://signal.nfx.com) investor lists into structured JSON: venture investors, the VC firms behind them, and the check size each investor actually writes.

Not affiliated with, endorsed by, or connected to NFX. It reads the same public investor lists any visitor can browse.

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/hqdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Text walkthrough

If you have ever searched for how to find investors for a startup, the hard part is not finding names, it is finding the right names with the right cheque size. This API starts from the public Signal NFX investor lists: 349 of them, spanning 103 sectors and four stages from pre-seed to Series B. Run `mode: "lists"` first and you get the whole catalog with a slug, a stage, a sector, and an investor count for each one. Pick the slugs that match your round, pass them as `listSlugs` with `mode: "investors"`, and every row comes back with the investor's name, position, firm, profile link, investment locations, and the min, target, and max investment they write. Switch to `mode: "firms"` and the same list gives you a list of VC firms instead, which is the shape you want for a CRM import. Turn on `enrichWithLinkedIn` or `enrichWithCrunchbase` and each unique firm also picks up industry, size, funding, rank, and status. No login, cookie, or token for the source is needed, because these are the public lists.

## Quick start (Python + uv)

```bash
git clone https://github.com/johnisanerd/Apify-NFX-Signal-Investor-API.git
cd Apify-NFX-Signal-Investor-API
cp .env.example .env      # paste your Apify token
uv sync
uv run nfx-signal-investor-api-example.py
```

Get a free Apify account and API token: https://apify.com?fpr=9n7kx3

## Features

- Investors with **check sizes** (min, target, max in USD), position, firm, and profile links
- A **list of VC firms** per sector or geography, deduplicated and ready to import
- The full **VC database** catalog: 349 lists across 103 sectors and four stages
- Optional **LinkedIn and Crunchbase firm enrichment** in the same run
- Cursor pagination that walks an entire list, with `maxItems` to cap a run
- Pay per result, so scraping a small test list stays cheap

## Input parameters

| Field | Type | Default | Description |
|---|---|---|---|
| `mode` | string | `investors` | `investors`, `firms`, or `lists`. |
| `listSlugs` | array | none | List slugs to pull, e.g. `fintech-seed`. Required for `investors` and `firms`. |
| `maxItems` | integer | `0` | Cap on rows returned. `0` means no limit. |
| `pageSize` | integer | `50` | Investors requested per API page. |
| `includeFirms` | boolean | `false` | In `investors` mode, also emit one row per firm. |
| `stage` | string | none | Filter the catalog: `pre_seed`, `seed`, `series_a`, `series_b`. |
| `locationId` | string | none | Location tag filter for `lists` mode. |
| `enrichWithLinkedIn` | boolean | `false` | Add LinkedIn firmographics to each firm. |
| `enrichWithCrunchbase` | boolean | `false` | Add Crunchbase data to each firm. |

## Output fields

`result_type` tells you the row kind: `investor`, `firm`, `list`, or `error`.

| Field | Description |
|---|---|
| `name`, `position`, `personUrl`, `headshotUrl` | The investor and their profile. |
| `minInvestment`, `targetInvestment`, `maxInvestment` | Check size in USD. |
| `firmName`, `firmUrl` | The firm and its profile. |
| `investmentLocations`, `listMemberships` | Geographies and other lists they appear on. |
| `slug`, `listUrl`, `investorCount`, `stage`, `vertical` | List catalog fields. |
| `linkedinIndustry`, `linkedinSize`, `linkedinFollowers`, `linkedinUrl` | LinkedIn enrichment. |
| `crunchbaseRank`, `crunchbaseEmployees`, `crunchbaseStatus`, `crunchbaseUrl` | Crunchbase enrichment. |

## Recipes

Ready-made examples on the Apify Store. Each one runs as-is.

- [Find Investors for Your Startup by Stage and Check Size](https://apify.com/johnvc/nfx-signal-investor-api/examples/find-investors-for-your-startup-by-stage-and-check-size?fpr=9n7kx3)
- [List of VC Firms in San Francisco Bay Area](https://apify.com/johnvc/nfx-signal-investor-api/examples/list-of-vc-firms-in-san-francisco-bay-area?fpr=9n7kx3)
- [Pre Seed Investors List With Check Sizes](https://apify.com/johnvc/nfx-signal-investor-api/examples/pre-seed-investors-list-with-check-sizes?fpr=9n7kx3)
- [Crunchbase Alternative for Investor and VC Firm Data](https://apify.com/johnvc/nfx-signal-investor-api/examples/crunchbase-alternative-for-investor-and-vc-firm-data?fpr=9n7kx3)
- [VC Database Export by Sector and Stage](https://apify.com/johnvc/nfx-signal-investor-api/examples/vc-database-export-by-sector-and-stage?fpr=9n7kx3)

**Schedule tip:** save any of these as a Task, attach a monthly Schedule, and diff each run to catch investors entering your sector.

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the NFX Signal Investor API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config**).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.apify.com/?tools=actors,docs,johnvc/nfx-signal-investor-api"]
    }
  }
}
```

3. Restart the app and complete the OAuth prompt, or add your Apify API token in connector settings.
4. Ask Cowork to run the NFX Signal Investor API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/nfx-signal-investor-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/nfx-signal-investor-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Verify with `claude mcp list`, or run `/mcp` inside a session.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it.
2. Authenticate with your Apify API token, and enable the tool `johnvc/nfx-signal-investor-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Or choose **Add custom connector** and paste `https://mcp.apify.com/?tools=actors,docs,johnvc/nfx-signal-investor-api`.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/nfx-signal-investor-api"
    }
  }
}
```

Then open **Cursor → Settings → MCP** and confirm the **apify** server shows a green dot.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

1. Profile icon → **Settings > Apps**. Enable **Developer mode** under Advanced settings if you do not see **Create app**.
2. **Create app**: name it Apify, MCP Server URL `https://mcp.apify.com/?tools=actors,docs,johnvc/nfx-signal-investor-api`, Authentication OAuth.
3. Click **Create** and authorize with Apify.
4. In a chat, click **+ → Developer mode** and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

## FAQ

### How do I find investors for my startup?

Run `mode: "lists"` to see the catalog, pick the slugs matching your sector and stage, then run `mode: "investors"` on them. Sort by `targetInvestment` and you have a target list ordered by the cheque each investor writes.

### Do I need a Signal NFX login?

No. The lists this reads are the public ones on [signal.nfx.com](https://signal.nfx.com), so no account or token is needed for the source.

### How do I get a list of VC firms for one city?

Use `mode: "firms"` with a geographic list slug such as `san-francisco-bay-area`, `new-york-city`, or `london`.

### Is this a Crunchbase alternative?

It is a complement. Those platforms are company-centric databases; this is investor-centric and includes check sizes that company databases rarely publish. You can enrich firms with Crunchbase data in the same run.

### People also search for

signal nfx, nfx signal investors, how to find investors, list of vc firms, vc database, venture capital data, pre seed investors, early stage investors, scraping investor lists

## Related

- Actor on Apify Store: https://apify.com/johnvc/nfx-signal-investor-api?fpr=9n7kx3
- Report an issue: https://apify.com/johnvc/nfx-signal-investor-api/issues/open?fpr=9n7kx3

Last Updated: 2026.08.20
