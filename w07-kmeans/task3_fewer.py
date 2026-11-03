#!/usr/bin/env python3
"""Week 7 · Task 3 — The same clustering, with far fewer distances.

Textbook §7.3, and §7.1.3 for why distance is the expensive part.

`NaiveKMeans` does what the definition says: every iteration, compare every
point with every centroid. That is n x k distance computations per pass, and on
a real dataset the distance computation is almost the entire cost.

Most of that work is wasted. After the first couple of iterations, most points
do not change cluster, and most centroids barely move. The triangle inequality
lets you prove a point cannot have changed cluster **without measuring it**.

    python3 bench.py
    python3 bench.py --yours

Correctness first: your final SSE must match the baseline's. Fewer distances
with a worse clustering is not an improvement, it is a different algorithm.
"""


class NaiveKMeans:
    """Every point against every centroid, every iteration."""

    def __init__(self, k, max_iter=50):
        self.k, self.max_iter = k, max_iter

    def run(self, points, initial_centroids, distance):
        centroids = list(initial_centroids)
        labels = [None] * len(points)
        for self.iterations in range(1, self.max_iter + 1):
            changed = False
            for i, p in enumerate(points):
                best, bi = None, 0
                for j, c in enumerate(centroids):
                    d = distance(p, c)
                    if best is None or d < best - 1e-12:
                        best, bi = d, j
                if labels[i] != bi:
                    labels[i] = bi
                    changed = True
            centroids = _means(points, labels, self.k, centroids)
            if not changed:
                break
        return labels, centroids


def _means(points, labels, k, previous):
    out = []
    for j in range(k):
        group = [p for p, l in zip(points, labels) if l == j]
        if group:
            out.append(tuple(sum(v) / len(group) for v in zip(*group)))
        else:
            out.append(previous[j])
    return out


class YourKMeans:
    """Your k-means.

        __init__(k, max_iter=50)
        run(points, initial_centroids, distance) -> (labels, centroids)

    Same starting centroids, same `distance` function - which is counted. That
    counter is your score.

    The idea, from §7.3 and the triangle inequality:

        if a point is much closer to its current centroid than that centroid
        moved, and than any other centroid could have come, then it cannot have
        changed cluster, and you do not have to measure anything

    Keeping enough bookkeeping to make that test cheap, without keeping so much
    that the bookkeeping costs more than the distances, is the task.

    You may call `distance` on two centroids, and those calls are counted too -
    which is the correct accounting, since that is real work. There are k of
    them and n points, and k is much smaller than n. That asymmetry is the
    whole opening.
    """

    def __init__(self, k, max_iter=50):
        if k <= 0:
            raise ValueError("k must be positive")
        self.k, self.max_iter = k, max_iter
        self.iterations = 0
        self.pruned_by_lower = 0
        self.pruned_by_separation = 0
        self.pruned_by_both = 0

    def run(self, points, initial_centroids, distance):
        n = len(points)
        centroids = list(initial_centroids)
        if len(centroids) != self.k:
            raise ValueError("initial_centroids must contain exactly k centers")
        if not points:
            self.iterations = 0
            return [], centroids

        # Hamerly bounds: upper[i] bounds the distance to point i's assigned
        # center; lower[i] bounds its distance to every other center.
        labels = [None] * n
        upper = [float("inf")] * n
        lower = [0.0] * n
        self.pruned_by_lower = self.pruned_by_separation = self.pruned_by_both = 0

        for iteration in range(1, self.max_iter + 1):
            # Half the nearest-center separation is a second safe pruning test.
            separation = [float("inf")] * self.k
            for a in range(self.k):
                for b in range(a + 1, self.k):
                    half = distance(centroids[a], centroids[b]) / 2.0
                    if half < separation[a]:
                        separation[a] = half
                    if half < separation[b]:
                        separation[b] = half

            changed = False
            for i, point in enumerate(points):
                old_label = labels[i]
                if old_label is not None:
                    passes_lower = upper[i] < lower[i]
                    passes_separation = upper[i] < separation[old_label]
                    if passes_lower or passes_separation:
                        if passes_lower and passes_separation:
                            self.pruned_by_both += 1
                        elif passes_lower:
                            self.pruned_by_lower += 1
                        else:
                            self.pruned_by_separation += 1
                        continue

                # A point that fails either bound is checked exactly. Keeping
                # centers in index order makes distance ties go to the lower id.
                distances = [distance(point, center) for center in centroids]
                best_label = min(range(self.k), key=distances.__getitem__)
                best_distance = distances[best_label]
                second_distance = min(
                    (distances[j] for j in range(self.k) if j != best_label),
                    default=float("inf"))
                if old_label != best_label:
                    labels[i] = best_label
                    changed = True
                upper[i] = best_distance
                lower[i] = second_distance

            new_centroids = _means(points, labels, self.k, centroids)
            self.iterations = iteration
            if not changed:
                return labels, new_centroids

            # Moving centers changes both bounds. The largest movement among
            # competing centers gives a valid update to each lower bound.
            shifts = [distance(old, new)
                      for old, new in zip(centroids, new_centroids)]
            max_other_shift = [
                max((shifts[j] for j in range(self.k) if j != own), default=0.0)
                for own in range(self.k)
            ]
            for i, label in enumerate(labels):
                upper[i] += shifts[label]
                lower[i] = max(0.0, lower[i] - max_other_shift[label])
            centroids = new_centroids

        return labels, centroids
