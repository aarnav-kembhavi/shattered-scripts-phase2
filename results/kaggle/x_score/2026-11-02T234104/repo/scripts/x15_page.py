"""X15 human intelligibility page generator (drafted 2026-11-02; the sample is fixed by the amendment, nothing is collected before approval).

Selection: 100 SIB-200 Kannada items stratified by category (proportional allocation, largest remainder, default_rng(15)) from the 257 items with
a clean natural romanization. Latin square: four annotator groups g = 0..3; group g sees item i (position in the seeded item order) in form
FORMS[(i + g) % 4], so each annotator sees each item in one form only and every item appears in every form across the four groups. Item
order within a page is a seeded shuffle (default_rng(150 + g)). The true label is NOT in the page. One self-contained HTML file per group
(annotation/x15/annotate_x15_g{g}.html); the annotator picks one of the seven topics and the page offers a CSV download (item id, form, choice,
milliseconds, group, seat), kept in localStorage while working. No names are collected: a seat letter only (the role).
Usage: python scripts/x15_page.py [--preview]     (--preview writes a 6-item banner version to annotation/x15/preview_g0.html)
Output: annotation/x15/, results/phase2/x15/selection.json (ids, categories, form assignment, no labels in the pages)
"""
import argparse
import html
import json
import sys

import numpy as np

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
import e0c_sib as e0c  # noqa: E402
import l_ladder as lad  # noqa: E402

FORMS = ["native", "itrans", "lossy", "natural"]
CATS = e0c.CATS
OUT = REPO / "annotation" / "x15"


def select() -> list[dict]:
    its = lad.sib257_items()["sib"]
    by = {c: [it for it in its if it["label"] == k] for k, c in enumerate(CATS)}
    n = len(its)
    quota = {c: 100 * len(v) / n for c, v in by.items()}
    take = {c: int(q) for c, q in quota.items()}
    for c in sorted(quota, key=lambda c: quota[c] - take[c], reverse=True)[: 100 - sum(take.values())]:
        take[c] += 1
    rng = np.random.default_rng(15)
    pick = []
    for c in CATS:
        idx = rng.choice(len(by[c]), take[c], replace=False)
        pick += [by[c][j] for j in sorted(idx)]
    order = np.random.default_rng(15).permutation(len(pick))
    return [pick[j] for j in order]


def text_of(it: dict, form: str) -> str:
    return it["forms"]["natural257"]["text"] if form == "natural" else it["forms"][form]["text"]


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Topic reading task</title><style>
body{font-family:system-ui,sans-serif;max-width:46rem;margin:1.5rem auto;padding:0 1rem;line-height:1.5;color:#1b1b1b;background:#fff}
.banner{color:#1b1b1b;background:#fff3cd;border:1px solid #e0c36a;padding:.5rem .8rem;border-radius:6px;margin-bottom:1rem}
.text{font-size:1.25rem;padding:1rem;border:1px solid #bbb;border-radius:8px;margin:1rem 0;background:#fafafa;white-space:pre-wrap}
label{display:block;padding:.45rem .6rem;border:1px solid #ccc;border-radius:6px;margin:.3rem 0;cursor:pointer}
label:hover{background:#f0f0f0} input{margin-right:.5rem}
button{font-size:1rem;padding:.55rem 1rem;border-radius:6px;border:1px solid #444;background:#222;color:#fff;cursor:pointer}
button:disabled{opacity:.4} .bar{height:6px;background:#ddd;border-radius:3px;margin:.5rem 0} .bar div{height:6px;background:#2a6;border-radius:3px}
@media (prefers-color-scheme:dark){body{background:#151515;color:#eee}.text{background:#1e1e1e;border-color:#555}label{border-color:#555}label:hover{background:#262626}}
</style></head><body>
<h1>Topic reading task</h1>
__BANNER__
<div id="start"><p>You will see __N__ short texts, one at a time. Each is a sentence in Kannada, written in Kannada script or in English letters.
Choose the topic that fits the text best from the seven options. There are no trick questions and no time limit. Please do not use a
translator or any other tool, and do not discuss the texts with others; this is a measurement of how readable the writing is, not a test of you.</p>
<p>Your seat letter (given to you, not your name): <input id="seat" size="3" maxlength="2"></p><button id="go">Start</button></div>
<div id="task" hidden><div class="bar"><div id="prog"></div></div><div id="count"></div><div class="text" id="txt"></div>
<form id="opts"></form><p><button id="next" disabled>Next</button></p></div>
<div id="end" hidden><h2>Finished</h2><p>Thank you. Download your answers and send the file as instructed.</p><button id="dl">Download answers (CSV)</button></div>
<script>
const ITEMS=__ITEMS__, GROUP=__GROUP__, CATS=__CATS__, KEY="x15_g"+GROUP+"__PREVIEWKEY__";
let st=JSON.parse(localStorage.getItem(KEY)||"null")||{i:0,seat:"",rows:[]}; let t0=0;
const $=id=>document.getElementById(id);
function save(){localStorage.setItem(KEY,JSON.stringify(st));}
function show(){ if(st.i>=ITEMS.length){$("task").hidden=true;$("end").hidden=false;return;}
 $("start").hidden=true;$("task").hidden=false;$("count").textContent=(st.i+1)+" of "+ITEMS.length;$("prog").style.width=(100*st.i/ITEMS.length)+"%";
 $("txt").textContent=ITEMS[st.i].text; $("opts").innerHTML=CATS.map((c,k)=>'<label><input type="radio" name="o" value="'+k+'">'+c+'</label>').join("");
 $("next").disabled=true; t0=Date.now(); document.querySelectorAll("input[name=o]").forEach(r=>r.onchange=()=>$("next").disabled=false);}
$("go").onclick=()=>{st.seat=$("seat").value.trim().toUpperCase();if(!st.seat){alert("Please enter your seat letter");return;}save();show();};
$("next").onclick=e=>{e.preventDefault();const v=document.querySelector("input[name=o]:checked");if(!v)return;
 st.rows.push([ITEMS[st.i].id,ITEMS[st.i].form,CATS[+v.value],Date.now()-t0,GROUP,st.seat]);st.i++;save();show();};
$("dl").onclick=()=>{const csv="item_id,form,choice,ms,group,seat\\n"+st.rows.map(r=>r.map(x=>'"'+String(x).replace(/"/g,'""')+'"').join(",")).join("\\n");
 const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));a.download="x15_g"+GROUP+"_seat"+st.seat+".csv";a.click();};
if(st.i>0||st.rows.length){$("seat").value=st.seat;} if(st.seat&&st.i>0)show();
</script></body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    items = select()
    OUT.mkdir(parents=True, exist_ok=True)
    # the tracked selection file holds ids only: gold labels and the form-by-group mapping are private (annotation/private/x15_keys.json, written by scripts/export_xlsx.py)
    sel = {"n": len(items), "seed": 15, "ids": [it["id"] for it in items]}
    for g in range(4):
        order = np.random.default_rng(150 + g).permutation(len(items))
        rows = [{"id": items[j]["id"], "form": FORMS[(j + g) % 4], "text": text_of(items[j], FORMS[(j + g) % 4])} for j in order]
        if a.preview and g == 0:
            demo = rows[:6]
            page = (PAGE.replace("__BANNER__", '<div class="banner"><b>PREVIEW.</b> Six of the 100 items of group 0, for layout review only. '
                                                'Nothing is collected from this preview.</div>')
                    .replace("__N__", "100").replace("__ITEMS__", json.dumps(demo, ensure_ascii=False)).replace("__GROUP__", "0")
                    .replace("__CATS__", json.dumps(CATS)).replace("__PREVIEWKEY__", "_preview"))
            (OUT / "preview_g0.html").write_text(page, encoding="utf-8")
            continue
        if a.preview:
            continue
        page = (PAGE.replace("__BANNER__", "").replace("__N__", str(len(rows))).replace("__ITEMS__", json.dumps(rows, ensure_ascii=False))
                .replace("__GROUP__", str(g)).replace("__CATS__", json.dumps(CATS)).replace("__PREVIEWKEY__", ""))
        (OUT / f"annotate_x15_g{g}.html").write_text(page, encoding="utf-8")
    if not a.preview:
        write_json(results_dir("phase2/x15") / "selection.json", sel, {"seed": 15, "status": "drafted, not collected; pages contain no labels"})
    cnt = {c: sum(1 for it in items if CATS[it["label"]] == c) for c in CATS}
    print("selected", len(items), cnt)


if __name__ == "__main__":
    main()
