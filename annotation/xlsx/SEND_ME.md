# Messages to paste (WhatsApp, English). Nothing has been sent.

Attach the one file named in each message. Do not send two roles' files to the same person. Time estimates are my estimates from the text lengths (X8: 100 sentences,
1,602 Kannada words, 16 words per sentence on average; X15: 100 texts of about 16 words each); no one has done a task yet, so the first returned file tells you the real time.

---

## X8 annotator P  (attach `X8_P.xlsx`)

Hi, thank you for helping with my research. Attached is an Excel file with 100 Kannada sentences. For each sentence, please type it in English letters (romanized Kannada),
exactly the way you would type it in a WhatsApp message to a friend, in the yellow column. Please do NOT look anything up and do not use any translator, typing tool or AI.
Before you start, turn off Excel AutoCorrect (the first sheet explains how; otherwise it capitalises and changes your words). It takes about 1.5 hours (1 to 2); you can do it
in several sittings. When done, save and send the same file back to me here. Please do not discuss it with anyone else who is doing it. Thank you!

## X8 annotator Q  (attach `X8_Q.xlsx`)

Same message as P with `X8_Q.xlsx`. Must be a different person from P, and P and Q must not see each other's file.

---

## X15 annotators (eight people, one file each: `X15_G1_a`, `X15_G1_b`, `X15_G2_a`, `X15_G2_b`, `X15_G3_a`, `X15_G3_b`, `X15_G4_a`, `X15_G4_b`)

Hi, thank you for helping with my research. Attached is an Excel file with 100 short Kannada sentences (some in Kannada script, some in English letters). For each one, please
pick the topic that fits best from the dropdown list in the yellow column (science/technology, travel, politics, sports, health, entertainment, geography). Answer every row,
even if you are not sure. Please do NOT look anything up, no translator or AI, and do not discuss the sentences with anyone. It takes about 30 to 45 minutes. When done, save and
send the same file back to me here. Thank you!

(Send each person a different file; the two people of a group, for example G1_a and G1_b, may know each other but must not compare answers. All eight must be native Kannada speakers
who have not seen the items.)

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
| X15 (8 people) | 100 texts, about 16 words each | 30 to 45 minutes | about 15 to 25 seconds per text; Kannada-script texts faster, the English-letter forms slower |
| T3 (1 person) | 3 lines | 10 to 15 minutes | reading three lines and typing at most one or two corrections |

Returned files go to `scripts/import_x8.py` (P and Q) and `scripts/import_x15.py` (the eight), which check missing or blank cells, labels not in the list, edited locked cells
and duplicate ids before writing the registered formats. For X8 they also print the share of cells starting with an uppercase letter and the share with characters outside the expected
romanization set (smart quotes, ellipsis and so on), which would show that AutoCorrect was left on. There is no importer for T3; read the Verdict and Corrected columns by eye.

Note: the one-line Kannada sentence on the first sheet of the X8 files was written by me (a machine) and has not been checked by a native speaker; the English instructions say the same thing.
