# Worked example

`expiring-quotes-walkthrough.html` is a complete, real walkthrough. Open it in a
browser before you build your own — it is faster than reading about it.

It was produced by this skill for an insurance MGA platform, then rewritten for
publication: the customer's name, their logo and the reviewing team's details have
all been replaced. The fake data was always fake. The product is called "Meridian
Specialty" here and does not exist.

## What the feature is

An underwriter's policy list is long, and three things on it are quietly going
wrong at any moment:

1. Quotes whose effective date has already passed — business that was lost and
   never closed out
2. Quotes about to go effective in the next few days — still time to chase the
   broker
3. In-force policies expiring soon with no renewal started

The proposed feature watches for all three in the background and shows a small
stack of badges in a corner of the screen. Click one and the list filters to
exactly those policies.

## Why it is built the way it is

**The screen is the real screen.** The sidebar, the table, the status pills, the
view tabs and the density were all read off the actual application. Someone who
uses that product every day recognises it immediately, and that recognition is what
makes them engage with the proposal instead of squinting at it.

**The data is obviously invented.** Hogsmeade Hollow MHC, Acme Acres RV Resort,
Duckburg Estates. No customer will mistake these for their own records, which means
nobody spends the review arguing about whether the numbers are right. The *columns*
are real — Policy, Agency, UW, Effective, Expires, TIV, Premium — and that is what
had to be right.

**Today is frozen.** `TODAY` is a fixed date near the top of the file. Every
"expires in three days" in the walkthrough stays true forever. If it read the real
clock, the whole premise would fall apart a week later.

**The screen moves at every step.** Step four filters the list. Step six opens the
close-file dialog and clicks through all five reasons. Step ten cycles the warning
window through 5, 8, 12, 8 and back to 3 days while the badge counts visibly
change. Step eleven cycles the badges through three sizes. Step thirteen walks them
around all four corners of the screen. None of these are described — they happen.

**It answers the objection before it is raised.** Step twelve exists only to say
that a regular underwriter sees their own book and cannot widen it, because whoever
approves this will ask. Answering it inside the walkthrough is worth a week of
email.

**It ends by asking.** The last caption is "That is the whole feature. Does this
look right to you?" and the review panel opens by itself. The reviewer never has to
work out what is expected of them.

## Things worth stealing

- The badge stack parks in a corner the user picks and remembers the choice in
  `localStorage`, so the walkthrough can demonstrate a preference actually
  persisting
- The demo controls panel in the bottom left switches between two user roles, so
  one file can show what each role sees. It is clearly labelled as demo scaffolding
  that would not ship
- The intro card lists the three checks before anything moves, so a reviewer who
  disagrees with the premise can say so in the first ten seconds

## What was removed for publication

The customer's name and brand colour, their logo (which was embedded in the file as
an image), and the delivery configuration that posted reviews to a specific team
chat channel. The feedback constants are all blank, so the review panel falls back
to copy, download and email — which is the behaviour you get by default anyway.
