# newry-ai-tools

Claude plugins for Newry, distributed firm-wide via Cowork's organization plugin settings.
Maintained by the Newry AI program team.

---

## Plugins

### Consultant-facing

| Plugin | Source folder | Purpose |
|--------|--------------|---------|
| newry-knowledge | `plugins/newry-knowledge/` | Firm-wide knowledge search — SharePoint, Airtable, and consultant tool directory. Requires M365 + Airtable connectors. |
| primary-research-toolkit | `plugins/primary-research-toolkit/` | End-to-end primary research workflow: plan, guide, acquisition, prep, synthesis, corpus query. Requires M365 connector. |
| sof-toolkit | `plugins/sof-toolkit/` | Evaluate, align, and draft Summary of Findings slides using the Pyramid Principle. |
| project-technical-onboarding | `plugins/project-technical-onboarding/` | Guides week-1 Technical Orientation document for any client engagement. Requires M365 connector. |

### Program builder-facing

| Plugin | Source folder | Purpose |
|--------|--------------|---------|
| newry-operator | `plugins/newry-operator/` | Design advisor, decision logger, build prioritization, quality review, and operator dashboard for anyone stewarding the AI program. |

---

## How updates work

Plugins are distributed via GitHub sync. The repo contains a `.claude-plugin/marketplace.json`
that lists all plugin source directories. When changes are pushed, Cowork syncs automatically
on the next user session (if "Sync automatically" is enabled) or on manual trigger.

**Prerequisite:** Cowork Org Settings → Plugins → `Newry-LLC/newry-ai-tools` connected as
plugin source with "Sync automatically" enabled. See `strategy/plugin-install-guide.md` in
the `Building Tools for Newry` working folder for setup instructions.

**Note:** Each plugin lives as a source directory in `plugins/` with a `.claude-plugin/plugin.json`
metadata file. The `.plugin` zip files in `outputs/` are kept for manual install fallback only
and are not used by GitHub sync.

---

## How to update a plugin (for maintainers)

1. Edit source `SKILL.md` files in `plugins/<plugin-name>/skills/`
2. Run the **Plugin Auditor** skill to review changes
3. Update version in `plugins/<plugin-name>/.claude-plugin/plugin.json`
4. Update `strategy/plugin-index.md` and `strategy/Newry AI Plugin Index.xlsx`
5. Push changes to `Newry-LLC/newry-ai-tools` → Cowork syncs automatically

For full program context, decision history, and build priorities: install `newry-operator.plugin`
and run "show the dashboard" in Cowork.

---

## Ownership

Repo owned by `Newry-LLC` org. Current maintainer: Sylvan Shank (`sylvansid`).
To transfer maintainer access after handoff: **GitHub Org Settings → Members → invite new owner**.
