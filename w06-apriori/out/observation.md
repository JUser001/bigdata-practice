# Week 6 observations

## Task 1 — A-Priori and rules

With 2,000 items, brute force has 1,999,000 possible pairs; at support 50, 1,849 items survive pass one (1,708,476 possible survivor pairs), and the baseline actually held 820,259 observed pair counters. On the benchmark, pair `{0, 1}` gives confidence 0.446 for `0 → 1` and 0.652 for `1 → 0`; the top rule is `1468 → 0` (confidence 0.839, lift 1.282), a real but moderate association.

## Task 2 — Lowering support

The active execution host did not run out through support 1: the peak was 312.0 MiB traced allocation and 7.09 s. From support 50 to 3, answers grew 39.1× while peak counters rose only 1.09× and then saturated; repeat Task 2 if the PC-bang computer is different.

## Task 3 — PCY

With 1,000,003 buckets, pass one uses a 4,000,012-byte integer array, then a 125,001-byte packed bitmap; peak pair counters fell from 820,259 to 23,356 (97.2%) with identical 6,397 answers. The memory sweep crossed between 4,000 baskets (Plain 2.98 MiB vs PCY 4.01 MiB) and 8,000 (Plain 12.56 MiB vs PCY 4.04 MiB); with only 10,003 buckets, collisions raised PCY to 820,259 counters, so the filter stopped helping.

## Task 4 — SON (optional)

Scaled local thresholds gave zero false negatives: 8 chunks produced 14,201 candidates and 4 chunks 9,876, while both returned the same 6,397 frequent pairs. If a pair were globally frequent but below the scaled threshold in every chunk, summing its chunk counts would put its global count below support, a contradiction; Spark could not run because PySpark is absent.
