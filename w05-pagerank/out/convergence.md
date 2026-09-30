# Task 2 · Convergence measurements

**Machine (A7)** — Linux-6.18.44-fc-v50-x86_64-with-glibc2.39, x86_64, Python 3.12.3. Intel Xeon @ 2.1 GHz, **1 vCPU, 3.9 GiB RAM**, a cloud sandbox container. Nothing else was running except the shell that ran these scripts. Timings are single runs (no repeats), so treat anything under ~20 ms as noise; iteration counts do not depend on the machine.

Graph = the harness graph from `bench.build()` (power-law out-degrees, 12 dead ends, one 2-node trap). `tol` is the L1 change between successive rank vectors.

## A1 / A2 · Iterations against beta (1,200 nodes, tol 1e-10)

| beta | iterations | seconds | ln(tol)/ln(beta) — the textbook worst-case bound |
|---|---|---|---|
| 0.5 | 14 | 0.007 | 33 |
| 0.7 | 17 | 0.008 | 65 |
| 0.85 | 20 | 0.017 | 142 |
| 0.95 | 23 | 0.018 | 449 |
| 0.99 | 24 | 0.014 | 2291 |

## A3 · The shape as beta → 1

On the harness graph the count grows **slowly and smoothly** (14 → 24 as beta goes 0.5 → 0.99), far below the worst-case bound `ln(tol)/ln(beta)` (which reaches ~2,300 at beta = 0.99). Every run stopped honestly: the early-stopped ranks are within 3e-12 of a 3,000-iteration reference.

**Why.** Error shrinks by a factor `beta · |λ₂(M)|` per iteration, where λ₂ is the second-largest eigenvalue of the (dead-end-repaired) link matrix. `beta` is only the *upper* bound, reached when `|λ₂(M)| = 1`, i.e. when the graph has parts that mix slowly (near-disconnected communities, traps, periodic cycles). The harness graph is almost a DAG (Tarjan finds 1,190 strongly connected components for 1,200 nodes: a 10-node core and the 2-node trap), so there is little cycling for the surfer to get stuck in and `|λ₂(M)|` is small.

Checked with two extra graphs (1,200 nodes, tol 1e-10, not part of `convergence.json`):

| beta | random graph, uniform links (fast mixing) | two communities of 600 joined by 3 one-way edges (slow mixing) | bound ln(tol)/ln(beta) |
|---|---|---|---|
| 0.5 | 16 | 24 | 33 |
| 0.7 | 20 | 45 | 65 |
| 0.85 | 24 | 98 | 142 |
| 0.95 | 27 | 307 | 449 |
| 0.99 | 29 | 1463 | 2291 |

The slow-mixing graph reproduces the textbook picture: iterations explode as beta → 1 (24 → 1,463, about 60×), still under the bound. Physically, `1/(1 - beta)` is the surfer's average run length between teleports; the closer beta is to 1, the longer the chain has to run before it forgets where it started, and the more the graph's own structure (the soft trap) decides how long that takes.

## A4 · Graph size (tol 1e-10)

| beta | iterations, 1,200 nodes | iterations, 20,000 nodes | seconds, 1,200 | seconds, 20,000 | time ratio |
|---|---|---|---|---|---|
| 0.5 | 14 | 14 | 0.007 | 0.196 | 27× |
| 0.7 | 17 | 18 | 0.008 | 0.236 | 29× |
| 0.85 | 20 | 21 | 0.017 | 0.263 | 16× |
| 0.95 | 23 | 24 | 0.018 | 0.320 | 18× |
| 0.99 | 24 | 25 | 0.014 | 0.311 | 23× |

Sizes are 16.7× apart. **Iteration count barely moved** (+0 to +1) while **wall time grew 15–29×** (the 1,200-node runs take only 7–18 ms, so those ratios are noisy), i.e. on the order of the 16.7× size ratio: about linear in the number of nodes/edges. They answer different questions: the count is how many times you must apply the operator (set by beta and the mixing of the graph, not by how many pages there are); the time is the cost of *one* application, which touches every edge once, so it scales with the edge count.

## A5 · Tolerance (1,200 nodes)

| beta | tol 1e-4 | tol 1e-6 | tol 1e-10 | extra iterations per extra digit, 1e-4 → 1e-10 |
|---|---|---|---|---|
| 0.5 | 6 | 9 | 14 | 1.3 |
| 0.7 | 8 | 10 | 17 | 1.5 |
| 0.85 | 9 | 12 | 20 | 1.8 |
| 0.95 | 9 | 13 | 23 | 2.3 |
| 0.99 | 10 | 13 | 24 | 2.3 |

Each extra digit of accuracy costs a *constant* number of iterations (the error shrinks geometrically), so the iteration count is linear in `log(1/tol)`: about 2 iterations per digit at beta = 0.85 and 2.3 at 0.99 here, versus the worst-case `1/(-log10 beta)` ≈ 14 per digit at 0.85 and ≈ 229 at 0.99. Going from 1e-4 to 1e-10 (six digits) cost 11 extra iterations at beta = 0.85 on this graph; 6 digits are cheap when the graph mixes fast, expensive when it does not.

## A6 · Does the top 10 change with beta?

Top 10 at beta = 0.85: `p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008`.

- On the 1,200-node graph the **set** of ten pages is identical for every beta tried (0.05 … 0.99): always the ten seed pages `p00000`–`p00009`.
- The **order** is identical to the 0.85 order for every beta from 0.55 to 0.99 (0.01 grid from 0.50 to 0.60, then 0.6, 0.7, 0.8, 0.9, 0.95, 0.97, 0.99).
- Coming down from 0.99 the order **first changes at beta = 0.54**: `p00004` and `p00000` swap places (ranks 7 and 8). It also differs from the 0.85 order at every beta tried from 0.05 to 0.5.
- On the 20,000-node graph, only the five recorded betas were compared: 0.7, 0.85, 0.95, 0.99 give the same top 10 in the same order; 0.5 does not.

Fragility: at 0.85 the two closest neighbours in the list are `p00007`/`p00008`, only 1.8e-3 apart in rank, so a top-10 *order* is a statement about that beta, not about the graph.

**What it means:** on this graph the choice of 0.85 does not decide *which* pages are important, and it barely decides their order in the range people actually use (0.55–0.99), so beta is a tuning detail here. That is a property of this graph and not a promise; a published ranking should state beta, tolerance and how dead ends were handled, and one should not read fine differences between adjacent ranks as meaningful.

## Reproduce

```bash
rm -f out/convergence.json
python3 task2_convergence.py --betas 0.5,0.7,0.85,0.95,0.99
python3 task2_convergence.py --tol 1e-6 --betas 0.5,0.7,0.85,0.95,0.99
python3 task2_convergence.py --tol 1e-4 --betas 0.5,0.7,0.85,0.95,0.99
python3 task2_convergence.py --nodes 20000 --betas 0.5,0.7,0.85,0.95,0.99
python3 task2_convergence.py --nodes 20000 --tol 1e-6 --betas 0.5,0.85,0.99
```
Note: `task2_convergence.py` was changed to add `--max-iter` (default 5000) and a `converged` field; the original cap of 500 iterations would have stopped the beta = 0.99 run early on slower-mixing graphs.
