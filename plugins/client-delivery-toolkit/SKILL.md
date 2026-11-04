---
name: cd-readout
description: "Turn a client presentation deck into a slide-by-slide talking track (key message, talking points, full spoken script, transitions) plus prep notes with likely client questions. Use for 'generate a script for this presentation', 'write a readout script', 'talking track', 'script for my slides', 'what do I say on each slide', 'help me prep to present slides X–Y', or /cd-readout."
---

# Readout Script

Turns the slides a consultant is presenting into a talking track they can rehearse from and use in the room. Each slide gets the one thing the audience should take away, talking points to speak from loosely, a full script to read aloud, and a line that leads into the next slide. The script has to sound like a consultant talking to a client, not like written copy.

This is a rehearsal aid, not a teleprompter. The point is to get the presenter past the blank page so they can practice in their own words, and then present from the talking points. Every output says so (see Step 4).

## Usage logging

At the start of every run, before any other work, create one record in the Airtable Plugin Usage Log. The first time per session, tell the user in one line: "Logging this run to Newry's plugin usage log (your email, tool, project code)."

- **Base ID:** `appRawPuacfAvVH2Z` | **Table ID:** `tblmACtwIClniGn5n`
- **Tool:** `create_records_for_table`
- **Fields:**
  - `fldRrr3BkrJW8rE3L` (ts): current UTC time, ISO 8601 (e.g. `2026-11-04T14:30:00Z`)
  - `fldNHK285dPCOdNhB` (plugin): `"client_delivery_toolkit"`
  - `fld4EyuVEhxAhPZEd` (sub_skill): `"readout_script"`
  - `fldmTXyfFZRpbZEvQ` (user_id): the user's email from session context; `"unknown"` if unavailable
  - `fldu8rvXDfvi2O3jF` (project): the project code if the user or deck gives one (e.g. `"COR775"`), else `""`

If Airtable isn't connected or the write fails for any reason, just continue.

## Step 1: Gather inputs (before writing anything)

You need the deck plus three pieces of context. Ask for anything missing in a single AskUserQuestion call. Don't guess.

1. **Deck**: a .pptx, a PDF, or a SharePoint link. For a SharePoint link, find the file with the Microsoft 365 connector (sharepoint_search on the file name) and read it with read_resource. For a .pptx upload, use the pptx skill to extract the text. For a PDF, read the pages visually so charts aren't missed. Read every slide in scope: the action title, body bullets, sub-bullets, quote callouts, chart labels and values, footnotes, and tags such as "Preliminary".
2. **Client**: who is in the room. Company, the attendees' roles and seniority, how familiar they are with the topic, and any sensitivities.
3. **Tone**: for example confident and direct, collaborative and exploratory, formal executive readout, or technical deep-dive. This is the tone of the meeting. It is separate from the presenter's personal voice, which Step 1c handles.
4. **Meeting objective**: what the meeting has to achieve, such as aligning on findings, getting a decision, setting up next phase scope, or building credibility with a new stakeholder.

Also ask, as optional questions:

- **Which slides is this person presenting?** Often it's one section of a shared deck. Script only those slides, but read the whole deck, because the script refers back to earlier sections (especially the Summary of Findings).
- **Other presenters and handoffs**: who speaks before and after, so the script can say things like "…that Louis touched on at the beginning" and hand off cleanly.
- **Time allotted** for their section, which sets how long the scripts should be.
- **Pull in project context?** Ask whether to check recent client emails, meeting transcripts and project files for more context (see Step 1b). Let the user pick which sources to use, or skip this.
- **Match your voice?** First check whether the presenter has a saved voice profile (see Step 1c). If they do, ask: "Use your saved readout voice, or refresh it?" If they don't, ask how the script should learn their speaking voice: from their meeting recordings (Otter or Granola), a past script or speaker notes they wrote, a few of their emails, or skip and use the default house voice.

## Step 1b: Gather project context (optional, only if the user says yes)

This step helps you understand the room. It is not a source of new content for the script. Check only the sources the user approved, and use whichever connectors are available. If a connector isn't connected, say so in one line and move on.

- **Email and chat**: search Outlook (outlook_email_search), Teams and Slack for the client's name, the project code (e.g. COR775) and the attendees' names. Cover roughly the last 4–6 weeks, or the time since the last readout. Look for questions the client asked, concerns or pushback, decisions made, requests made of the team, and who is attending.
- **Past meetings**: search the meeting notetaker that's connected (Otter via otter_search, Granola via search_meetings / search_transcripts, or Teams meeting transcripts) for earlier client calls on this project. Note how the client reacted to past findings and any questions that were left open.
- **Project folder**: find the project's SharePoint folder from the deck's location or the project code. Read the SOW or proposal (the project objectives) and the most recent previous update deck (what was already presented). Skip interview transcripts and working files unless the user asks.
- **Relationship notes**: if the newry-knowledge skills are available, use airtable-search to look up the client's contacts and any context-log notes on the attendees.

Keep it bounded: read what's relevant to this meeting, not the whole history. Then post a short **context summary** (5–8 bullets, each naming its source, such as "email from [name], Oct 14") in a SendUserMessage, and ask the user to confirm or correct it before you write. That summary covers attendees, what the client cares about right now, open questions, sensitivities, and what was presented last time.

**How to use the context:**
- Use it to set the tone and objective, to choose which evidence to lead with, and to steer framing and transitions toward what the client cares about. For example, if the client asked about cost, lead with the cost evidence the slide already has.
- Use it heavily in the prep notes: likely questions, earlier questions this deck answers, and topics to handle carefully.
- Never put facts, numbers or quotes into the script that aren't on the slides, even if they appear in an email. Never have the presenter say anything that reveals a private email, internal Newry discussion, or a sensitivity about a person ("we know your VP is skeptical"). Put that kind of thing in the prep notes, marked internal.
- If the context contradicts the deck (for example, a number the client corrected over email), flag it in the prep notes under "Check before presenting" rather than quietly changing the script.

## Step 1c: Calibrate to the presenter's voice

The script is read aloud by the person running this skill, so it should sound like them, not like whoever wrote this skill. The presenter is whoever is using the skill unless they say they're scripting for someone else.

### Use a saved profile when there is one

Learning the voice is a one-time step. Before searching anything, check the available skills for a personal `my-readout-voice` skill (the user's saved spoken-voice profile). If it's there and the user chose to use it in Step 1, read it, use it as the voice profile, and skip the rest of Step 1c. Don't re-search recordings or emails, and don't ask the user to confirm the profile again. Only rebuild it when the user asks to refresh it, or when they're scripting for someone else.

### Build a profile (first run, or when refreshing)

Use only the sources the user picked in Step 1, in this order of preference:

1. **Their own meeting recordings (best).** Search whichever notetaker is connected (Otter via otter_search, or Granola via search_transcripts / get_meeting_transcript) for recent client calls or readouts where the presenter spoke at length, and read 2–3 of their longer speaking turns. Spoken transcripts show how they actually talk: sentence length, filler and qualifier words, how they signpost and hedge, "we" vs. "I".
2. **A past readout script, talking track or speaker notes they wrote** (an upload, or a file they point to on SharePoint).
3. **A few of their own sent emails** (outlook_email_search, from the presenter). Emails are written voice, so use them only for vocabulary, formality and pet phrases, not for sentence rhythm.
4. **None available or skipped:** use the default house voice in the reference example below.

Use only material the presenter produced themselves. Read it for style only: never carry facts, numbers, client names or quotes from these samples into the script.

From the samples, write a short **voice profile** (4–6 bullets: typical sentence length and run-on habits, qualifiers and filler they use, how they signpost points, formality and humor, phrases they repeat, how they hedge) with one short example line in their style. Post it in the same SendUserMessage as the context summary (or on its own if Step 1b was skipped) and ask the user to confirm or correct it. If a `my-writing-style` skill is available for this user, read it as an extra input, but prefer spoken samples over written ones.

When refreshing, start from the saved profile and change only what the new samples show differently.

## Step 2: Find the storyline

Before you script anything, write down for yourself the 1–2 sentence argument that runs through the slides in scope, and how each slide moves that argument forward. Check it against the deck's Summary of Findings, since the presenter's section is usually going into detail on one or more of those bullets. If you gathered project context, check that the storyline answers what the client has been asking about and what the SOW objectives call for. Each transition should come from this storyline: the bold closing line on one slide sets up the next slide's headline.

## Step 3: Turn each slide into a script

### How to work from the slide

- **Headline**: say the action title nearly word for word, so the room can follow on screen. Turn slide shorthand into speech: "~1 out of 6" becomes "about one out of six", "~2M" becomes "as many as about two million".
- **Bullets**: choose the 3–4 strongest pieces of evidence rather than reading every bullet. Leave supporting detail, such as mechanics or secondary sub-bullets, for Q&A. Follow the slide's order so the audience can track along.
- **Quote callouts**: don't read quotes aloud. Paraphrase the main point and attribute it by company or role: "AeroVironment gave us an example where…", "that lines up with the Robinson Unmanned perspective here…".
- **Charts and sizing slides**: point at the chart ("you can see the ramp here"), give the bottom-line numbers, then the main assumption in plain words (usually from the footnote), for example "If we conservatively hold the current one in six adoption rate…". Don't walk through every bar. Check whether figures are annual or cumulative before you say them.
- **Caveats**: add one only where the numbers depend on an assumption the client might misread ("The important caveat is…"). Don't add a caveat just because a slide is tagged Preliminary.
- **First slide of the section**: begin by explaining where the findings come from ("Through our primary research over the past few weeks…") and link back to the earlier presenter or the Summary of Findings.
- **Answering something the client asked**: if the context shows the client asked about something this slide covers, the presenter can say so naturally ("this gets at the question you raised last time about…"), but only for questions the client raised directly with the team, never for something learned from internal discussion.

### Output for each slide

**Slide [N]: [Short slide name]**

*Key message:* One sentence the audience should remember. It is usually a sharpened version of the action title.

*Talking points:*
- 3–5 bullets with the specific evidence: numbers, examples, attributed sources.

*Script:* Written to be spoken, in this order:
1. **Framing** (1 sentence), only where needed: a section opener, or a slide that changes perspective ("From the supplier side, we think…").
2. **Headline**, as described above.
3. **Evidence** in conversational prose. When there are several points, signpost them ("There are a few things I want to highlight here. First, **speed matters**… Second… Third… And lastly…") and bold the short label for each point.
4. **So-what** (1 sentence), starting with "So…" or "So ultimately…", that ties the evidence back to the headline.
5. **Caveat**, only where needed (see above).

*Transition:* One **bold** line at the end of the script that sets up the next slide's headline, often opening with "That being said…" or "And if…". If it's a natural pause point, add "Any questions here before I move on to the next slide?". Use these after dense slides, not on every slide. On the last slide in scope, the transition is the handoff to the next presenter or the close.

## Voice: sound like a person presenting

The script should read like someone talking through their slides, and a little unpolished is fine.

**Whose voice:** if Step 1c produced a voice profile, the script follows it. The profile decides word choice, sentence length and rhythm, qualifiers, signposting style and formality, and it overrides the stylistic "Do" items below where they conflict (for example, a presenter who naturally speaks in short sentences keeps short sentences). The reference example below is the default house voice, used when there is no profile, and a model of the structure either way. Whatever the voice, these rules always apply: no invented data, quotes or claims; no selling lines that aren't on the slide; no press-release phrasing (the written-word vocabulary and quotable closers listed under "Don't"); and the script must still sound spoken, not written.

**Do:**
- Write in first person plural ("we uncovered", "what we heard from our experts", "we think", "we're looking at this as"). The presenter can say "I" when they narrate ("I'll go over these in a little more detail").
- Let sentences run on the way people talk, joined with "and", "so" and "which" ("…which is a huge jump, so suppliers need to be able to scale…"). Vary the length of sentences.
- Use everyday spoken words and small qualifiers: "really", "pretty", "a lot", "around", "about", "going to", "right now", "anywhere from".
- Point at the slide: "here", "you can see", "this slide".
- Hedge the way a consultant would: "isn't likely to", "may", "probably", "we think".
- Keep the client's terms and acronyms as they use them (DDP, EO/IR, OEM, 1:1).

**Don't:**
- Write a string of short, punchy, polished sentences, or paragraphs that are all the same length.
- Use em-dash asides, triplets added for rhythm, or quotable closing lines ("that's where the scale comes from", "the real story here is…").
- Use "It's not X, it's Y" contrasts, or written-word vocabulary such as crucial, critical, key, landscape, leverage, unlock, robust, pivotal, underscore, notably, meaningful (use it at most once).
- Add selling lines or commentary that isn't on the slide, such as pitching the client's own product, unless the objective calls for it at the close.
- Invent data, quotes, sources or claims (for example "this came up in every interview") that aren't in the deck. If a slide is thin, flag it in the prep notes rather than padding.

**Length:** about 130 words per minute of speaking time. With no time given, aim for 150–250 words per content slide.

**Tone and objective:** match the seniority from Step 1. Executives get the so-what earlier with less detail, and technical audiences get more of the evidence. If the goal is a decision, introductions or a next phase, the last slide's transition should build up to that ask.

### Reference example (the default house voice and the target structure)

> **Slide 11 — Component supplier considerations**
>
> For suppliers, we think the winning component suppliers will combine reliability, speed, and cross-platform compatibility to drive scaled adoption.
>
> There are a few things I want to highlight here.
>
> First, **speed matters**. We heard an example where an eight-week lead-time advantage was enough to win an IR component competition, even though the customer accepted lower-grade optics as a result.
>
> Second, **winning the initial program doesn't necessarily lock in the business**. OEMs may continue looking for lower-cost alternatives even after military deliveries begin, so suppliers need to remain cost-competitive throughout the program.
>
> Third, **scale is becoming increasingly important**. Drone production expectations have moved from 20,000 units just a couple years ago, toward potentially more than a million drones per year, which is a huge jump, so component suppliers need to be able to scale with their OEM customers.
>
> So, ultimately, we see the winning suppliers as those that can combine quality, speed, scalability, and cross-platform compatibility, and DDP can help establish those suppliers as a trusted reference standard across multiple OEMs.
>
> **And if those supply-side requirements can be met, the longer-term opportunity is substantially larger than the current DDP quantities.**

Before you deliver, read each script aloud in your head. Rewrite any sentence that sounds like a press release or a summary someone wrote down rather than something said in a meeting. If there is a voice profile, also rewrite any sentence the presenter wouldn't plausibly say.

## Step 4: Deliver

- By default, produce a Word document (use the docx skill) titled "[Client] – [Meeting] Readout Script".
- **First thing in the document, before anything else**, a short boxed or shaded note:
  > **First draft for rehearsal, not for reading aloud.** Review it, change anything that doesn't sound like you, and practice until you can present from the talking points alone. The prep that makes you sharp on your feet is the rehearsal, not the script.
- Then a short header listing the client, tone, objective, slides covered and voice source (e.g. "your Granola calls, Oct 2026" or "default house voice"), followed by the slides in order. Send it to the user with SendUserFile.
- **Always** end with a **Prep notes** section, separate from the script. Lead with likely questions, since that's the most useful part for rehearsal:
  - **Likely client questions, by slide**, 2–3 per content slide, each with a short answer drawn from the evidence you left out of the script (or "not covered in the deck: check with the team" if the deck can't answer it). Where project context was used, include questions the client has already raised and say which slide answers them.
  - Follow-ups worth raising or offering (people to invite, analyses to show, such as a forecast with and without a key assumption, and anything the client requested that is still outstanding).
  - **Check before presenting**: numbers to double-check (annual vs. cumulative, headline vs. chart mismatches, anything the context contradicts), slides where the evidence is thin, or anything that clashes with the stated objective.
  - If project context was used: a short **Room context (internal)** list covering attendees, sensitivities and topics to handle carefully, each with its source. Label it internal so the document isn't forwarded as-is.
- In the chat message that delivers the file, repeat the rehearsal reminder in one line.
- Offer in one line to write the talking points into the .pptx speaker notes, or to make a shorter version that has only the key messages and transitions.
- **Save the voice for next time.** If you built or refreshed a voice profile this run (and it's the user's own voice, not someone they scripted for), offer in one line to save it so future runs skip calibration. On yes, call `propose_skills` with a personal skill named `my-readout-voice`: kind "new" if none exists, or "improvement" with target `my-readout-voice` (carrying the complete updated file) if it does. Use the SKILL.md format below. The user saves it from the review card.
- **Learn from corrections.** If the user edits the script's wording or says it doesn't sound like them, update the voice profile for the rest of the session. If they have a saved `my-readout-voice`, offer in one line to update it with what changed (same `propose_skills` improvement flow). Don't re-propose a save the user already declined in this conversation.

### `my-readout-voice` format

```markdown
---
name: my-readout-voice
description: "Reference only, not run on its own: [Name]'s spoken presenting voice, read by the readout-script skill when writing their talking tracks."
---

# [Name]'s readout voice

Built from: [sources, e.g. "3 Granola client calls, Sep–Oct 2026"]. Last updated: [date].

## Voice profile
- [4–6 bullets: sentence length and run-ons, qualifiers and filler, signposting, formality and humor, repeated phrases, hedging]

## Sounds like
> [1–2 short example lines in their style, on a generic topic, with no client names or data]

## Avoid
- [Things they've corrected or said don't sound like them]
```

Never put client names, numbers, quotes or other project content in this file. It describes how the person talks, not what they've said.
