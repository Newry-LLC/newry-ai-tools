# newry-ai-tools

Claude plugins for Newry, distributed firm-wide via Cowork's organization plugin settings.
Maintained by the Newry AI program team.

---

## Plugins

### Consultant-facing

| Plugin | Purpose |
|--------|---------|
| `newry-knowledge.plugin` | Firm-wide knowledge search — SharePoint, Airtable, and consultant tool directory. Requires M365 + Airtable connectors. |
| `primary-research-toolkit.plugin` | End-to-end primary research workflow: plan, guide, acquisition, prep, synthesis, corpus query. Requires M365 connector. |
| `sof-toolkit.plugin` | Evaluate, align, and draft Summary of Findings slides using the Pyramid Principle. |
| `project-technical-onboarding.plugin` | Guides week-1 Technical Orientation document for any client engagement. Requires M365 connector. |

### Program builder-facing

| Plugin | Purpose |
|--------|---------|
| `newry-operator.plugin` | Design advisor, decision logger, build prioritization, quality review, and operator dashboard for anyone stewarding the AI program. |

---

## How updates work

Plugins are auto-distributed via GitHub. When a new `.plugin` file is pushed to this repo,
Cowork automatically updates all users on their next session — no manual re-upload needed.

**Prerequisite:** Cowork Org Settings → Plugins → `Newry-LLC/newry-ai-tools` connected as
plugin source with "Sync automatically" enabled. See `strategy/plugin-install-guide.md` in
the `Building Tools for Newry` working folder for setup instructions.

---

## How to update a plugin (for maintainers)

1. Edit source `SKILL.md` files in `Building Tools for Newry/plugins/<plugin-name>/`
2. Run the **Plugin Auditor** skill to review changes
3. Repackage using the **Plugin Builder** skill → saves updated `.plugin` to `outputs/`
4. Update `strategy/plugin-index.md` and `strategy/Newry AI Plugin Index.xlsx`
5. Uninstall old version in Cowork → install new `.plugin`
6. Push updated `.plugin` to this repo → auto-update distributes to all users

For full program context, decision history, and build priorities: install `newry-operator.plugin`
and run "show the dashboard" in Cowork.

---

## Ownership

Repo owned by `Newry-LLC` org. Current maintainer: Sylvan Shank (`sylvansid`).
To transfer maintainer access after handoff: **GitHub Org Settings → Members → invite new owner**.
