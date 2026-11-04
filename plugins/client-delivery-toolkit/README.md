# Client Delivery Toolkit

Tools for presenting to clients. Built from consultant-made skills; first one is Anna D'Amico's **Readout Script**.

## Readout Script

Turns the slides you're presenting into a talking track you rehearse from, in **your** speaking voice.

**Start it:** `/client-delivery-toolkit:readout-script`, or say "generate a script for this presentation", "write a readout script", "talking track for slides 10–12".

**You give it:** the deck (.pptx, PDF or SharePoint link) and which slides are yours. It asks about the room, tone and objective, and optionally checks email, Teams/Slack, meeting notes (Otter or Granola) and the project folder for context.

**You get:** a Word doc with, for each slide, a key message, talking points (paste into speaker notes), a full script and a transition. It ends with **prep notes**: likely client questions with answers, follow-ups, numbers to check, and an internal-only room-context list.

**It's a first draft for rehearsal, not something to read aloud.** Practice from it, then present from the talking points. That's how Anna used it for Corning.

**Your voice:** first run, it learns how you talk from your recorded calls, a past script, or your emails, and offers to save that as a personal `my-readout-voice` skill so later runs skip this step. The profile holds no client content and isn't shared.

**Rules it keeps:** every fact comes from the slides. Email or meeting context shapes emphasis and the prep notes, never the script. Conflicts get flagged under "Check before presenting."

**Run logging:** each run is logged (your email, tool, project code) to Newry's plugin usage log.

**Known overlap:** if you have Anna's older `client-talking-track` or the standalone `readout-script` skill installed personally, remove it so Claude doesn't pick the wrong one.

## Dependencies

- Built-in `docx` and `pptx` skills
- Connectors (all optional except M365 for SharePoint decks): Microsoft 365, Otter or Granola, Slack, Airtable
- `newry-knowledge` plugin (optional, for relationship notes)
