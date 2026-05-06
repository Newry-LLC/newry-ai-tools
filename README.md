# newry-ai-tools
Claude skills and plugins for Newry consultants. Managed by the Newry-LLC GitHub org and distributed firm-wide via Cowork's organization plugin settings.

## Skills

### `cowork-fix.skill`
Guides users through fixing the Cowork workspace error: `Failed to start Claude's workspace — VHDX file not found`. Triggers automatically when a user mentions the Cowork startup error to Claude. Walks the user through a back-and-forth diagnostic — user runs PowerShell commands, Claude interprets results and gives the next step.

### `sharepoint-search.skill`
Lets Claude answer natural language questions against any Newry SharePoint content — project materials, internal resources, client documents, decks. Requires the Microsoft 365 connector to be active in Claude Desktop.

## How to update a skill (for maintainers)

1. Edit the .skill or .plugin file locally
2. Commit and push to this repo
3. Re-upload the updated file via Cowork → Organization Settings → Plugins

## Ownership

Repo owned by Sylvan Shank (`sylvansid`). To transfer after handoff: **GitHub Org Settings → Danger Zone → Transfer ownership**.
