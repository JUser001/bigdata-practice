# Task 2 · Distance contrast measurements

Each dimension used 20,000 attempted pairs. The first seven rows use 1,000
points; the 500- and 1,000-dimensional runs use 2,000 points. Equal-index pairs
are discarded by the supplied sampler, so the accepted pair count is just under
20,000 in some runs. Full measurements and timings are in `curse.json`.

| Dimensions | Points | Mean distance | Contrast | Relative SD |
|---:|---:|---:|---:|---:|
| 2 | 1,000 | 0.521 | 488.582 | 0.476 |
| 5 | 1,000 | 0.884 | 14.257 | 0.282 |
| 10 | 1,000 | 1.274 | 3.925 | 0.193 |
| 20 | 1,000 | 1.815 | 2.253 | 0.135 |
| 50 | 1,000 | 2.867 | 0.982 | 0.083 |
| 100 | 1,000 | 4.068 | 0.545 | 0.060 |
| 200 | 1,000 | 5.776 | 0.372 | 0.041 |
| 500 | 2,000 | 9.126 | 0.256 | 0.026 |
| 1,000 | 2,000 | 12.909 | 0.153 | 0.019 |

## A3–A8

- **A3 — Contrast:** It first falls below 1 at 50 dimensions, and below 0.5 at
  200 dimensions for this sample size. The drop is steep at low dimensions and
  continues more gradually afterward.
- **A4 — Mean distance:** The mean grows approximately with `sqrt(d)`, not
  linearly. For example, the 20-dimensional mean is 1.815 and the 1,000-
  dimensional mean is 12.909; both are close to `0.408 × sqrt(d)`.
- **A5 — Relative spread:** Relative standard deviation falls from 0.476 at 2
  dimensions to 0.019 at 1,000. It describes the typical spread around the mean;
  contrast describes the sampled extremes. Relative SD is the steadier measure
  of whether typical distances are becoming alike, while contrast also changes
  with the number of points and sampled pairs.
- **A6 — Point count (fixed at 20 dimensions):** Contrast was 1.787 for 200
  points, 2.253 for 1,000, and 2.448 for 2,000. The mean stayed near 1.817 and
  relative SD near 0.13. With more points, the sample is more likely to include
  unusually close or distant pairs, so contrast depends on `n` as well as `d`.
- **A7 — Machine and runtime:** Windows 11, Intel64 Family 6 Model 170, Python
  3.12.14. The largest run (2,000 points, 1,000 dimensions, 19,997 accepted
  pairs) took 2.55 seconds.
- **A8 — Week 3 LSH:** This experiment does not directly show that Jaccard LSH
  fails. It measures Euclidean distances between uniform cube points, while
  shingle sets use Jaccard similarity and have their own distribution. It is a
  useful warning to measure similarity contrast on the actual sets; it is not a
  proof that Jaccard nearest neighbors lose meaning.
