"""Annotator packages, Excel version (protocol change of 2026-10-25, RESULTS.md; the HTML packages of 2026-10-24 were
never sent and are in git history only).

  annotation/dist/A/        annotator_A.xlsx (500 items + worked_examples sheet to check first), quick_start.pdf,
                            instructions.pdf                                                   -> A.zip
  annotation/dist/B_part1/  annotator_B_part1.xlsx (40 blind items, no Gemini draft anywhere), quick_start.pdf,
                            instructions.pdf                                                   -> B_part1.zip
  annotation/dist/B_part2/  annotator_B_part2.xlsx (60 items with drafts), worked_examples.xlsx, quick_start.pdf
                            -> B_part2.zip (send only after B's 40 blind items are in and A has confirmed the examples)
  annotation/dist/messages/ WhatsApp texts for A, B part 1, B part 2 (for Aarnav; not in any zip)

Workbooks come from scripts/k_xlsx.py (run `build` first). Quick-start pictures are Excel's own rendering of DEMO
workbooks that hold only the worked-example items (never one of the 500), captured with scripts/xlshot.ps1 (Excel
COM); the one-page PDFs are printed by headless Chrome. Rater C's workbook is built later (k_xlsx.py rater).

Usage: python scripts/k_package.py      (A, B part 1, B part 2; already sent, do not rebuild)
       python scripts/k_package.py c    (Rater C: message now; package once rater_C.xlsx is filled)
"""
from __future__ import annotations

import base64
import html
import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

import websocket

REPO = Path(__file__).resolve().parents[1]
ANN = REPO / "annotation"
DIST = ANN / "dist"
XLSX = ANN / "xlsx"
CHROME = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
sys.path[:0] = [str(ANN), str(REPO / "scripts")]
import merge_xlsx as M  # noqa: E402

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




# ---------------------------------------------------------------- pictures of the workbooks (Excel's own rendering)

def demo_books(work: Path) -> dict:
    """Demo workbooks with the worked-example items only, filled the way an annotator would."""
    import k_xlsx as K
    from openpyxl import Workbook
    E = json.load(open(ANN / "examples_v1.json", encoding="utf-8"))["examples"]
    e1, e3 = E[0], E[2]
    row = {"item_id": e1["id"], "source": "flores_sib", "native": e1["native"], "english": e1["english"],
           "natural_draft": e1["natural"]["draft"], "natural_naturalness": int(e1["natural"]["naturalness"]),
           "natural_meaning": e1["natural"]["meaning"], "natural_corrected": e1["natural"]["corrected"],
           "kanglish_draft": e1["kanglish"]["draft"], "kanglish_corrected": e1["kanglish"]["draft"]}
    books = {}
    wb = Workbook()
    K.readme_sheet(wb, K.README["A"])
    wb[M.README][M.NAME_CELL] = "Annotator A"
    K.data_sheet(wb, M.ITEMS, M.DRAFT_SHEET, [row])
    ex = K.example_rows()
    ex[0]["check"] = "OK"
    K.data_sheet(wb, M.EXAMPLES, M.EXAMPLES_SHEET + M.EXAMPLES_CHECK, ex)
    books["A"] = work / "demo_A.xlsx"
    wb.save(books["A"])
    wb = Workbook()
    K.readme_sheet(wb, K.README["B1"])
    wb[M.README][M.NAME_CELL] = "Annotator B"
    K.data_sheet(wb, M.ITEMS, M.BLIND_SHEET, [{"item_id": e3["id"], "native": e3["native"],
                                               "natural_corrected": "apartment olagade yaaru iralilla.",
                                               "kanglish_corrected": "apartment olage yaru irlilla"}])
    books["B1"] = work / "demo_B1.xlsx"
    wb.save(books["B1"])
    wb = Workbook()
    K.readme_sheet(wb, K.README["B2"])
    wb[M.README][M.NAME_CELL] = "Annotator B"
    K.data_sheet(wb, M.ITEMS, M.DRAFT_SHEET, [row])
    books["B2"] = work / "demo_B2.xlsx"
    wb.save(books["B2"])
    return books


def shot(book: Path, sheet: str, rng: str, png: Path) -> Path:
    """Excel's picture of a range; the clipboard copy is occasionally blank, so blank pictures are retaken."""
    from PIL import Image
    for _ in range(4):
        png.unlink(missing_ok=True)
        p = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                            str(REPO / "scripts/xlshot.ps1"), "-book", str(book), "-sheet", sheet, "-range", rng,
                            "-png", str(png)], capture_output=True, text=True)
        if png.exists():
            im = Image.open(png).convert("RGBA").convert("L")
            inner = im.crop((4, 4, im.width - 4, im.height - 4))  # a blank picture is white inside its frame
            dark = sum(inner.histogram()[:200]) / max(1, inner.width * inner.height)
            if dark > 0.005:
                return png
        time.sleep(2)
    raise SystemExit(f"Excel picture failed for {book.name}!{rng}: {p.stdout[-300:]} {p.stderr[-300:]}")


# ---------------------------------------------------------------- documents

def quickstart(title: str, intro: str, steps: list, foot: str, out: Path, first: str = "") -> None:
    cells = "".join(f'<div class="step"><span class="n">{k}</span>{cap}'
                    + "".join(f'<img src="{p.name}">' for p in imgs) + "</div>"
                    for k, (cap, imgs) in enumerate(steps, 1))
    out.write_text(f"""<!doctype html><html><head><meta charset="utf-8"><title>Quick start</title><style>{CSS}
.grid {{ grid-template-columns: 1fr; gap: 6px; }} .step img {{ max-height: 230px; width: auto; max-width: 100%; }}
</style></head><body><h1>{title}</h1><div class="sub">{intro}</div>{first}<div class="grid">{cells}</div>
<div class="foot">{foot}</div></body></html>""", encoding="utf-8")


AUTOCORRECT = ("<b>Turn off AutoCorrect before typing.</b> In Excel: File &gt; Options &gt; Proofing &gt; AutoCorrect "
               "Options, and untick <i>Correct TWo INitial CApitals</i>, <i>Capitalize first letter of sentences</i> "
               "and <i>Replace text as you type</i>. On a phone or tablet, also turn off autocorrect and automatic "
               "capitals in your keyboard settings.")
NAME = "Open the file. On the sheet <b>READ_ME</b>, type your name in the yellow cell (the same name every time)."
SAVE = ("<b>Save</b> with Ctrl+S as an Excel Workbook (<b>.xlsx</b>), never as CSV. You can close and reopen the file "
        "any time: your work is in the file.")
RULES = ("<b>Rules:</b> type the way you really type; there is no single correct spelling. No translation tools, AI "
         "tools or dictionaries. Do not discuss items with anyone. Use the Note column for anything odd. Only the "
         "yellow cells can be changed. Questions or problems: ask Aarnav.")


WHATSAPP = {  # ready to paste (Aarnav, 2026-10-25: about 2 minutes per item; A about 15 hours, B about 3 hours)
    "A": """Hi [name]! Thank you so much for helping with the Kannada project 🙏

I'm attaching A.zip. Please unzip it on your laptop/desktop. Inside:
• annotator_A.xlsx: your annotation file (open it in Excel)
• quick_start.pdf: one page with every step (please read this first)
• instructions.pdf: the full instructions

First, today or tomorrow: open the sheet "worked_examples" in annotator_A.xlsx and check the 3 examples. For each one choose OK, or "needs correction" and write what you would change. Save the file and send it back to me within a day, as a separate message, before you start the main items.

Then the main work: for each of 500 sentences you see the Kannada, the English, and two AI-written versions (Kannada typed in English letters, and Kanglish). Rate each one first with the dropdowns, then correct it so it sounds the way people really type.

Before typing, please turn off AutoCorrect in Excel (File > Options > Proofing > AutoCorrect Options: untick "Correct TWo INitial CApitals", "Capitalize first letter of sentences" and "Replace text as you type"), and keyboard autocorrect if you use your phone.

Time: about 2 minutes per item, so about 15 hours in total. About 25 items a day (under an hour) works well; short sessions are fine.

Sending it back: save as .xlsx (never CSV) and send me the file here on WhatsApp (as a Document) at the end of each week.

Please don't use Google Translate, AI tools or dictionaries, and don't discuss the sentences with anyone. Any question, just message me!""",
    "B_part1": """Hi [name]! Thank you so much for helping with the Kannada project 🙏

I'm attaching B_part1.zip. Please unzip it on your laptop/desktop. Inside:
• annotator_B_part1.xlsx: your file for part 1 (open it in Excel)
• quick_start.pdf: one page with every step (please read this first)
• instructions.pdf: the full instructions

Part 1 (40 sentences): you only see a Kannada sentence. For each one, type it yourself in English letters, the way you'd type on your phone, and also write it as Kanglish. Nothing to rate. Please don't look anything up.

Before typing, please turn off AutoCorrect in Excel (File > Options > Proofing > AutoCorrect Options: untick "Correct TWo INitial CApitals", "Capitalize first letter of sentences" and "Replace text as you type"), and keyboard autocorrect if you use your phone.

Time: about 2 minutes per item, so about 3 hours for all 100 sentences across both parts.

Sending it back: as soon as all 40 are done, save as .xlsx (never CSV) and send me the file here on WhatsApp (as a Document). I'll then send you part 2 (the other 60).

Please don't use Google Translate, AI tools or dictionaries, and don't discuss the sentences with anyone. Any question, just message me!""",
    "B_part2": """Thanks [name], got your first 40! 🙏

Here is B_part2.zip, with:
• worked_examples.xlsx: 3 examples of how to rate an AI-written version and then correct it (please read this first)
• annotator_B_part2.xlsx: the other 60 sentences
• quick_start.pdf: the steps for part 2

For each sentence you see the Kannada, the English, and two AI-written versions. Rate each one first with the dropdowns, then correct it so it sounds the way people really type. Type your name in the yellow cell on READ_ME, as before, and keep AutoCorrect off.

About 2 minutes per item. Save as .xlsx (never CSV) and send me the file here when you finish. Any question, just message me!""",
}


def build() -> None:
    for name in ("annotator_A.xlsx", "annotator_B_part1.xlsx", "annotator_B_part2.xlsx", "worked_examples.xlsx"):
        assert (XLSX / name).exists(), f"run scripts/k_xlsx.py build first ({name} missing)"
    work = Path(tempfile.mkdtemp(prefix="kpkg_xlsx_"))
    books = demo_books(work)
    img = lambda key, sheet, rng, name: shot(books[key], sheet, rng, work / name)
    # remove the HTML-era packages and anything older from dist (kept in git history)
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "messages").mkdir(parents=True)
    c = Chrome()
    try:
        # ---- A
        qs = [(AUTOCORRECT, []),
              (NAME, [img("A", M.README, "A1:B7", "a_readme.png")]),
              ("In the sheet <b>items</b> (one row per item): <b>rate each draft first</b>, before changing anything: "
               "choose naturalness 1&ndash;5 and keeps-the-meaning yes/no from the dropdowns. <b>Then correct</b> the "
               "draft in <i>your corrected version</i> (it starts as a copy of the draft; leave it if it is fine). Do "
               "the same for the Kanglish draft.", [img("A", M.ITEMS, "E1:H2", "a_items.png")]),
              (SAVE + " <b>Send the .xlsx to Aarnav at the end of each week</b> (WhatsApp, as a Document).", [])]
        first = ('<div class="foot" style="margin:0 0 8px; background:#fdf1e6; border:1px solid #e8b48a">'
                 '<span class="n" style="background:#a4400b">0</span><b>First, within a day: check the 3 worked '
                 'examples.</b> Open the sheet <b>worked_examples</b>. For each row choose <b>OK</b> or <b>needs '
                 'correction</b> (and write your correction in the last column). Save and send the file to Aarnav, '
                 'then start the items.' f'<img src="a_examples.png" style="width:100%; margin-top:4px"></div>')
        img("A", M.EXAMPLES, "I1:L3", "a_examples.png")
        d = DIST / "A"
        d.mkdir()
        shutil.copyfile(XLSX / "annotator_A.xlsx", d / "annotator_A.xlsx")
        quickstart("Quick start: Annotator A (500 items, Excel)", "You need <b>annotator_A.xlsx</b> and Excel. Full "
                   "instructions: <b>instructions.pdf</b>. About 2 minutes per item; about 25 items a day works well.",
                   qs, RULES, work / "qs_A.html", first)
        one_page(c, work / "qs_A.html", d / "quick_start.pdf")
        md_html(ANN / "instructions/annotator_A.md", work / "ins_A.html")
        c.pdf((work / "ins_A.html").as_uri(), d / "instructions.pdf")
        # ---- B part 1 (no draft text anywhere: the demo shows only a worked-example sentence written by hand)
        qs = [(AUTOCORRECT, []),
              (NAME.replace("every time", "in both parts"), [img("B1", M.README, "A1:B7", "b1_readme.png")]),
              ("In the sheet <b>items</b> you see only a Kannada sentence. In the yellow cells, <b>write both versions "
               "yourself</b>, from scratch: natural romanization (word for word, as you type on a phone) and Kanglish. "
               "Nothing to rate. Do all 40.", [img("B1", M.ITEMS, "A1:E2", "b1_items.png")]),
              (SAVE + " <b>As soon as all 40 are done, send the .xlsx to Aarnav</b> (WhatsApp, as a Document). Part 2 "
               "follows after that.", [])]
        d = DIST / "B_part1"
        d.mkdir()
        shutil.copyfile(XLSX / "annotator_B_part1.xlsx", d / "annotator_B_part1.xlsx")
        quickstart("Quick start: Annotator B, part 1 (40 items, Excel)", "You need <b>annotator_B_part1.xlsx</b> and "
                   "Excel. Full instructions: <b>instructions.pdf</b>. About 2 minutes per item.", qs, RULES,
                   work / "qs_B1.html")
        one_page(c, work / "qs_B1.html", d / "quick_start.pdf")
        md_html(ANN / "instructions/annotator_B.md", work / "ins_B.html")
        c.pdf((work / "ins_B.html").as_uri(), d / "instructions.pdf")
        # ---- B part 2
        qs = [("Read <b>worked_examples.xlsx</b> first: 3 examples (not among your items) of an AI draft, how it was "
               "rated, and a good correction.", []),
              ("Open <b>annotator_B_part2.xlsx</b>, type your name in the yellow cell on <b>READ_ME</b> (the same name "
               "as in part 1), and keep AutoCorrect off.", []),
              ("In the sheet <b>items</b>: <b>rate each draft first</b> with the dropdowns (naturalness 1&ndash;5, "
               "keeps the meaning yes/no), <b>then correct</b> it in <i>your corrected version</i> (leave it if it is "
               "fine). Same for the Kanglish draft.", [img("B2", M.ITEMS, "E1:H2", "b2_items.png")]),
              (SAVE + " <b>Send the .xlsx to Aarnav when you finish.</b>", [])]
        d = DIST / "B_part2"
        d.mkdir()
        for f in ("annotator_B_part2.xlsx", "worked_examples.xlsx"):
            shutil.copyfile(XLSX / f, d / f)
        quickstart("Quick start: Annotator B, part 2 (60 items, Excel)", "You need <b>annotator_B_part2.xlsx</b>, "
                   "<b>worked_examples.xlsx</b> and Excel. About 2 minutes per item.", qs, RULES, work / "qs_B2.html")
        one_page(c, work / "qs_B2.html", d / "quick_start.pdf")
    finally:
        c.close()
    for k, t in WHATSAPP.items():
        (DIST / "messages" / f"whatsapp_{k}.txt").write_text(t, encoding="utf-8")
    zips = {"A.zip": ("A", ["annotator_A.xlsx", "quick_start.pdf", "instructions.pdf"]),
            "B_part1.zip": ("B_part1", ["annotator_B_part1.xlsx", "quick_start.pdf", "instructions.pdf"]),
            "B_part2.zip": ("B_part2", ["annotator_B_part2.xlsx", "worked_examples.xlsx", "quick_start.pdf"])}
    for z, (folder, files) in zips.items():
        with zipfile.ZipFile(DIST / z, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                zf.write(DIST / folder / f, f"{folder}/{f}")
        print(z, files, (DIST / z).stat().st_size, "bytes")
    shutil.rmtree(work, ignore_errors=True)


# Rater C (registered K3 design): never told where a version comes from; no mention of Gemini or AI anywhere
WHATSAPP_C = """Hi [name]! Thank you so much for helping with the Kannada project 🙏

I'm attaching C.zip. Please unzip it on your laptop/desktop. Inside:
• rater_C.xlsx: your rating file (open it in Excel)
• instructions.pdf: the instructions (one short page)

For each of 40 Kannada sentences you see two versions typed in English letters, once as natural romanization and once as Kanglish (80 rows). Rate how natural each version sounds, from 1 (nobody would type this) to 5 (exactly how people type on a phone), with the dropdowns. Rate each version on its own; both can get the same rating. Go with your first impression.

Type your name in the yellow cell on the sheet READ_ME. When you finish, save as .xlsx (never CSV) and send me the file here on WhatsApp (as a Document).

Please don't use translation or other online tools, and don't discuss the sentences with anyone. Any question, just message me!"""


def build_c() -> int:
    """Rater C's package, built only after `k_xlsx.py rater` has filled rater_C.xlsx from B's returned blind 40. The
    side mapping stays in data/annotation/k3_rater_key_v1.json and is never packaged. Every XML part of the workbook,
    the instructions and the message are searched for words that say where a version comes from."""
    import k_xlsx as K
    (DIST / "messages").mkdir(parents=True, exist_ok=True)
    msg = DIST / "messages" / "whatsapp_C.txt"
    msg.write_text(WHATSAPP_C, encoding="utf-8")
    book = XLSX / "rater_C.xlsx"
    if not book.exists():
        h = K.wordcheck_c([XLSX / "template_rater_C.xlsx", ANN / "instructions/rater_C.md", msg])
        print({"status": "message written; rater_C.xlsx not built yet (needs B's blind 40)", "forbidden_word_hits": h})
        return 1 if h else 0
    d = DIST / "C"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    shutil.copyfile(book, d / "rater_C.xlsx")
    work = Path(tempfile.mkdtemp(prefix="kpkg_c_"))
    c = Chrome()
    try:
        md_html(ANN / "instructions/rater_C.md", work / "ins_C.html")
        c.pdf((work / "ins_C.html").as_uri(), d / "instructions.pdf")
    finally:
        c.close()
    h = K.wordcheck_c([d / "rater_C.xlsx", ANN / "instructions/rater_C.md", msg])
    if h:
        print({"status": "refused: forbidden words in C's package", "hits": h})
        return 1
    with zipfile.ZipFile(DIST / "C.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for f in ("rater_C.xlsx", "instructions.pdf"):
            zf.write(d / f, f"C/{f}")
    print({"C.zip": (DIST / "C.zip").stat().st_size, "forbidden_word_hits": 0})
    shutil.rmtree(work, ignore_errors=True)
    return 0


def one_page(c, html_path: Path, pdf: Path) -> None:
    for scale in (1.0, 0.95, 0.9, 0.85, 0.8, 0.75):  # largest print scale that keeps it to one page
        if c.pdf(html_path.as_uri(), pdf, scale) == 1:
            return
    raise SystemExit(f"{pdf}: does not fit one page")


if __name__ == "__main__":
    if sys.argv[1:] == ["c"]:
        sys.exit(build_c())
    build()
