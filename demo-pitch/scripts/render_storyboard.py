"""Render a JSON storyboard as an offline production-review page, not a demo.

Standard library only. Usage: python render_storyboard.py INPUT.json OUTPUT.html
Does not execute supplied HTML, generate speech, or simulate product behavior.
"""
import argparse
import html
import json
from pathlib import Path


def render(data):
    def esc(value):
        return html.escape(str(value), quote=True)

    if not isinstance(data, dict):
        raise ValueError('Storyboard must be an object')
    for key in ('title', 'audience', 'decision', 'premise', 'status'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f'Missing text field: {key}')
    beats = data.get('beats')
    if not isinstance(beats, list) or not beats:
        raise ValueError('At least one storyboard beat is required')
    seen, cards, words, sections = set(), [], 0, {}
    for beat in beats:
        if not isinstance(beat, dict):
            raise ValueError('Each storyboard beat must be an object')
        for key in ('id', 'section', 'headline', 'speech', 'visual', 'proof',
                    'evidence_type', 'data_provenance', 'source', 'delivery'):
            if not isinstance(beat.get(key), str) or not beat[key].strip():
                raise ValueError(f'Missing text field in beat: {key}')
        if beat['id'] in seen:
            raise ValueError('Duplicate beat id: ' + beat['id'])
        seen.add(beat['id'])
        if beat['evidence_type'] not in ('observed', 'simulated', 'planned', 'measured'):
            raise ValueError('Unknown evidence type: ' + beat['evidence_type'])
        words += len(beat['speech'].split())
        sections[beat['section']] = sections.get(beat['section'], 0) + len(beat['speech'].split())
        fields = ''.join('<dt>' + esc(label) + '</dt><dd>' + esc(beat[key]) + '</dd>'
                         for key, label in [('visual', 'Visible scene'), ('proof', 'What it establishes'),
                                            ('data_provenance', 'Data provenance'),
                                            ('source', 'Source / limitation'), ('delivery', 'Voice direction')])
        cards.append('<article><p class="tag">' + esc(beat['section']) + ' · ' +
                     esc(beat['evidence_type']) + '</p><h2>' + esc(beat['headline']) +
                     '</h2><blockquote>' + esc(beat['speech']) + '</blockquote><dl>' + fields + '</dl></article>')
    title = esc(data['title'])
    section_summary = '; '.join(esc(k) + ': ' + str(v) + ' words' for k, v in sections.items())
    return ('''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>''' + title + ''' — storyboard</title><style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f3f1ec;color:#172a32;
font:17px/1.55 system-ui,sans-serif}main{max-width:1050px;margin:auto;padding:40px 24px}
header{background:#173a43;color:white;padding:32px;border-radius:16px}h1{font-size:36px;line-height:1.2}
h2{font-size:25px;line-height:1.25}.tag{text-transform:uppercase;letter-spacing:.09em;font-size:12px;font-weight:750}
article{background:white;border:1px solid #d5d9d5;border-radius:14px;padding:28px;margin-top:24px}
blockquote{margin:20px 0;padding:16px 20px;border-left:4px solid #b4572e;background:#faf5ef;font-size:21px}
dl{display:grid;grid-template-columns:175px 1fr;gap:12px}dt{font-weight:700}dd{margin:0;overflow-wrap:anywhere}
.notice{padding:16px;border:1px solid #c79350;background:#fff7e7;border-radius:8px}
@media(max-width:600px){main{padding:20px 12px}header,article{padding:20px}dl{display:block}dd{margin:4px 0 16px}}
@media print{body{background:white}main{padding:0}article{break-inside:avoid}header{color:#172a32;background:white}}
</style><main><header><p class="tag">Production storyboard · No audio or product interaction</p><h1>''' + title + '''</h1>
<p>''' + esc(data['premise']) + '</p></header><p class="notice">' + esc(data['status']) +
        '</p><p><strong>Audience:</strong> ' + esc(data['audience']) + '<br><strong>Decision:</strong> ' +
        esc(data['decision']) + '</p><p>' + str(words) +
        ' spoken words across all listed beats. ' + section_summary +
        '. Duration has not been recorded or measured.</p>' +
        ''.join(cards) + '</main></html>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Input and output must be different files')
    try:
        result = render(json.loads(args.input.read_text(encoding='utf-8-sig')))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding='utf-8')
    print(args.output.resolve())


if __name__ == '__main__':
    main()
