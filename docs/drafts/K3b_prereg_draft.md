# DRAFT PRE-REGISTRATION — K3b: Gemini vs native-speaker natural romanization on Dakshina Kannada (draft 2026-10-23; not registered, not run)

To be appended to RESULTS.md only after Aarnav approves it. No Dakshina text has been sent to Gemini.

**Question.** Does Gemini, given the same prompt used for our natural drafts, romanize Kannada the way native speakers
do? K3 tests this on 40 blind items rated by Rater C. K3b tests it at scale on independent human romanizations, by
spelling statistics instead of ratings.

**Data.** Dakshina v1.0, official release (`storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar`, MD5
verified 2026-10-23; CC BY-SA 4.0), `kn/romanized/kn.romanized.rejoined.tsv`. These are 10,000 Kannada Wikipedia strings
romanized by native-speaker annotators (strings of 30+ words were split for annotation and rejoined). Dev and test are
5,000 each. None overlaps any of our evaluation items (checked 2026-10-23).
- **Sample:** 500 strings drawn with `numpy.random.default_rng(6)` from the 10,000. Excluded before drawing: duplicate
  native strings (23) and strings of fewer than 3 native words. The exclusion counts are logged.

**Gemini outputs.**
- **Primary:** `gemini-3.5-flash-lite`, prompt `natural_romanization_v1` (identical to our natural drafts), temperature
  0, cached.
- **Defects:** a defective output (any Indic-script or new non-ASCII character, as `defective()`) gets attempts 2–3, as
  for E0. Strings still defective are excluded and counted.
- **Resample reference:** a random 200 of the 500 (`default_rng(7)`) get two more samples at temperature 1.0 with the
  same prompt (G1, G2). This measures how much Gemini's own spelling varies.

**Normalization.** Both sides are lowercased. Statistics are computed on Latin letters only.

**Measures.** All are per string, over the sample, with paired bootstrap CIs (10,000 resamples over strings).
- **chrF** (sacrebleu, char order 6, word order 0, β = 2) of Gemini against the human romanization. Reported next to
  chrF(G1, G2) on the 200 resample strings. Descriptive, no threshold. Dakshina has one romanization per string, so
  there is no human–human reference.
- **Vowel doubling:** occurrences of aa, ee, ii, oo, uu per 100 letters.
- **h-digraphs:** kh, gh, chh, jh, th, dh, ph, bh per 100 letters. This counts aspiration marking, but "th"/"dh" are
  also used for dental t/d, so the measure is the use of h-digraphs, not aspiration as such.
- **English-word share:** words of 4+ letters in the wordfreq English list (Zipf ≥ 3), as `scripts/english_share.py`.

**Decision rule** (per statistic: the ratio R = mean Gemini / mean human, with bootstrap CIs):
- **Matches:** the 90% CI of R lies within [0.80, 1.25].
- **Differs:** the 95% CI of R excludes 1 and the 90% CI is not within [0.80, 1.25]. The direction is reported.
- **Inconclusive:** otherwise.
- **K3b holds** ("Gemini spells like native speakers on these measures") if all three statistics match.
- **K3b refuted** if any statistic differs; the statistic and direction are named.
- Otherwise inconclusive.
- **English-share edge case:** if the human English-word share is below 0.5% of words, R is unstable. That statistic is
  then reported as the difference in percentage points with a 95% CI, without a verdict, and K3b is decided on the
  other two.

**Stated limitations, now.**
- Dakshina is Wikipedia text, a formal register. Its annotators romanized under their own task instructions (not
  published in full), not "as typed on a phone".
- Matching spelling statistics does not show that a romanization is natural; K3 (ratings) covers that.
- At temperature 0, the primary output is close to deterministic. The resample reference uses temperature 1.0 and so
  likely overstates Gemini's everyday variation.

**Cost and time.** About 500 primary requests, up to 1,000 with retries, plus 400 resample requests. That fits the free
tier's daily cap (1,000 per day in our client) over 1–2 days, at about 80 minutes of wall time per day at 12 requests
per minute. CPU analysis takes minutes. €0.

**Hindi.** Dakshina also has Hindi (`hi`, 10,000 strings, same procedure and splits), so a K3b-hi would be possible
for Phase D. It is not part of this draft.
