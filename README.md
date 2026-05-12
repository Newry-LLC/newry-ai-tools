# newry-ai-tools

Claude plugins for Newry consultants. Managed by the Newry-LLC GitHub org and distributed firm-wide via Cowork's organization plugin settings.

## Plugins

### `newry-knowledge.plugin`

Firm-wide knowledge plugin with two skills:

- **sharepoint-search** — Answers natural language questions against any Newry SharePoint content: project materials, internal resources, client documents, decks. Requires the Microsoft 365 connector in Cowork settings.
- **airtable-search** — Answers questions about Newry project history, AER learnings, client contacts, and staff expertise. Requires the Airtable connector in Cowork settings.

### `primary-research-toolkit.plugin`

End-to-end primary research workflow: research plan design, interview guide design, interviewee acquisition, interview prep, coding & synthesis, and corpus query. Requires the Microsoft 365 connector in Cowork settings.

### `cowork-fix.skill`

Standalone troubleshooting guide for the Cowork workspace startup error (`Failed to start Claude's workspace — VHDX file not found`). Distributed separately as needed; not installed org-wide.

## How to update a plugin (for maintainers)

1. Edit the source `SKILL.md` files in the local plugin folder (`Building Tools for Newry/plugins/<plugin-name>/`)
2. Run the Plugin Auditor skill to review changes
3. Repackage using the Plugin Builder skill → saves updated `.plugin` file to `outputs/`
4. Upload the updated file via Cowork → Organization Settings → Plugins

## Ownership

Repo owned by Sylvan Shank (`sylvansid`). To transfer after handoff: **GitHub Org Settings → Danger Zone → Transfer ownership**.
