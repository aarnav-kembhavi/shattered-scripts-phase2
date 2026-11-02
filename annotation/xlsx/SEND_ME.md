# Messages to paste (WhatsApp, English). Updated 2026-11-03 01:37 IST: X15 is skipped and removed; X8 (P and Q) and T3 remain.

Attach the one file named in each message. Do not send two roles' files to the same person. Time estimates are my estimates from the text lengths (X8: 100 sentences,
1,602 Kannada words, 16 words per sentence on average); no one has done a task yet, so the first returned file tells you the real time.

---

## X8 annotator P  (attach `X8_P.xlsx`)

Hi, thank you for helping with my research. Attached is an Excel file with 100 Kannada sentences. For each sentence, please type it in English letters (romanized Kannada),
exactly the way you would type it in a WhatsApp message to a friend, in the yellow column. Please do NOT look anything up and do not use any translator, typing tool or AI.
Please do not change columns A and B. Before you start, turn off Excel AutoCorrect (the first sheet explains how; otherwise it capitalises and changes your words). It takes about 1.5 hours (1 to 2); you can do it
in several sittings. When done, save and send the same file back to me here. Please do not discuss it with anyone else who is doing it. Thank you!

## X8 annotator Q  (attach `X8_Q.xlsx`)

Same message as P with `X8_Q.xlsx`. **X8_Q goes to a different group of speakers, none of whom are in P's group, and nobody in Q's group sees X8_P.** P and Q must not see each other's file.

---

## T3 verifier  (attach `T3_verification.xlsx`; one native Kannada speaker who reads and writes Kannada)

Hi, thank you for helping with my research. Attached is a short Excel sheet with three Kannada question lines that a machine wrote. For each row, please say in the Verdict column
whether the Kannada line is correct, natural Kannada for the English meaning shown (Correct or Needs change), and if it needs a change, type the corrected Kannada line in the last
column (change as little as possible; the English words in the line stay in English). The second row is already marked as probably wrong; please give the wording you would use.
It takes about 10 to 15 minutes. Please send the file back to me here when done. Thank you!

---

## Time estimates (task, items, estimate, how it was derived)

| Task | Items | Estimate per annotator | Basis |
|---|---|---|---|
| X8 (P, Q) | 100 sentences, 1,602 words | about 1.5 hours (1 to 2 hours) | reading plus typing about 16 words per sentence at roughly 20 words per minute including thinking |
| T3 (1 person) | 3 lines | 10 to 15 minutes | reading three lines and typing at most one or two corrections |

The X8 workbooks are not protected: the importers compare every cell outside the answer column with the original, so any edit to another cell is reported and blocks the import.

Returned files go to `scripts/import_x8.py` (P and Q), which check missing or blank cells, labels not in the list, edited locked cells
and duplicate ids before writing the registered formats. For X8 they also print the share of cells starting with an uppercase letter and the share with characters outside the expected
romanization set (smart quotes, ellipsis and so on), which would show that AutoCorrect was left on. There is no importer for T3; read the Verdict and Corrected columns by eye.

Note: the one-line Kannada sentence on the first sheet of the X8 files was written by me (a machine) and has not been checked by a native speaker; the English instructions say the same thing.
