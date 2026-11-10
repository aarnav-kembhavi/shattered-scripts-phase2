"""Collision-rate summary (the lead author, 2026-11-02): the Phase 1 definition is the value used everywhere; the literal reading
("share of types in a collision group") is recorded as a footnote value only. Reads results/phase2/x4/fetch/collision_rates.json."""
import json
from shattered.runlog import REPO, write_json
d = json.load(open(REPO / "results/phase2/x4/fetch/collision_rates.json", encoding="utf-8"))
out = {l: {"collision_rate": v["merged_frac"], "footnote_literal_share_in_a_collision_group": v["share_of_types_in_a_collision_group"],
           "native_types": v["native_types"], "lossy_types": v["lossy_types"], "types_unmapped_excluded": v["types_unmapped_excluded"]}
       for l, v in d.items() if l != "provenance"}
write_json(REPO / "results/phase2/x4/fetch/collision_rates_summary.json", out,
           {"primary": "collision_rate = 1 - lossy word types / native word types (Phase 1 definition, 10.4% for Kannada)",
            "footnote": "share of native types whose lossy form is shared with another type (literal registered wording); reported as a footnote value only",
            "decision": "the lead author 2026-11-02"})
for l, v in out.items():
    print(l, round(v["collision_rate"], 4), round(v["footnote_literal_share_in_a_collision_group"], 4))
