# -*- coding: utf-8 -*-
"""Backfill a phase4_status field onto every person record (131 total) and a
firm-level rollup, so verification coverage is queryable directly from the
data files -- this becomes an Airtable column at write-back time."""
import json
import glob
from pathlib import Path

DATA = Path(__file__).parent / "data" / "people"
CHECKED_DATE = "2026-07-03"

# (crd, name) -> status, compiled from every Phase 4 round run this session
VERIFIED = [
    ("335594", "Cean Nicholas Kenefick-rogers"), ("306180", "Jonathan David Bird"),
    ("311639", "Brian Joseph Rellihan"), ("105130", "Harry A Papp"),
    ("158641", "Dana Marie Anspach"), ("152662", "Markell Anthony Staffieri"),
    ("282003", "Brian Patrick Jack"), ("299951", "Mark Alan Bonnett"),
    ("299951", "Rick Schultenover"), ("131692", "Royce Creighton xxx-xx-xxxx RAMEY"),
    ("108818", "Todd Michael Foster"), ("175300", "Curt Randall Thompson"),
    ("175300", "Matthew Keith Underwood"), ("129415", "Cynthia Kay Fick"),
    ("129597", "Eric Joshua Weiss"), ("129597", "Amanda Marie Wray"),
    ("318258", "Stephen Daniel Hofmann"), ("116933", "Kelly Alan Christensen"),
    ("116933", "Julia L. Christensen"), ("153410", "Mark Paul Stein"),
    ("158641", "Caley Jared Miller"), ("158641", "Amy Leigh Shepard"),
    ("173383", "Justin C Thomas"), ("285243", "Kimberly Karen Bannwarth"),
    ("318330", "Jenifer Warnhoff"), ("333708", "Joshua Adam Gardner"),
    ("337660", "Erin Beth Itkoe"), ("337660", "Erin Beth xxx-xx-xxxx ITKOE"),
]

VERIFIED_WITH_CAVEAT = [
    ("172113", "Geoffrey Allen Grenert"), ("108818", "John Edward Foster"),
    ("175300", "Donald Edward Callaghan"), ("175300", "Nicholas Guido Botticelli"),
    ("325721", "Jason Charles Rowley"), ("325721", "David T. Hatfield"),
    ("282017", "Robert Verlin Sollis"), ("285243", "Dawn Deborah Jurkovich"),
    ("131692", "Elizabeth Mollie Shabaker"),
    ("331395", "Jeremy Paul Dicker"), ("331395", "Jeremy Paul xxx-xx-xxxx DICKER"),
]

CORRECTED = [
    ("325721", "Aaron Paul Brodt"), ("116798", "Robert Ralph Korljan"),
    ("173383", "Andrew Joseph Brinkman"), ("131692", "Jennifer Wagoner Kirksey"),
    ("282003", "Matthew Joseph Figueroa"), ("298110", "Barry Scott Rhonemus"),
    ("105130", "Jeffrey Nels Edwards"), ("113954", "Michael Maurice Smith"),
    ("116069", "Alan Edward Rosenfield"), ("128549", "David John Fernandez"),
    ("129415", "Gina Giachetti Wight"), ("131458", "Jeffrey Stephen Watts"),
    ("131458", "Daniel Bradford Gwilliam"), ("131458", "David Bruce Watts"),
    ("131692", "Aimee Lynn Williams-Ramey"), ("143420", "Stephen Leon Harrison"),
    ("146054", "Colin Patrick Heafy"), ("147351", "Richard Alan Siegel"),
    ("147351", "James Nelson Robinson"), ("152662", "Matthew Ds Staffieri"),
    ("165214", "Carter Allen Pearl"), ("165214", "Daniel Steven Flack"),
    ("167657", "Mark Edward Rauguth"), ("168774", "Jake Clifford Ulrich"),
    ("285932", "Kyle Robert Spahn"), ("291070", "Cody Lee Ashton"),
    ("291070", "David Lee Dorsey"), ("291070", "Michael Clawson Bird"),
    ("298408", "Jeffrey Michael Jones"), ("317615", "Matthew Gene Walker"),
    ("318330", "Daniel Christopher Thompson"), ("326261", "Trent Robert White"),
    ("328450", "Zachary Stuart Brodt"), ("328450", "Marcus John Pimentel"),
]

status_map = {}
for crd, name in VERIFIED:
    status_map[(crd, name)] = "verified"
for crd, name in VERIFIED_WITH_CAVEAT:
    status_map[(crd, name)] = "verified_with_caveat"
for crd, name in CORRECTED:
    status_map[(crd, name)] = "corrected"

total_people = 0
total_checked = 0
missing = []

for f in sorted(glob.glob(str(DATA / "*.json"))):
    d = json.loads(Path(f).read_text(encoding="utf-8"))
    crd = d["crd"]
    checked_here = 0
    for p in d["people"]:
        total_people += 1
        key = (crd, p["name"])
        status = status_map.pop(key, "not_checked")
        p["phase4_status"] = status
        if status != "not_checked":
            p["phase4_checked_date"] = CHECKED_DATE
            checked_here += 1
            total_checked += 1
    d["phase4_firm_summary"] = f"{checked_here} of {len(d['people'])} people checked"
    Path(f).write_text(json.dumps(d, indent=2), encoding="utf-8")

print(f"Total people: {total_people}")
print(f"Total checked: {total_checked}")
if status_map:
    print(f"WARNING: {len(status_map)} (crd, name) pairs in the lists never matched a real record:")
    for k in status_map:
        print(" ", k)
else:
    print("All entries in VERIFIED/VERIFIED_WITH_CAVEAT/CORRECTED matched a real record.")
