"""Positive controls for the X9b exclusion scan: a planted evaluation sentence must be found (native, ITRANS rendering, English, short line), a clean text must not."""
from shattered.data import x9b_streams as S
from shattered.translit import to_itrans

ev = S.eval_sentences()
kn, en = ev["flores_kn"][5], ev["flores_en"][7]
short = next(s for s in ev["sib_en"] if len(s) < 20) if any(len(s) < 20 for s in ev["sib_en"]) else None
itr = " ".join(to_itrans(w) for w in kn.split())
sets_n, sets_i = ev, {"flores_kn_itrans": [itr], "flores_en": ev["flores_en"]}
idx_n, idx_i = S.Index(sets_n), S.Index(sets_i)
tests = {
    "native planted mid-text": (idx_n.hits("ಪೀಠಿಕೆ ಪಠ್ಯ.\n" + "  ".join(kn.split()) + " ಮುಕ್ತಾಯ")).issuperset({"flores_kn"}),
    "english planted": "flores_en" in idx_n.hits("Intro text. " + en + " Outro."),
    "quote-attached start": "flores_en" in idx_n.hits('He said "' + en + '" yesterday.'),
    "clean text": idx_n.hits("ಇದು ಯಾವುದೇ ಮೌಲ್ಯಮಾಪನ ವಾಕ್ಯವನ್ನು ಹೊಂದಿಲ್ಲ. This is clean.") == set(),
    "ITRANS rendering of the planted sentence": idx_i.hits("x\n" + S.render_itrans("ಪೀಠಿಕೆ " + kn + " ಮುಕ್ತಾಯ")) == {"flores_kn_itrans"},
}
if short:
    tests["short sentence equals a line"] = "sib_en" in idx_n.hits("a\n" + short + "\nb")
for k, v in tests.items():
    print(("PASS " if v else "FAIL "), k)
raise SystemExit(0 if all(tests.values()) else 1)
