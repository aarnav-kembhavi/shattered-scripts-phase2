# T3 instruction check (one page, for a native Kannada speaker)

**What this is.** In experiment X1 (T3) the question line of each task prompt is written in Kannada. The label words
(negative, positive, no, maybe, yes, geography, ...) stay in English on purpose, and so do the field names
(Review, Premise, Hypothesis, Text, Answer). The Kannada was drafted by a machine (gemini-3.5-flash-lite) and has
not been checked by a person. **Nothing is scored on T3 until this sheet is returned.**

**What we ask.** For each of the three lines: is it correct, natural Kannada that a reader would understand as the
English meaning given? Mark OK, or write the corrected line. Please change as little as possible and keep the
English label words as they are.

---

## 1. Sentiment (review is negative or positive)

Full prompt (the review text goes after `Review:`):

```
Review: {review text}
Question: ಈ ವಿಮರ್ಶೆಯು negative ಅಥವಾ positive ಎಂದು ನೀವು ಹೇಳುತ್ತೀರಾ?
Answer:
```

English source: *Would you say this review is negative or positive?*
Literal gloss of the Kannada: *Would you say that this review is negative or positive?*

- [ ] OK  - [ ] Needs a change. Corrected line: ______________________________________________

## 2. XNLI (premise and hypothesis; answer no, maybe or yes)

```
Premise: {premise}
Hypothesis: {hypothesis}
Question: ದತ್ತಾಂಶವು ಸತ್ಯವಾಗಿದ್ದರೆ, ಪರಿಕಲ್ಪನೆಯು ಸತ್ಯವೇ? no, maybe, ಅಥವಾ yes ಆಯ್ಕೆಮಾಡಿ.
Answer:
```

English source: *If the premise is true, is the hypothesis true? Choose no, maybe, or yes.*
Literal gloss of the Kannada: *If the "data" is true, is the "concept" true? Choose no, maybe, or yes.*

**This line is the likely problem.** The draft renders "premise" as ದತ್ತಾಂಶ (data, dataset) and "hypothesis" as
ಪರಿಕಲ್ಪನೆ (concept, notion). These are not the usual words for the logic terms, and the line does not point at the
`Premise:` and `Hypothesis:` lines above it. Please give the wording you would use (or say the field names should
simply stay in English inside the sentence).

- [ ] OK  - [ ] Needs a change. Corrected line: ______________________________________________

## 3. SIB-200 (topic of the text)

```
Text: {text}
Question: ಈ ಪಠ್ಯದ ಮುಖ್ಯ ವಿಷಯವೇನು: geography, entertainment, health, sports, politics, travel ಅಥವಾ science?
Answer:
```

English source: *What is the main topic of this text: geography, entertainment, health, sports, politics, travel or science?*
Literal gloss of the Kannada: *What is the main topic of this text: geography, entertainment, health, sports, politics, travel or science?*

- [ ] OK  - [ ] Needs a change. Corrected line: ______________________________________________

---

Glosses were written by Claude from the Kannada and are only meant to help you see the intended meaning; they are not a
check. Returned by: ______________   Date: ____________   Overall: [ ] all three OK  [ ] changes above

*Files (frozen 2026-11-02, before any T3 scoring): `src/shattered/llm/templates/e0_{sentiment,xnli,sib}_v3.txt`,
sha256 prefixes d033e17f70369f67, 71fd1dbbc2d6395c, d0ac3dcb7c832384; record in `results/phase2/x1/t3_templates.json`.
If a line is changed, the changed file becomes the T3 template and the change is logged as a dated deviation.*
