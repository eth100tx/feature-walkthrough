# Writing the tour

The tour is the whole product. A beautiful mockup with a weak script gets closed
after four steps. A plain mockup with a good script gets watched to the end and
answered.

## The shape of a step

```js
{ text:'Quotes whose effective date has already passed. You did not win them, and they need closing out.',
  run: async()=>{ activeFilter='expired'; renderMockup();
                  await sleep(150); await spotReveal(['#filterChip','#rows'], 8); } },
```

`text` is what the caption says. `run` changes the screen to match, waits long
enough for the change to land, then calls `spotReveal()` on the thing being talked
about. The engine handles the timing, the dimming, and the caption.

## The rules that matter

**One idea per step.** If your sentence contains "and", it is probably two steps.
Two short steps always beat one long one.

**Say what it does for the person, not what the control is called.** "Click a badge
and the list filters to exactly those policies" is right. "There is a filter
control in the top right" is a manual, not a walkthrough.

**Make the screen move.** This is the single biggest difference between convincing
and cheap. Do not narrate over a static screen. Filter the list. Open the panel.
Cycle a setting through four real values so the counts visibly change. Click through
the options in a dialog one at a time. The viewer should see the feature working,
not hear about it.

```js
// Weak: describes a setting.
{ text:'You can change the warning window.',
  run: async()=>{ openSettings(); await spotReveal(['#settings'], 14); } }

// Strong: the numbers move while they watch.
{ text:'Three days for quotes, thirty for renewals — change them and the counts move.',
  run: async()=>{ openSettings(); await sleep(80);
                  await spotReveal(['#quoteDays','#badges'], 12);
                  for(const v of [5,8,12,8,3]){ settings.quoteDays=v; renderMockup();
                                                applySpot(); await sleep(340); } } }
```

**Spotlight the smallest region that makes the point.** `spotReveal()` takes an
array of selectors and lights up their combined bounding box. Two adjacent elements
is fine. Half the screen defeats the purpose.

**Open on the world as it is now.** The first step should show the existing screen
before the feature appears, so the viewer has something to compare against.

**End with the question.** The last step's text should be a version of "that is the
whole feature — does this look right?" When it finishes, the engine opens the
review panel by itself.

**Eight to fifteen steps.** Below eight, it feels thin. Above fifteen, people stop
watching. If the feature genuinely needs more, it is two features and it deserves
two walkthroughs.

## Pacing

The engine holds one second after the caption appears before running the step, then
holds 2.6 seconds after a short caption or 3.4 seconds after a long one. You do not
need to manage that.

What you do manage is the timing *inside* a step:

- `await sleep(120)` to `sleep(200)` after a re-render, before spotlighting, so the
  spotlight measures the element in its new position
- `await sleep(330)` to `sleep(560)` between frames of an animated sequence
- `await sleep(700)` after opening a dialog, before interacting with it

If a spotlight lands in the wrong place, the cause is almost always a missing sleep
between the re-render and the `spotReveal()` call.

## Functions available to a step

| Call | Does |
|---|---|
| `spotReveal(selectors, pad)` | Dim the screen and grow the highlight out of the caption onto these elements |
| `applySpot()` | Re-measure the current highlight, after the page moved underneath it |
| `spotOff()` | Clear the dimming entirely |
| `sleep(ms)` | Wait |
| `resetMockup()` | Put the mockup back to its opening state |
| `MODKEY` | "option" on a Mac, "alt" elsewhere — use it in caption text |

## The intro card

Three or four points, each a bold line and one plain line underneath. Write it as
"this is what we think we heard", because that is what it is for. It gives the
reviewer the shape of the thing before anything moves, and it gives them a fair
chance to say "that is not what I asked for" in the first ten seconds rather than
the last.

It auto-advances after about seven seconds, or when they press the button.

## Voice

Write like a person explaining their work to a colleague, not like a product
brochure and not like documentation.

- Say "you" to the reviewer.
- Short sentences.
- No exclamation marks, no "simply", no "just", no "seamlessly", no "powerful".
- Use the customer's own words for their own things, always.
- It is fine to state the reason behind a rule: "A quote past its effective date is
  business we lost." That one sentence shows you understood their business, and it
  is worth more than three sentences about the interface.

## Testing your own script

Read the captions on their own, in order, with the screen covered. If they tell a
coherent story by themselves, the tour is good. If they only make sense while
looking at the screen, rewrite them.
