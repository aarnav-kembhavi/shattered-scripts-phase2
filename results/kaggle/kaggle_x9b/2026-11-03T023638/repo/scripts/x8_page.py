"""X8 blind second-annotator page (registered in RESULTS.md, Phase 2 pre-registration X8; n = 100 by amendment 1).

Items: 100 Kannada FLORES+ sentences from the 496 retained natural-sample sentences (data/processed/natural_flores_m4_500_v1.jsonl,
non-defective), chosen with default_rng(8), preferring sentences that are not among the 300 annotated FLORES items (data/annotation/items_v2.jsonl);
only if fewer than 100 remain are annotated ones added (counted). Annotators P and Q (role letters only) each write a natural romanization from
scratch, seeing only the Kannada sentence: the page contains no Gemini text, no English translation and no label. JSON export, progress kept in
localStorage. One self-contained file: annotation/annotate_blind_v1.html; selection in results/phase2/x8/selection.json (ids only).
Usage: python scripts/x8_page.py [--preview]
"""
import argparse
import json

import numpy as np

from shattered.runlog import REPO, results_dir, write_json

OUT = REPO / "annotation" / "annotate_blind_v1.html"
PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Typing Kannada in English letters</title><style>
body{font-family:system-ui,sans-serif;max-width:46rem;margin:1.5rem auto;padding:0 1rem;line-height:1.5;color:#1b1b1b;background:#fff}
.banner{color:#1b1b1b;background:#fff3cd;border:1px solid #e0c36a;padding:.5rem .8rem;border-radius:6px;margin-bottom:1rem}
.kn{font-size:1.4rem;padding:1rem;border:1px solid #bbb;border-radius:8px;margin:1rem 0;background:#fafafa}
textarea{width:100%;font-size:1.1rem;padding:.6rem;border:1px solid #888;border-radius:6px;box-sizing:border-box;min-height:5rem}
button{font-size:1rem;padding:.55rem 1rem;border-radius:6px;border:1px solid #444;background:#222;color:#fff;cursor:pointer;margin-right:.4rem}
button:disabled{opacity:.4} .bar{height:6px;background:#ddd;border-radius:3px;margin:.5rem 0} .bar div{height:6px;background:#2a6;border-radius:3px}
select,input{font-size:1rem;padding:.3rem}
@media (prefers-color-scheme:dark){body{background:#151515;color:#eee}.kn{background:#1e1e1e;border-color:#555}textarea,select,input{background:#222;color:#eee}}
</style></head><body>
<h1>Typing Kannada in English letters</h1>
__BANNER__
<div id="start"><p>You will see __N__ Kannada sentences, one at a time. For each, type it the way <b>you</b> would type it in a WhatsApp message to a friend, using English
letters only (no Kannada script, no accents). Keep every word and the word order; do not translate or shorten. There is no single right spelling: write it your way.
Please do not use a translator, an AI tool or a dictionary, and do not discuss the sentences with anyone. Turn off autocorrect and automatic capital letters on your keyboard.</p>
<p>You are annotator: <select id="who"><option value="">choose</option><option>P</option><option>Q</option></select></p><button id="go">Start</button></div>
<div id="task" hidden><div class="bar"><div id="prog"></div></div><div id="count"></div><div class="kn" id="kn"></div>
<textarea id="ans" spellcheck="false" autocapitalize="off" autocorrect="off" placeholder="Type the sentence in English letters"></textarea>
<p><button id="back">Back</button><button id="next" disabled>Next</button><button id="save">Save a backup file (JSON)</button></p></div>
<div id="end" hidden><h2>Finished</h2><p>Thank you. Download your answers and send the file as instructed.</p><button id="dl">Download answers (JSON)</button></div>
<script>
const ITEMS=__ITEMS__, KEY="x8_blind__KEYSUF__";
let st=JSON.parse(localStorage.getItem(KEY)||"null")||{i:0,who:"",ans:{}};
const $=id=>document.getElementById(id);
function save(){localStorage.setItem(KEY,JSON.stringify(st));}
function show(){ if(st.i>=ITEMS.length){$("task").hidden=true;$("end").hidden=false;return;}
 $("start").hidden=true;$("task").hidden=false;$("count").textContent=(st.i+1)+" of "+ITEMS.length;$("prog").style.width=(100*st.i/ITEMS.length)+"%";
 $("kn").textContent=ITEMS[st.i].native;$("ans").value=st.ans[ITEMS[st.i].index]||"";$("next").disabled=!$("ans").value.trim();$("back").disabled=st.i==0;$("ans").focus();}
function out(){return JSON.stringify({annotator:st.who,n:Object.keys(st.ans).length,answers:ITEMS.filter(x=>st.ans[x.index]!==undefined).map(x=>({index:x.index,romanization:st.ans[x.index]}))},null,1);}
function dl(){const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([out()],{type:"application/json"}));a.download="x8_annotator_"+st.who+".json";a.click();}
$("ans").oninput=()=>{$("next").disabled=!$("ans").value.trim();};
$("go").onclick=()=>{st.who=$("who").value;if(!st.who){alert("Please choose P or Q");return;}save();show();};
$("next").onclick=()=>{st.ans[ITEMS[st.i].index]=$("ans").value.trim();st.i++;save();show();};
$("back").onclick=()=>{if(st.i>0){st.ans[ITEMS[st.i].index]=$("ans").value.trim();st.i--;save();show();}};
$("save").onclick=()=>{st.ans[ITEMS[st.i].index]=$("ans").value.trim();save();dl();};
$("dl").onclick=dl;
if(st.who&&st.i>0){$("who").value=st.who;show();}
</script></body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    rows = [json.loads(l) for l in (REPO / "data" / "processed" / "natural_flores_m4_500_v1.jsonl").open(encoding="utf-8")]
    kept = [r for r in rows if not r["defective"]]
    annotated = {int(json.loads(l)["id"].split("-")[1]) for l in (REPO / "data" / "annotation" / "items_v2.jsonl").open(encoding="utf-8")
                 if json.loads(l)["id"].startswith("flores-")}
    fresh = [r for r in kept if r["index"] not in annotated]
    rng = np.random.default_rng(8)
    pick = [fresh[j] for j in rng.choice(len(fresh), 100, replace=False)] if len(fresh) >= 100 else None
    assert pick is not None, f"only {len(fresh)} unannotated sentences"
    items = [{"index": r["index"], "native": r["native"]} for r in pick]  # no Gemini text, no translation
    if a.preview:
        items = items[:5]
    page = (PAGE.replace("__BANNER__", '<div class="banner"><b>PREVIEW.</b> Five of the 100 sentences, for layout review only. Nothing is collected before it is sent out.</div>' if a.preview else "")
            .replace("__N__", "100").replace("__ITEMS__", json.dumps(items, ensure_ascii=False)).replace("__KEYSUF__", "_preview" if a.preview else ""))
    assert "natural" not in json.dumps(items)
    (REPO / "annotation" / ("preview_blind_v1.html" if a.preview else "annotate_blind_v1.html")).write_text(page, encoding="utf-8")
    if not a.preview:
        write_json(results_dir("phase2/x8") / "selection.json", {"n": 100, "seed": 8, "indices": [r["index"] for r in pick],
                   "retained_496": len(kept), "annotated_excluded": len(kept) - len(fresh), "unannotated_available": len(fresh)},
                   {"status": "page built, not sent; contains no Gemini text"})
    print("kept", len(kept), "unannotated", len(fresh), "picked", len(pick))


if __name__ == "__main__":
    main()
