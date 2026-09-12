# Research and design decisions

Research checked September 12, 2026. These are primary practitioner and vendor sources, not controlled evidence that a formula increases conversion. Summaries below are deliberately selective. The resulting skill is our synthesis, not an official implementation or endorsement of these methods.

| Source | Relevant guidance | Decision in this skill |
| --- | --- | --- |
| [Peter Cohan, Great Demo: Automated Demos Do—Get to the Point!](https://greatdemo.com/automated-demos-do-get-to-the-point/) (2024) | Establish the situation, show the deliverable, take the shortest useful path to it, offer optional depth, and choose a meaningful next action. | Show the result early after a concise problem; move menus and configuration into supporting material. |
| [2Win: Tell-Show-Tell](https://www.2winglobal.com/blog/tell-show-tell-product-demo-framework) (2026) | Frame relevance before a capability demonstration and connect the result to operational impact. A topic list and repeated description do not accomplish that. | Give each proof beat context, an observable change, and its meaning. Do not adopt the article's unsourced neuroscience explanation or absolute zero-error examples. |
| [Nancy Duarte: Developing the Big Idea](https://www.duarte.com/blog/how-to-develop-the-best-big-idea-for-your-presentation/) (2018) | Center a presentation on one point of view and what is at stake; cut material that does not serve it. | Write one sentence the viewer should remember and use it to choose scenes. |
| [Kevin Hale, Y Combinator: How to Design a Better Pitch Deck](https://www.ycombinator.com/blog/how-to-design-a-better-pitch-deck/) (2015) | Make a presentation legible, simple, and obvious so its important ideas can be understood and remembered. | Crop or enlarge the evidence, reduce competing text, and make the changed state easy to see. Deck advice informs visual clarity; it is not a complete software-demo method. |
| [April Dunford: Positioning](https://www.aprildunford.com/) | Positioning explains differentiated value relative to alternatives for a particular customer. | Identify the actual workaround and the audience who values the difference. We are not reproducing her book or asserting its full sales-pitch sequence. |
| [TechSmith: How to Record a Voice Over](https://www.techsmith.com/blog/voice-over/) (2026) | Script and rehearse; use natural tone, deliberate pacing, clear pronunciation, appropriate pauses, and test recordings. | Direct a performance, audition a passage, and inspect the finished recording. Greater enthusiasm alone does not solve flatness. |
| [OpenAI: Text to speech](https://developers.openai.com/api/docs/guides/text-to-speech) | Direction-capable speech generation can accept instructions for delivery. Synthetic speech requires clear disclosure. | Keep speech text and delivery instructions separate; verify current model support before generation. |
| [ElevenLabs: Text to Speech guide](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech) | Expression controls depend on the model; v3 supports audio tags, while its pause syntax differs from other models. | Use a provider adapter rather than treating SSML or bracketed directions as portable. |

## Resolving the apparent disagreement

The resulting default outline is **situation → problem/stakes → promise/early outcome → visible proof → payoff/CTA**. This is our synthesis: use a brief situation to establish relevance, reveal a useful result early, and devote the demonstration to substantiating it. Propose concrete content in that outline, agree the pitch goals with the user, and only then build the production artifact. Collaborative story development is a workflow choice in this skill, not a finding from the cited sources.

“Start with the problem” and “show the end result first” can coexist: briefly name a relevant problem, then present the outcome before the setup steps. A cold viewer needs context. A well-qualified live prospect may need only one sentence of it. Neither approach justifies opening with a long company introduction or a contextless dashboard.

Tell-show-tell is useful inside a proof scene. It is not a reason to repeat every sentence three times. The close should explain what changed for the viewer.

## Brainstormed formats

| Angle | Best fit | Opening / proof | Failure to avoid |
| --- | --- | --- | --- |
| Decision under pressure | Buyer with a consequential recurring job | A recognizable moment of uncertainty; show the answer, then how it becomes trustworthy. | Invented catastrophe or making normal work seem foolish. |
| Before / after the handoff | Products shared by several roles | One person's work creates another's decision; follow the same artifact through both views. | Two disconnected persona tours. |
| New way to do a familiar job | New category or changed workflow | Show the constraint of the current workaround, then a qualitatively different result. | Unsupported competitive superiority or AI spectacle. |

These are options, not required opening tropes. A routine but costly delay can be a stronger problem than a fictional emergency. A highly technical audience may need deeper evidence; a short investor clip may need a concise mechanism followed by separately sourced business evidence.

## Production heuristics, not research findings

A roughly two-minute recorded pitch is a possible starting hypothesis for a short concept demo, not a universal optimum. Put the recognizable problem in the opening seconds, show an outcome before a long sequence, and reserve the bulk of time for meaningful proof. Estimate spoken time at roughly 130–155 words per minute while drafting, then replace estimates with measured audio plus visual reading time. Dense UI and unfamiliar terms require more room.

Choose one next step that matches readiness: review the concept, test a workflow with sample data, scope a pilot, or schedule a technical discussion. Do not invent pilot availability, contact details, traction, or a booking destination.
