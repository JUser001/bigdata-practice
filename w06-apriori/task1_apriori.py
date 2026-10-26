#!/usr/bin/env python3
"""Week 6 Task 1: A-Priori frequent pairs and association rules."""
import argparse
from itertools import combinations

BASKETS = [
    {"bread", "milk"},
    {"bread", "diaper", "beer", "egg"},
    {"milk", "diaper", "beer", "cola"},
    {"bread", "milk", "diaper", "beer"},
    {"bread", "milk", "diaper", "cola"},
    {"bread", "milk", "beer"},
    {"diaper", "beer"},
]


def frequent_singletons(baskets, support):
    """Return {item: count} for items appearing in at least support baskets."""
    counts = {}
    for basket in baskets:
        for item in basket:
            counts[item] = counts.get(item, 0) + 1
    return {item: count for item, count in counts.items() if count >= support}


def frequent_pairs(baskets, support):
    """Count frequent pairs, generating candidates only from frequent items."""
    frequent_items = set(frequent_singletons(baskets, support))
    counts = {}
    for basket in baskets:
        survivors = sorted(basket & frequent_items)
        for a, b in combinations(survivors, 2):
            pair = frozenset((a, b))
            counts[pair] = counts.get(pair, 0) + 1
    return {pair: count for pair, count in counts.items() if count >= support}


def association_rules(baskets, support, min_confidence):
    """Return directional rules (antecedent, consequent, confidence, lift)."""
    n_baskets = len(baskets)
    if n_baskets == 0:
        return []
    singleton_counts = frequent_singletons(baskets, support)
    pair_counts = frequent_pairs(baskets, support)
    rules = []
    for pair, pair_count in pair_counts.items():
        a, b = sorted(pair)
        for antecedent, consequent in ((a, b), (b, a)):
            confidence = pair_count / singleton_counts[antecedent]
            if confidence >= min_confidence:
                consequent_support = singleton_counts[consequent] / n_baskets
                lift = confidence / consequent_support
                rules.append((antecedent, consequent, confidence, lift))
    return sorted(rules, key=lambda rule: rule[2], reverse=True)


def verify():
    fails = 0

    def check(label, got, want):
        nonlocal fails
        ok = got == want
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<44} {got}"
              + ("" if ok else f"\n{'':>54}want {want}"))
        fails += not ok

    singles = frequent_singletons(BASKETS, 3)
    check("frequent singletons at support 3",
          dict(sorted(singles.items())),
          {"beer": 5, "bread": 5, "diaper": 5, "milk": 5})

    pairs = frequent_pairs(BASKETS, 3)
    got = {tuple(sorted(pair)): count for pair, count in pairs.items()}
    check("frequent pairs at support 3", dict(sorted(got.items())),
          {("beer", "bread"): 3, ("beer", "diaper"): 4,
           ("beer", "milk"): 3, ("bread", "diaper"): 3,
           ("bread", "milk"): 4, ("diaper", "milk"): 3})
    check("infrequent items excluded from pairs",
          any("cola" in pair or "egg" in pair for pair in got), False)

    rules = association_rules(BASKETS, 3, 0.75)
    hit = [rule for rule in rules if rule[0] == "diaper" and rule[1] == "beer"]
    check("diaper -> beer confidence",
          round(hit[0][2], 3) if hit else None, 0.8)
    check("rules are sorted by confidence",
          all(rules[i][2] >= rules[i + 1][2]
              for i in range(len(rules) - 1)), True)

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    raise SystemExit(verify() if args.verify else parser.print_help())
