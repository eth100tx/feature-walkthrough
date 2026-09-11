# Getting the walkthrough in front of people

Do none of this unless the user asks. The default — one file, sent as an
attachment — works, needs no infrastructure, and cannot break.

## Default: just send the file

The output is a single HTML file with no dependencies. Email it, drop it in chat,
put it on a shared drive. The recipient double-clicks it and it plays.

This works offline, works on any operating system, works on a locked-down corporate
laptop, and will still work in five years.

The reviewer's answer comes back through whichever of these they prefer:

- **Copy** puts the review on their clipboard to paste wherever they like
- **Download** saves it as a text file
- **Email it** opens a pre-filled message, if `FEEDBACK_EMAIL` was set

Nothing leaves the page unless the reviewer presses one of those buttons.

## Optional: the answer comes back on its own

If the user wants reviews to arrive in their chat tool without the reviewer having
to copy anything, set the two webhook constants at the top of the file:

```js
const WEBHOOK_URL   = 'https://hooks.slack.com/services/...';
const WEBHOOK_STYLE = 'slack';    // or 'discord'
```

For Slack, create an incoming webhook at `api.slack.com/apps` → your app →
Incoming Webhooks. For Discord, it is Server Settings → Integrations → Webhooks.

Three things to be straight with the user about before they do this:

1. **The webhook URL is in the file.** Anyone who receives the walkthrough can read
   it and post to that channel. Use a webhook pointing at a channel where that does
   not matter, and rotate it when the project ends. Never reuse a webhook that is
   wired to anything important.
2. **It fails quietly by design.** If the post does not go through, the reviewer
   still sees their review and the copy, download and email buttons. They never hit
   a dead end because of your infrastructure.
3. **It is fire-and-forget.** The request is sent as `text/plain` to dodge the CORS
   preflight that Slack and Discord both reject, which means the browser cannot read
   the response. The page assumes it worked. If reviews are not arriving, test the
   webhook with `curl` rather than debugging in the browser.

## Optional: put it on a web address

Some reviewers will not open an HTML attachment, and some mail systems strip them.
A link avoids both problems.

It is one static file, so anything that serves static files will do. Free options
that need no server of your own:

- **GitHub Pages** — commit the file to a repository, enable Pages, link to it
- **Netlify Drop** — drag the file onto `app.netlify.com/drop`, get a URL
- **Cloudflare Pages** — same idea, connected to a repository
- **Any web host you already have** — copy the file in, it needs nothing but a
  static file server

Two cautions worth passing on:

- A public URL is public. Anyone with the link can see the feature you are
  proposing and the customer it is for. If that matters, use the attachment, or
  put the page behind whatever access control your host offers.
- Give the file a name nobody would guess if you are relying on obscurity, and
  remember that obscurity is not access control.

## What not to build

Resist building a service around this. The value is that it is one file that works
everywhere and depends on nothing. A hosting platform, a review database and a
notification pipeline is a different product, and it is the thing that stops people
from using this at all.
