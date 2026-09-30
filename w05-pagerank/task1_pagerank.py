#!/usr/bin/env python3
"""Week 5 · Task 1 — PageRank, and the two ways it breaks.

Textbook §5.1 (PageRank), §5.1.3 (dead ends), §5.1.4 (spider traps).

PageRank is a random surfer following links forever, and the rank of a page is
how often the surfer is there. As one line of linear algebra it is
`r = M r`, and as written it does not work on the actual web.

Two structures break it, and the fix for both is the same one line. Build the
broken version first so you can see each failure, then fix it.

    python3 task1_pagerank.py --verify
"""
import argparse

# A: -> B, C      B: -> C      C: -> A
SIMPLE = {"A": ["B", "C"], "B": ["C"], "C": ["A"]}

# C has no out-links at all. Rank leaks out of the graph and everything -> 0.
DEAD_END = {"A": ["B", "C"], "B": ["C"], "C": []}

# C and D only point at each other. They absorb everything.
SPIDER_TRAP = {"A": ["B"], "B": ["C"], "C": ["D"], "D": ["C"]}


def pagerank(graph, beta=0.85, iterations=100, tol=1e-10):
    """Rank every node. Return {node: rank}, summing to 1.

    `beta` is the probability the surfer follows a link. With probability
    1 - beta they teleport to a node chosen uniformly.

    You have to handle both of these, and the textbook handles them the same way:

      dead ends    a node with no out-links. Where does its rank go, and where
                   should it go instead?
      spider traps a group of nodes that only link to each other. Without
                   teleporting, they end up with all of it

    Stop early when the ranks stop moving - `tol` is the L1 change below which
    you should call it converged. Return the ranks, and set `pagerank.iterations`
    to how many you actually used, because Task 2 measures that.
    """
    # Every node counts, including ones that only ever appear as a link target.
    nodes = list(graph)
    seen = set(nodes)
    for outs in graph.values():
        for w in outs:
            if w not in seen:
                seen.add(w)
                nodes.append(w)
    n = len(nodes)
    outs_of = {v: graph.get(v, []) for v in nodes}
    dead_ends = [v for v in nodes if not outs_of[v]]

    r = {v: 1.0 / n for v in nodes}
    pagerank.iterations = 0
    for it in range(1, iterations + 1):
        # A dead end has nowhere to send its rank. Choice made here: it teleports
        # to a uniformly random page (same as the surfer being "stuck" and jumping).
        leaked = sum(r[v] for v in dead_ends)
        # teleport (1 - beta) plus the dead-end share: the same amount for every node
        base = ((1 - beta) + beta * leaked) / n

        nr = {v: base for v in nodes}
        for v in nodes:
            outs = outs_of[v]
            if outs:
                share = beta * r[v] / len(outs)
                for w in outs:
                    nr[w] += share

        delta = sum(abs(nr[v] - r[v]) for v in nodes)
        r = nr
        pagerank.iterations = it
        if delta < tol:
            break
    return r


def pagerank_no_teleport(graph, iterations=100):
    """The broken version: beta = 1, no teleporting. Build this too.

    It exists so you can watch both failures happen rather than take them on
    trust. The harness checks that it really does fail.
    """
    nodes = list(graph)
    seen = set(nodes)
    for outs in graph.values():
        for w in outs:
            if w not in seen:
                seen.add(w)
                nodes.append(w)
    n = len(nodes)

    r = {v: 1.0 / n for v in nodes}
    for _ in range(iterations):
        nr = {v: 0.0 for v in nodes}        # no teleport term
        for v in nodes:
            outs = graph.get(v, [])
            if outs:                        # a dead end sends its rank nowhere: it just vanishes
                share = r[v] / len(outs)
                for w in outs:
                    nr[w] += share
        r = nr
    return r


# ------------------------------------------------------------------- harness
def verify():
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<48} {detail}")
        fails += not ok

    try:
        r = pagerank(SIMPLE)
    except NotImplementedError:
        print("  pagerank is still a stub"); return 1

    check("ranks sum to 1", abs(sum(r.values()) - 1) < 1e-6, f"{sum(r.values()):.6f}")
    check("every node ranked", set(r) == set(SIMPLE), sorted(r))
    # C is pointed at by both A and B, so it has to come first.
    check("C outranks A and B", r["C"] > r["A"] and r["C"] > r["B"],
          {k: round(v, 4) for k, v in sorted(r.items())})

    try:
        broken = pagerank_no_teleport(DEAD_END)
    except NotImplementedError:
        print("  pagerank_no_teleport is still a stub"); return 1
    check("without the fix, a dead end drains the graph",
          sum(broken.values()) < 0.5, f"total rank {sum(broken.values()):.4f}")

    fixed = pagerank(DEAD_END)
    check("with the fix, rank is conserved",
          abs(sum(fixed.values()) - 1) < 1e-6, f"{sum(fixed.values()):.6f}")

    trapped = pagerank_no_teleport(SPIDER_TRAP)
    check("without the fix, a spider trap takes everything",
          trapped["C"] + trapped["D"] > 0.95,
          f"C+D = {trapped['C'] + trapped['D']:.4f}")

    untrapped = pagerank(SPIDER_TRAP)
    check("with the fix, A and B keep some rank",
          untrapped["A"] > 0.01 and untrapped["B"] > 0.01,
          {k: round(v, 4) for k, v in sorted(untrapped.items())})

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())
