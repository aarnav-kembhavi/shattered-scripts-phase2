"""Annotator packages (2026-10-24, Aarnav): annotation/dist/annotator_{A,B}/ with the annotation page, a one-page quick
start (PDF, screenshots of every step), three worked examples (PDF; items not in the 500), the instructions (PDF), a
ready-to-paste WhatsApp message, and a zip of the folder (the message is left out of the zip: it is for Aarnav).

Screenshots come from a demo copy of annotate_v2.html whose embedded items are replaced by the worked-example items
(so no screenshot shows any of the 500 items or any draft of a blind item) and whose file pickers are stubbed (the
browser's own Save/Open window cannot be captured; the quick start describes it in words). Headless Chrome is driven
over the DevTools protocol. Rater C's package is not built here (only after B's 40 blind items arrive).

Usage: python scripts/k_package.py
"""
from __future__ import annotations

import base64
import html
import json
import re
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

import websocket

REPO = Path(__file__).resolve().parents[1]
ANN = REPO / "annotation"
PAGE = ANN / "annotate_v2.html"
EXAMPLES = ANN / "examples_v1.json"
DIST = ANN / "dist"
CHROME = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
ROLES = {"annotator_A": {"name": "Annotator A", "mode": "all", "n": 500, "md": ANN / "instructions/annotator_A.md"},
         "annotator_B": {"name": "Annotator B", "mode": "double", "n": 100, "md": ANN / "instructions/annotator_B.md"}}


# ---------------------------------------------------------------- inputs

def load_examples() -> list:
    """The worked examples, with every draft checked against the stored draft file it is quoted from."""
    E = json.load(open(EXAMPLES, encoding="utf-8"))["examples"]
    items = {json.loads(x)["id"] for x in (REPO / "data/annotation/items_v2.jsonl").open(encoding="utf-8")}
    natives = {json.loads(x)["native"] for x in (REPO / "data/annotation/items_v2.jsonl").open(encoding="utf-8")}
    stored = {}
    for f in ("drafts_v1.jsonl", "drafts_regen_v1.jsonl"):
        for x in (REPO / "data/annotation" / f).open(encoding="utf-8"):
            r = json.loads(x)
            stored.setdefault((r["id"], r["kind"]), []).append(r["text"])
    for x in (REPO / "data/processed/natural_flores_m4_500_v1.jsonl").open(encoding="utf-8"):
        r = json.loads(x)
        stored.setdefault((f"flores-{r['index']}", "natural"), []).append(r["natural"])
    for e in E:
        assert e["id"] not in items and e["native"] not in natives, f"{e['id']} is one of the 500 items"
        for kind in ("natural", "kanglish"):
            if e[kind]:
                assert e[kind]["draft"] in stored.get((e["id"], kind), []), f"{e['id']} {kind}: draft not in files"
    return E


def demo_page(E: list, out: Path) -> None:
    """annotate_v2.html with the worked-example items in place of the 500, and stubbed file pickers."""
    src = PAGE.read_text(encoding="utf-8")
    demo = []
    for k, e in enumerate(E[:2]):  # standard items (drafts shown)
        demo.append({"id": e["id"], "source": "flores_sib" if e["id"].startswith("flores") else "sentiment",
                     "native": e["native"], "english": e["english"], "natural_draft": e["natural"]["draft"],
                     "kanglish_draft": e["kanglish"]["draft"], "double": True, "blind": False})
    b = E[2]  # the second annotator's first screen: a blind item (no drafts shown)
    demo.insert(0, {"id": b["id"], "source": "flores_sib", "native": b["native"], "english": b["english"],
                    "natural_draft": "", "kanglish_draft": "", "double": True, "blind": True})
    new, n = re.subn(r'(<script id="items" type="application/json">)(.*?)(</script>)',
                     lambda m: m.group(1) + json.dumps(demo, ensure_ascii=False) + m.group(3), src, count=1, flags=re.S)
    assert n == 1
    stub = """<script>
window.__saved = '';
const __handle = name => ({name, createWritable: async () => ({write: async t => { window.__saved = t; }, close: async () => {}}),
  requestPermission: async () => 'granted', getFile: async () => ({text: async () => window.__saved})});
window.showSaveFilePicker = async o => __handle(o.suggestedName);
window.showOpenFilePicker = async () => [__handle(window.__resumeName)];
</script>
"""
    new = new.replace('<script id="items"', stub + '<script id="items"', 1)
    out.write_text(new, encoding="utf-8")


# ---------------------------------------------------------------- headless Chrome over CDP

class Chrome:
    def __init__(self, width=720, height=900):
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        self.port = s.getsockname()[1]
        s.close()
        self.prof = tempfile.mkdtemp(prefix="kpkg_")
        self.proc = subprocess.Popen([str(CHROME), "--headless=new", f"--remote-debugging-port={self.port}",
                                      f"--user-data-dir={self.prof}", "--no-first-run", "--disable-gpu",
                                      "--allow-file-access-from-files", f"--window-size={width},{height}",
                                      "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json"))
                ws = next(t["webSocketDebuggerUrl"] for t in tabs if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.1)
        self.ws, self.i = websocket.create_connection(ws, timeout=60, suppress_origin=True), 0
        self.cmd("Page.enable")
        self.cmd("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=2, mobile=False)

    def cmd(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == self.i:
                if "error" in m:
                    raise RuntimeError(f"{method}: {m['error']}")
                return m.get("result", {})

    def js(self, expr):
        r = self.cmd("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"])
        return r["result"].get("value")

    def goto(self, url):
        self.cmd("Page.navigate", url=url)
        for _ in range(200):
            if self.js("document.readyState") == "complete":
                break
            time.sleep(0.05)
        time.sleep(0.3)

    def shot(self, path: Path, selectors: list, pad=8, max_h=None):
        """Screenshot of the box enclosing the given elements (page coordinates)."""
        box = self.js("""(() => { const r = %s.map(s => document.querySelector(s).getBoundingClientRect());
            return [Math.min(...r.map(b => b.left)) + scrollX, Math.min(...r.map(b => b.top)) + scrollY,
                    Math.max(...r.map(b => b.right)) + scrollX, Math.max(...r.map(b => b.bottom)) + scrollY]; })()"""
                      % json.dumps(selectors))
        x0, y0, x1, y1 = box[0] - pad, max(0, box[1] - pad), box[2] + pad, box[3] + pad
        if max_h:
            y1 = min(y1, y0 + max_h)
        r = self.cmd("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                     clip={"x": max(0, x0), "y": y0, "width": x1 - max(0, x0), "height": y1 - y0, "scale": 1})
        path.write_bytes(base64.b64decode(r["data"]))

    def pdf(self, url, out: Path, scale=1.0):
        self.goto(url)
        r = self.cmd("Page.printToPDF", printBackground=True, preferCSSPageSize=True, scale=scale)
        out.write_bytes(base64.b64decode(r["data"]))
        return len(re.findall(rb"/Type\s*/Page[^s]", out.read_bytes()))

    def close(self):
        try:
            self.cmd("Browser.close")
        except Exception:
            pass
        self.proc.wait(timeout=20)
        shutil.rmtree(self.prof, ignore_errors=True)


# ---------------------------------------------------------------- screenshots

HL = "outline:3px solid #d62728; outline-offset:2px; border-radius:6px;"


def highlight(c: Chrome, sel: str | None):
    c.js("document.querySelectorAll('[data-hl]').forEach(e => { e.style.outline = ''; e.removeAttribute('data-hl'); });")
    if sel:
        c.js(f"(() => {{ const e = document.querySelector({json.dumps(sel)}); e.setAttribute('data-hl', 1); "
             f"e.style.cssText += {json.dumps(HL)}; }})()")


def screenshots(c: Chrome, demo: Path, role: dict, E: list, out: Path) -> list:
    """(file, caption) per step. The demo page holds: [blind item, example 1, example 2]."""
    out.mkdir(parents=True, exist_ok=True)
    c.goto(demo.as_uri())
    c.js("localStorage.clear()")
    c.goto(demo.as_uri())
    steps, hdr = [], ["header"]
    name, B = role["name"], role["mode"] == "double"
    c.js("document.querySelectorAll('textarea').forEach(t => t.style.minHeight = '135px')")
    if not B:  # Annotator A never sees the blind item, and A's items are not marked double
        c.js("ALL.shift(); ALL.forEach(r => r.double = false); show();")

    def step(fn, caption, sel, hl=None, **kw):
        highlight(c, hl)
        p = out / f"step{len(steps) + 1}.png"
        c.shot(p, sel, **kw)
        steps.append((p, caption))

    step(None, "Open <b>annotate_v2.html</b> in Chrome or Edge (double-click it, or drag it into a browser window).",
         ["header", "details"])
    c.js(f"document.getElementById('who').value = {json.dumps(name)}; "
         "document.getElementById('who').dispatchEvent(new Event('change'));")
    step(None, f"Type your name in the <b>Annotator</b> box (here \"{name}\"). Use exactly the same name every time.",
         hdr, hl="#who")
    if B:
        c.js("document.querySelector('input[value=double]').click();")
        step(None, "Select <b>Second annotator (100 items)</b>. Never use \"All 500 items\".", hdr,
             hl="input[value=double]")
    else:
        step(None, "Keep <b>All 500 items</b> selected.", hdr, hl="input[value=all]")
    c.js(f"document.getElementById('newfile').click();")
    time.sleep(0.4)
    step(None, "Click <b>New CSV file…</b>. A Save window opens: choose a folder you will find again (e.g. Documents) "
         "and click Save. The bar then says <i>Connected to …csv</i>.", hdr, hl="#newfile")
    if B:
        c.js("document.getElementById('ta-natural').value = 'apartment olagade yaaru iralilla.'; "
             "document.getElementById('ta-kanglish').value = 'apartment olage yaru irlilla';")
        step(None, "<b>Part 1 (first 40 items):</b> you see only the Kannada. Write both versions yourself, from "
             "scratch, then click Save and next. Nothing to rate.", ["#blind-banner", "#native", "#box-natural",
                                                                      "#box-kanglish"], max_h=520)
        c.js("document.getElementById('save').click();")
        time.sleep(0.4)
    e = E[0]
    for kind in ("natural", "kanglish"):
        c.js(f"document.querySelector('input[name={kind}_naturalness][value=\"{e[kind]['naturalness']}\"]').click();"
             f"document.querySelector('input[name={kind}_meaning][value=\"{1 if e[kind]['meaning'] == 'yes' else 0}\"]').click();")
    step(None, "<b>Rate first</b>, before changing anything: naturalness 1–5 and whether the draft keeps the meaning "
         "(yes/no), for both drafts.", ["#box-natural"], hl="#box-natural .scale", max_h=330)
    c.js(f"document.getElementById('ta-natural').value = {json.dumps(e['natural']['corrected'])};")
    step(None, "<b>Then correct</b> the draft in the box. If it is already fine, leave it unchanged (Reset brings "
         "the draft back). Do the same for the Kanglish draft.", ["#box-natural"], hl="#ta-natural")
    c.js(f"document.getElementById('ta-kanglish').value = {json.dumps(e['kanglish']['corrected'])};")
    c.js("document.getElementById('save').click();")
    time.sleep(0.5)
    c.js("idx = list().findIndex(r => r.id === %s); show();" % json.dumps(e["id"]))
    step(None, "Click <b>Save and next</b>. Every save rewrites your CSV file (the bar shows <i>Saved to …csv</i>), "
         "so nothing is lost if you close the page.", ["header", "#save", "#msg"], hl="#save", max_h=10)
    # the save row lives at the bottom of the page: shoot header and save row separately and stack them
    p_hdr, p_save = out / "_hdr.png", out / "_save.png"
    highlight(c, None)
    c.shot(p_hdr, ["header"])
    highlight(c, "#save")
    c.shot(p_save, ["#save", "#msg"], pad=10)
    stack(p_hdr, p_save, steps[-1][0])
    csv = c.js("window.__saved")
    c.js("localStorage.clear()")
    c.goto(demo.as_uri())
    c.js("window.__saved = %s; window.__resumeName = %s;" % (json.dumps(csv), json.dumps(f"{name}.csv")))
    if not B:
        c.js("ALL.shift(); ALL.forEach(r => r.double = false); show();")
    c.js(f"document.getElementById('who').value = {json.dumps(name)};")
    if B:
        c.js("document.querySelector('input[value=double]').click();")
    c.js("document.getElementById('openfile').click();")
    time.sleep(0.5)
    step(None, "<b>Next time:</b> open the page, enter the same name (and the same choice), click <b>Continue a CSV "
         "file…</b> and pick the same file. Then click <b>First unfinished</b>.", hdr, hl="#openfile")
    (out / "_hdr.png").unlink(missing_ok=True)
    (out / "_save.png").unlink(missing_ok=True)
    return steps


def stack(a: Path, b: Path, out: Path):
    from PIL import Image
    A, B = Image.open(a), Image.open(b)
    W = max(A.width, B.width)
    im = Image.new("RGB", (W, A.height + B.height + 16), "white")
    im.paste(A, (0, 0))
    im.paste(B, (0, A.height + 16))
    im.save(out)


# ---------------------------------------------------------------- documents

CSS = """
@page { size: A4; margin: 10mm; }
body { font: 10.5px/1.4 "Segoe UI", system-ui, sans-serif; color: #1d1d1b; margin: 0; }
h1 { font-size: 17px; margin: 0 0 2px; } h2 { font-size: 13px; margin: 10px 0 4px; }
.sub { color: #555; margin-bottom: 8px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 12px; }
.step { break-inside: avoid; border: 1px solid #ddd9d0; border-radius: 6px; padding: 6px; }
.step img { width: 100%; display: block; border: 1px solid #eee; margin-top: 4px; }
.n { display: inline-block; background: #1f5f8b; color: #fff; border-radius: 10px; width: 18px; text-align: center;
     font-weight: 600; margin-right: 4px; }
.foot { margin-top: 8px; padding: 6px 8px; background: #f4f2ec; border-radius: 6px; }
.kn { font-family: "Nirmala UI", "Noto Sans Kannada", sans-serif; font-size: 13px; }
.ex { break-inside: avoid; border: 1px solid #ddd9d0; border-radius: 6px; padding: 8px 10px; margin-bottom: 10px; }
.mono { font-family: Consolas, ui-monospace, monospace; font-size: 10.5px; background: #fafaf8; padding: 3px 5px;
        border-radius: 4px; }
.lab { font-size: 9px; text-transform: uppercase; letter-spacing: .05em; color: #6b6b66; margin-top: 5px; }
.rate { font-weight: 600; } .why { color: #333; margin-top: 3px; }
"""


def quickstart_html(role: dict, steps: list, out: Path, extra_cols: int) -> None:
    B = role["mode"] == "double"
    cells = "".join(f'<div class="step"><span class="n">{k}</span>{cap}<img src="{p.name}"></div>'
                    for k, (p, cap) in enumerate(steps, 1))
    foot = ("<b>Order:</b> do the first 40 items (Part 1, write from scratch) before anything else and do not click "
            "ahead. <b>Send your CSV to Aarnav as soon as Part 1 is done</b>, then again when you finish. "
            if B else "<b>Pace:</b> about 25 items a day; short sessions are fine. <b>Send your CSV to Aarnav at the "
            "end of each week</b> (attach the .csv file in WhatsApp as a Document). ")
    foot += ("<b>Rules:</b> type the way you really type; there is no single correct spelling. No translation tools, "
             "AI tools or dictionaries. Do not discuss items with anyone. Use the Note box for anything odd. "
             "Questions or problems: ask Aarnav.")
    # Annotator A checks the worked examples before annotating (Aarnav, 2026-10-25); B gets them only after Part 1
    first = "" if B else (
        '<div class="foot" style="margin:0 0 8px; background:#fdf1e6; border:1px solid #e8b48a">'
        '<span class="n" style="background:#a4400b">0</span><b>Before you start: check the 3 worked examples.</b> '
        "Open <b>worked_examples.pdf</b> and read the 3 examples. If anything looks wrong (a rating, a correction, a "
        "spelling, a meaning), tell Aarnav what and why. Then start annotating with step 1.</div>")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Quick start</title><style>{CSS}
.grid {{ grid-template-columns: repeat({extra_cols}, 1fr); }}</style></head><body>
<h1>Quick start: {role['name']} ({role['n']} items)</h1>
<div class="sub">Kannada romanization check. You need <b>annotate_v2.html</b> and Chrome or Edge on a laptop or
desktop.{'' if B else ' Worked examples: <b>worked_examples.pdf</b>.'} Full instructions: <b>instructions.pdf</b>.</div>
{first}<div class="grid">{cells}</div><div class="foot">{foot}</div></body></html>"""
    out.write_text(doc, encoding="utf-8")


def examples_html(role: dict, E: list, out: Path) -> None:
    def kind_block(e, kind, title):
        k = e[kind]
        if not k:
            return ""
        same = k["corrected"] == k["draft"]
        return f"""<div class="lab">{title}: draft</div><div class="mono">{html.escape(k['draft'])}</div>
<div class="rate">Rating: naturalness {k['naturalness']} · keeps the meaning: {k['meaning']}</div>
<div class="lab">{title}: corrected{' (left unchanged)' if same else ''}</div>
<div class="mono">{html.escape(k['corrected'])}</div><div class="why">{html.escape(k['why'])}</div>"""
    blocks = "".join(f"""<div class="ex"><h2>Example {n}</h2>
<div class="lab">Kannada</div><div class="kn">{html.escape(e['native'])}</div>
<div class="lab">English</div><div>{html.escape(e['english'])}</div>
{kind_block(e, 'natural', 'Natural romanization')}{kind_block(e, 'kanglish', 'Kanglish')}</div>"""
                     for n, e in enumerate(E, 1))
    note = ("These examples are for the items where you see drafts (Part 2). In Part 1 you see no drafts: write both "
            "versions yourself the way you would type them." if role["mode"] == "double" else "")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Worked examples</title><style>{CSS}</style></head>
<body><h1>Worked examples</h1><div class="sub">Three sentences that are <b>not</b> among the items you will
annotate. Each shows the AI draft, how to rate it (before changing anything), and a good correction. Ratings are
your own judgement: these show the idea, not the only right answer. {note}</div>{blocks}</body></html>"""
    out.write_text(doc, encoding="utf-8")


def md_html(md: Path, out: Path) -> None:
    """Minimal Markdown (headings, lists, bold, paragraphs) for the instruction files."""
    lines, body, lst, prev = md.read_text(encoding="utf-8").splitlines(), [], None, ""

    def inline(t):
        t = html.escape(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        return re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    for ln in lines + [""]:
        m_ul, m_ol = re.match(r"^(\s*)- (.*)", ln), re.match(r"^(\s*)\d+\. (.*)", ln)
        if m_ul or m_ol:
            tag = "ul" if m_ul else "ol"
            if lst != tag:
                if lst:
                    body.append(f"</{lst}>")
                body.append(f"<{tag}>")
                lst = tag
            body.append(f"<li>{inline((m_ul or m_ol).group(2))}</li>")
            continue
        if ln.startswith("  ") and lst:  # continuation line of a list item
            body[-1] = body[-1][:-5] + " " + inline(ln.strip()) + "</li>"
            continue
        if lst:
            body.append(f"</{lst}>")
            lst = None
        if ln.startswith("## "):
            body.append(f"<h2>{inline(ln[3:])}</h2>")
        elif ln.startswith("# "):
            body.append(f"<h1>{inline(ln[2:])}</h1>")
        elif ln.strip() and prev.strip() and body and body[-1].startswith("<p>"):  # paragraph continues
            body[-1] = body[-1][:-4] + " " + inline(ln) + "</p>"
        elif ln.strip():
            body.append(f"<p>{inline(ln)}</p>")
        prev = ln
    out.write_text(f"""<!doctype html><html><head><meta charset="utf-8"><title>Instructions</title><style>{CSS}
body {{ font-size: 12px; }} li {{ margin: 2px 0; }}</style></head><body>{''.join(body)}</body></html>""",
                   encoding="utf-8")


WHATSAPP = {  # ready to paste; times set by Aarnav 2026-10-25
    "annotator_A": """Hi {first}! Thank you so much for helping with the Kannada project 🙏

I'm attaching a zip file (A.zip). Please unzip it on your laptop/desktop. Inside:
• annotate_v2.html: the annotation page (open it in Chrome or Edge)
• quick_start.pdf: one page with pictures of every step (please read this first)
• worked_examples.pdf: 3 examples of how to rate and correct
• instructions.pdf: the full instructions

Before you start: please read the 3 worked examples and check them. If anything looks wrong (a rating, a correction, a spelling), tell me what and why. Then start annotating.

What you'll do: for each of 500 sentences you see the Kannada, the English, and two AI-written versions (Kannada typed in English letters, and Kanglish). Rate each one first, then correct it so it sounds the way people really type.

Time: about 2 minutes per item, so about 15 hours in total. About 25 items a day (under an hour) works well. Short sessions are fine: everything is saved to your CSV file after each item.

Sending it back: at the end of each week, send me your CSV file here on WhatsApp (attach it as a Document).

Please don't use Google Translate, AI tools or dictionaries, and don't discuss the sentences with anyone. Any question, just message me!""",
    "annotator_B_part1": """Hi {first}! Thank you so much for helping with the Kannada project 🙏

I'm attaching a zip file (B_part1.zip). Please unzip it on your laptop/desktop. Inside:
• annotate_v2.html: the annotation page (open it in Chrome or Edge)
• quick_start.pdf: one page with pictures of every step (please read this first)
• instructions.pdf: the full instructions

What you'll do (100 sentences):
1) First 40: you only see a Kannada sentence. Type it yourself in English letters, the way you'd type on your phone, and also write it as Kanglish. Please do all 40 first, and don't click ahead.
2) Other 60: you see AI-written versions. Rate each one first, then correct it. Before you start these, I'll send you a short file with 3 worked examples.

Important: in the page, choose "Second annotator (100 items)", never "All 500 items".

Time: about 2 minutes per item, so about 3 hours in total. Short sessions are fine: everything is saved to your CSV file after each item.

Sending it back: as soon as the first 40 are done, send me your CSV file here on WhatsApp (attach it as a Document) and wait for the examples file. Send the CSV again when you finish.

Please don't use Google Translate, AI tools or dictionaries, and don't discuss the sentences with anyone. Any question, just message me!""",
    "annotator_B_part2": """Thanks {first}, got your first 40! 🙏

Here is B_part2.zip with worked_examples.pdf: 3 examples of how to rate an AI-written version and then correct it. Please read it, then carry on with the other 60 sentences in the same page and the same CSV file (open the page, enter the same name, choose "Second annotator (100 items)", click "Continue a CSV file…" and pick your file, then "First unfinished").

Rate each version first, before changing anything, then correct it. About 2 minutes per item. Send me the CSV here when you finish. Any question, just message me!""",
}


# ---------------------------------------------------------------- build

def build() -> None:
    E = load_examples()
    work = Path(tempfile.mkdtemp(prefix="kpkg_work_"))
    demo = work / "demo.html"
    demo_page(E, demo)
    c = Chrome()
    try:
        for role_id, role in ROLES.items():
            d = DIST / role_id
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)
            shutil.copyfile(PAGE, d / "annotate_v2.html")
            shots = work / role_id
            steps = screenshots(c, demo, role, E, shots)
            quickstart_html(role, steps, shots / "quick_start.html", 2)
            for scale in (1.0, 0.95, 0.9, 0.85, 0.8):  # largest print scale that keeps it to one page
                if c.pdf((shots / "quick_start.html").as_uri(), d / "quick_start.pdf", scale) == 1:
                    break
            else:
                raise SystemExit(f"{role_id}: quick start does not fit one page")
            examples_html(role, E, shots / "worked_examples.html")
            c.pdf((shots / "worked_examples.html").as_uri(), d / "worked_examples.pdf")
            md_html(role["md"], shots / "instructions.html")
            c.pdf((shots / "instructions.html").as_uri(), d / "instructions.pdf")
            for p, _ in steps:  # keep the screenshots next to the PDF for reuse
                (d / "screenshots").mkdir(exist_ok=True)
                shutil.copyfile(p, d / "screenshots" / p.name)
            for key, text in WHATSAPP.items():
                if key.startswith(role_id):
                    name = "whatsapp_message" + key[len(role_id):] + ".txt"
                    (d / name).write_text(text.replace("{first}", "[name]"), encoding="utf-8")
            # A.zip: everything (A checks the examples first). B: part 1 without the worked examples (for the 40
            # blind items); part 2 = the examples only, sent after B's 40 blind items and A's check of the examples.
            zips = {"annotator_A": {"A.zip": ("annotate_v2.html", "quick_start.pdf", "worked_examples.pdf",
                                              "instructions.pdf")},
                    "annotator_B": {"B_part1.zip": ("annotate_v2.html", "quick_start.pdf", "instructions.pdf"),
                                    "B_part2.zip": ("worked_examples.pdf",)}}[role_id]
            for zname, files in zips.items():
                z = DIST / zname
                with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
                    for f in files:
                        zf.write(d / f, f"{role_id}/{f}")
                print(role_id, "steps", len(steps), "->", z.relative_to(REPO), z.stat().st_size, "bytes")
    finally:
        c.close()
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    build()
