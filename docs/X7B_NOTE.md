# X7b: what it could and could not test (one-page note for Aarnav; X7b is NOT registered and nothing is committed for it)

**Status.** The X7 verdict ("does not survive", 2026-11-03) stands. The draft amendment for X7b (equal ACTUAL embedding parameters) was not approved as drafted and is not committed; it is kept out of the repository
(`build/X7B_DRAFT_not_approved.md`). This note states the problem with it. Decision on X7b: Aarnav's.

**The two designs side by side (factorized embedding, V x e table plus two projections of e x 384, plus e; d_model 384).**

| V | X7 (run) e | X7 actual embedding parameters | X7b (draft) e | X7b actual embedding parameters |
|---|---|---|---|---|
| 256 | 154 | 157,850 | 114 | 116,850 |
| 384 | 128 | 147,584 | 101 | 116,453 |
| 512 | 110 | 140,910 | 91 | 116,571 |
| 768 | 85 | 130,645 | 76 | 116,812 |
| 1024 | 70 | 125,510 | 65 | 116,545 |
| 4096 | 22 | 107,030 | 24 | 116,760 |

**Why X7b as drafted would not isolate fragmentation.** Equalizing the parameter count forces the embedding rank (the width e of the token table) to fall steeply with vocabulary: 114 at V = 256 against 24 at V = 4096 (X7: 154 against 22). A 4,096-token
vocabulary squeezed through 24 dimensions is a bottleneck that a 256-token (byte-level) vocabulary does not have, so the bits-per-byte rule would be decided mainly by that bottleneck, not by fragmentation: the sign of the 256 - 4096 gap is
already reversed in X7 (-0.051, p = 4e-5, every 256 seed better than every 4096 seed), where the rank was 154 against 22. X7b would raise the rank of 256 to 114 and of 4096 to 24; the same direction is the expected result, with a smaller margin, and
it could not be read as an answer to the fragmentation question either way.

**The first control has the opposite capacity bias.** In X7 the vocabulary with the most fragmentation (256) kept the most embedding parameters (157,850) and the one with the least (4096) the fewest (107,030): the control favoured the
fragmented end in parameters and disfavoured the other end in rank. X7b would remove the parameter difference but keep the rank difference. Neither design equalizes both quantities, and with a table of V x e entries both cannot be equal across vocabularies by construction
(equal parameters means unequal e; equal e means unequal parameters; Phase 1 itself had full-width e = 384 and parameters rising from 98,688 to 1,573,248).

**What X7b could test.** Whether the Phase 1 ordering (BPB falls as the vocabulary grows) depends on the embedding PARAMETER count alone: if, at equal parameters, bits per byte still fell with vocabulary size, parameter count would be ruled out as the explanation of the
Phase 1 ordering. The registered X7 rule already addresses a version of this and returned "does not survive".

**What X7b could not test.** (1) Fragmentation with embedding capacity held fixed: a worse 4096 at equal parameters would show the cost of a narrow embedding, not a cost of fewer tokens per word. (2) A clean separation of parameter capacity from rank. (3) Anything about
the assembly layer that is not also confounded by the same width difference (the probes read the residual stream, whose width is 384 in all runs, but the input representation passes through the e-wide bottleneck).

**Alternatives that exist (none is proposed for registration here).** A design with equal e across vocabularies (equal rank, unequal parameters, 4096 holding the most) would bias in the opposite direction to X7; X7, such a design and Phase 1 would bracket the question
rather than answer it. The X7-A measurement of the assembly layer on the 18 existing runs (separately drafted) costs about 0.5 GPU hours and needs no new training.
