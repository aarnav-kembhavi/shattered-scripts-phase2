"""Annotator packages, VERIFY version (protocol change of 2026-10-26, RESULTS.md: fine / wrong + fix; Rater C dropped).
The rate-and-correct packages of 2026-10-25 are in git history only.

  annotation/dist/A/        annotator_A.xlsx (500 items, 3 example rows at the top), instructions.pdf     -> A.zip
  annotation/dist/B_part1/  annotator_B_part1.xlsx (40 blind items: Kannada and English, no Gemini text),
                            instructions.pdf                                                           -> B_part1.zip
  annotation/dist/B_part2/  annotator_B_part2.xlsx (B's other 60, verify layout)                       -> B_part2.zip
                            (send only after B's 40 blind items are in and A has confirmed the examples)
  annotation/dist/messages/ WhatsApp texts for A, B part 1, B part 2 (for Aarnav; not in any zip)

Workbooks come from scripts/k_xlsx.py (run `build` first); before packaging, every workbook must pass the XML check
(answer cells empty, nothing hidden) and B part 1 the draft leak check. Instructions are printed by headless Chrome.

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


# ---------------------------------------------------------------- packages

WHATSAPP = {  # ready to paste (Aarnav, 2026-10-26: verify task, about 20 seconds per item; B part 1 about 1.5 hours)
    "A": """Hi [name]! Thank you so much for helping with the Kannada project 🙏

The file I sent earlier is replaced: please delete it and use this one (A.zip). Unzip it on your laptop/desktop. Inside:
• annotator_A.xlsx: your file (open it in Excel)
• instructions.pdf: the instructions (short)

The new task is much faster: for each sentence you see two versions typed in English letters (natural and Kanglish). For each one just pick "fine" or "wrong" from the dropdown, and if it is wrong type your fix. About 20 seconds per item, so about 3 hours in total.

First, within a day: look at the 3 shaded EXAMPLE rows at the top of the sheet "items" and reply to me "examples ok", or send me your corrections. Then start the items.

Before typing, please turn off AutoCorrect in Excel (File > Options > Proofing > AutoCorrect Options: untick the capitals options and "Replace text as you type"), and keyboard autocorrect if you use your phone.

Sending it back: save as .xlsx (never CSV) and send me the file here on WhatsApp (as a Document) every week.

Please don't use AI or translation tools, and don't discuss the sentences with anyone. Any question, just message me!""",
    "B_part1": """Hi [name]! Thank you so much for helping with the Kannada project 🙏

The part 1 file I sent earlier is replaced: please delete it and use this one (B_part1.zip). Unzip it on your laptop/desktop. Inside:
• annotator_B_part1.xlsx: your file (open it in Excel)
• instructions.pdf: the instructions (short)

Part 1: 40 sentences. For each Kannada sentence, type it your own way in English letters, the way you would on WhatsApp, and also as Kanglish. There's no right spelling, just type it how you really would, and please don't look anything up. About 1.5 hours.

Before typing, please turn off AutoCorrect in Excel (File > Options > Proofing > AutoCorrect Options: untick the capitals options and "Replace text as you type"), and keyboard autocorrect if you use your phone.

As soon as all 40 are done, save as .xlsx (never CSV) and send me the file here on WhatsApp (as a Document). Then I'll send you part 2.

Please don't use AI or translation tools, and don't discuss the sentences with anyone. Any question, just message me!""",
    "B_part2": """Thanks [name], got your 40! 🙏

Here is B_part2.zip with annotator_B_part2.xlsx: the 60 checks. For each sentence you see two versions typed in English letters (natural and Kanglish). Pick "fine" or "wrong" from the dropdown, and if it is wrong type your fix. The 3 shaded EXAMPLE rows at the top show how. About 20 seconds each.

Keep AutoCorrect off as before. Save as .xlsx (never CSV) and send me the file here when you finish. Any question, just message me!""",
}

PACKAGES = {  # zip: (folder, workbook, instructions markdown or None)
    "A.zip": ("A", "annotator_A.xlsx", "annotator_A.md"),
    "B_part1.zip": ("B_part1", "annotator_B_part1.xlsx", "annotator_B.md"),
    "B_part2.zip": ("B_part2", "annotator_B_part2.xlsx", None),
}


def build() -> None:
    import k_xlsx as K
    for _, book, _ in PACKAGES.values():
        assert (XLSX / book).exists(), f"run scripts/k_xlsx.py build first ({book} missing)"
        assert K.xmlcheck(XLSX / book)["clean"], f"{book}: answer cells not empty or something hidden"
    assert not K.leakcheck(XLSX / "annotator_B_part1.xlsx")["hits"], "B part 1 contains Gemini draft text"
    work = Path(tempfile.mkdtemp(prefix="kpkg_verify_"))
    if DIST.exists():  # the rate-and-correct packages of 2026-10-25 (git history only)
        shutil.rmtree(DIST)
    (DIST / "messages").mkdir(parents=True)
    c = Chrome()
    try:
        for z, (folder, book, md) in PACKAGES.items():
            d = DIST / folder
            d.mkdir()
            shutil.copyfile(XLSX / book, d / book)
            files = [book]
            if md:
                md_html(ANN / "instructions" / md, work / f"{folder}.html")
                c.pdf((work / f"{folder}.html").as_uri(), d / "instructions.pdf")
                files.append("instructions.pdf")
            with zipfile.ZipFile(DIST / z, "w", zipfile.ZIP_DEFLATED) as zf:
                for f in files:
                    zf.write(d / f, f"{folder}/{f}")
            print(z, files, (DIST / z).stat().st_size, "bytes")
    finally:
        c.close()
    for k, t in WHATSAPP.items():
        (DIST / "messages" / f"whatsapp_{k}.txt").write_text(t, encoding="utf-8")
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    build()
