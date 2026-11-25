"""Two-column Top Story layout with animated, semantic action icons."""
from .news_video import _esc

ICONS = {
    "search": "⌕", "profile": "♙", "chat": "▣", "chart": "↗",
    "edit": "✎", "check": "✓", "handoff": "→", "list": "☷", "shield": "◇",
}

CSS = """
.split-story{--split-left:90px;--split-right:90px;--split-top:165px;--split-bottom:164px;
  --split-gap:52px;--split-title:66px;--split-label:35px;--split-detail:24px;--split-icon:60px}
.split-story .split-grid{position:absolute;inset:var(--split-top) var(--split-right) var(--split-bottom) var(--split-left);
  display:grid;grid-template-columns:1fr 1.05fr;align-items:center;gap:var(--split-gap)}
.split-story .split-copy,.split-story .split-image{min-width:0}
.split-story .split-kicker{color:var(--ac1);font-weight:800;font-size:22px;letter-spacing:.09em;margin-bottom:14px}
.split-story .split-title{font-size:var(--split-title);font-weight:900;line-height:1.07;letter-spacing:-.04em;
  margin:0 0 30px;overflow-wrap:anywhere}
.split-story .split-steps{margin:0;padding:0;list-style:none;display:grid;gap:12px}
.split-story .split-step{display:grid;grid-template-columns:var(--split-icon) minmax(0,1fr);gap:16px;align-items:center;
  min-height:84px;padding:10px 16px;background:var(--pan);border:1px solid var(--bd);
  border-radius:18px;opacity:0}
.split-story .split-step strong,.split-story .split-step small{display:block;line-height:1.18;overflow-wrap:anywhere}
.split-story .split-step strong{font-size:var(--split-label);font-weight:750}
.split-story .split-step small{font-size:var(--split-detail);color:var(--mut);margin-top:4px}
.split-story .split-icon{width:var(--split-icon);aspect-ratio:1;display:grid;place-items:center;color:var(--ac1);
  border-radius:14px;background:rgba(94,209,225,.12);font-size:calc(var(--split-icon)*.66);
  font-weight:700;line-height:1}
.split-story .split-step:not(:last-child){position:relative}
.split-story .split-step:not(:last-child)::after{content:"";position:absolute;left:31px;
  bottom:-13px;height:12px;width:2px;background:var(--ac1)}
.split-story .split-image{margin:0;border-radius:22px;background:var(--pan);border:1px solid var(--bd);
  padding:12px;box-shadow:0 24px 65px #0007}
.split-story .split-image img{display:block;width:100%;aspect-ratio:1.36;object-fit:contain;
  border-radius:13px;background:#0a1223}
.split-story .split-image figcaption{font-size:18px;color:var(--mut);padding:11px 4px 0;line-height:1.2}
[data-width="1080"] .split-story{--split-left:58px;--split-right:106px;--split-top:230px;
  --split-bottom:410px;--split-gap:24px;--split-title:53px;--split-label:31px;
  --split-detail:24px;--split-icon:48px}
[data-width="1080"] .split-story .split-grid{grid-template-columns:1fr .96fr}
[data-width="1080"] .split-story .split-step{padding:12px 10px;gap:10px}
[data-width="1080"] .split-story .split-image{padding:7px}
[data-width="1080"] .split-story .split-image img{aspect-ratio:.87}
[data-width="1080"] .split-story .split-image figcaption{font-size:17px}
"""


def scene_html(scene, sid, image, kicker):
    cards = []
    for index, item in enumerate(scene["diagram"]["items"]):
        icon = ICONS[item["icon"]]
        detail = f'<small>{_esc(item["d"])}</small>' if item.get("d") else ""
        cards.append(f'<li class="split-step" id="{sid}-step{index}">'
                     f'<div class="split-icon" aria-hidden="true">{icon}</div>'
                     f'<div><strong>{_esc(item["t"])}</strong>{detail}</div></li>')
    alt = scene.get("media_alt") or scene["title"]
    credit = _esc(scene.get("media_credit", ""))
    return (f'<section class="seg split-story" id="{sid}"><div class="split-grid">'
            f'<div class="split-copy"><div class="split-kicker">{_esc(kicker)}</div>'
            f'<h2 class="split-title">{_esc(scene["title"])}</h2>'
            f'<ol class="split-steps">{"".join(cards)}</ol></div>'
            f'<figure class="split-image"><img src="{_esc(image)}" alt="{_esc(alt)}">'
            f'<figcaption>{credit}</figcaption></figure></div></section>')


def scene_animation(scene, sid, start, duration):
    count = len(scene["diagram"]["items"])
    for index in range(count):
        cue = start + min(0.2, duration * 0.1) + index * duration * .54 / count
        step = f"#{sid}-step{index}"
        yield (f'    m.fromTo("{step}",{{opacity:0,y:18}},'
               f'{{opacity:1,y:0,duration:0.32,ease:"power2.out"}},{cue:.2f});')
        yield (f'    m.fromTo("{step} .split-icon",{{scale:0.68}},'
               f'{{scale:1,duration:0.42,ease:"back.out(2)"}},{cue:.2f});')
