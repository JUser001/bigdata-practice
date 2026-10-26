# Task 2 — support threshold and observed growth

Measurements use the official fixed-seed benchmark baskets (20,000 baskets, 2,000 items), running `PlainApriori` with Python 3.12.14. Peak memory is Python `tracemalloc` peak, not total process or system RAM.

| Support | Frequent pairs | Peak pair counters | Peak traced memory | Time |
|---:|---:|---:|---:|---:|
| 400 | 249 | 10,585 | 1.0 MiB | 0.77 s |
| 200 | 776 | 58,626 | 6.1 MiB | 1.51 s |
| 100 | 2,244 | 273,701 | 25.2 MiB | 2.81 s |
| 50 | 6,397 | 820,259 | 97.4 MiB | 4.51 s |
| 25 | 17,045 | 893,456 | 97.4 MiB | 5.08 s |
| 12 | 43,116 | 893,456 | 98.0 MiB | 5.28 s |
| 6 | 101,938 | 893,456 | 113.8 MiB | 5.45 s |
| 3 | 250,054 | 893,456 | 149.4 MiB | 5.59 s |
| 1 | 893,456 | 893,456 | 312.0 MiB | 7.09 s |

## A2 — where it became unpleasant

Nothing ran out through the minimum meaningful support of 1. At support 1 the run took 7.09 s and reached 312.0 MiB (327.1 MB) traced Python allocation; this host still had ample system memory. No crash or resource failure was observed, so the honest boundary for this machine is “not reached in the tested range.”

## A4 — counter growth

Halving support from 400→200→100→50 raised peak counters by 5.5×, 4.7×, then 3.0×. From 50→25 they rose only 1.1×, then plateaued at 893,456 because that is the number of distinct co-occurring pairs in these baskets. The growth is strongly nonlinear and eventually bounded by the observed pair universe.

## A5 — answers versus work

From support 50 to 3, frequent answers grew from 6,397 to 250,054 (39.1×), while peak pair counters grew only from 820,259 to 893,456 (1.09×); at support 1 every observed pair is an answer. At support 50 the method held about 128 counters per answer. Lowering the threshold can therefore make the result set much larger even after candidate counters have saturated.

## A6 — machine and conditions

- CPU: Intel(R) Core(TM) i5-14400F; RAM: 31.84 GiB installed (9.41 GiB available at inventory); Windows 10; Python 3.12.14.
- Codex desktop and the PowerShell/Python task were the foreground context. Windows background processes were active (238 processes at the later inventory snapshot).
- These values describe the active execution host. If the PC-bang computer is a different machine, re-run Task 2 there so the report matches the computer used.
