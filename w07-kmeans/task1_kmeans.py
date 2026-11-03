#!/usr/bin/env python3
"""Week 7 · Task 1 — k-means, and the thing that decides the answer.

Textbook §7.1 (clustering, the curse of dimensionality), §7.3 (k-means).

k-means is four lines: pick centroids, assign every point to the nearest one,
move each centroid to the mean of its points, repeat. It always converges.

It converges to a **local** optimum, and which one depends entirely on where you
started. That is not a footnote - it is the difference between a clustering that
means something and one that does not, and you can watch it happen on nine points.

    python3 task1_kmeans.py --verify
"""
import argparse, math, random

# Three obvious blobs of three points each. Any sensible clustering finds them.
BLOBS = [(0.0, 0.0), (0.2, 0.1), (0.1, 0.2),
         (8.0, 8.0), (8.2, 8.1), (8.1, 8.2),
         (0.0, 8.0), (0.2, 8.1), (0.1, 8.2)]


def euclidean(a, b):
    """Distance between two points of any dimension."""
    if len(a) != len(b):
        raise ValueError("points must have the same number of dimensions")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def assign(points, centroids):
    """Nearest centroid for each point. Return a list of centroid indices.

    Ties go to the lower index, so that everybody's answer is the same.
    """
    if not centroids:
        raise ValueError("at least one centroid is required")
    labels = []
    for point in points:
        best_index = 0
        best_distance = euclidean(point, centroids[0])
        for index in range(1, len(centroids)):
            distance = euclidean(point, centroids[index])
            if distance < best_distance:
                best_index, best_distance = index, distance
        labels.append(best_index)
    return labels


def update(points, labels, k, previous=None):
    """Move each centroid to the mean of its points.

    An empty cluster has no mean. Keep its previous centroid when supplied;
    without previous centroids, use the first point as a deterministic fallback.
    """
    if k <= 0:
        raise ValueError("k must be positive")
    dimensions = len(points[0]) if points else 0
    sums = [[0.0] * dimensions for _ in range(k)]
    counts = [0] * k
    for point, label in zip(points, labels):
        counts[label] += 1
        for dimension, value in enumerate(point):
            sums[label][dimension] += value
    # Empty clusters retain their previous centroid. If this helper is called
    # without previous centroids, use a valid deterministic fallback point.
    return [tuple(value / counts[index] for value in sums[index])
            if counts[index] else (previous[index] if previous is not None else tuple(points[0]))
            for index in range(k)]


def kmeans(points, k, init="random", seed=246, max_iter=100):
    """Run to convergence. Return (labels, centroids, sse).

    `sse` is the sum over points of the squared distance to their own centroid.
    It is what k-means minimises, and it is how you compare two runs.

    `init` is either:
        "random"   pick k points at random as the starting centroids
        "++"       k-means++ (§7.3.2): pick the first at random, then pick each
                   next one with probability proportional to the squared distance
                   to the nearest centroid already chosen

    Set `kmeans.iterations` to how many passes you used.
    """
    if not points:
        raise ValueError("points must not be empty")
    if not 1 <= k <= len(points):
        raise ValueError("k must be between 1 and the number of points")
    if max_iter < 1:
        raise ValueError("max_iter must be at least 1")
    if init not in ("random", "++"):
        raise ValueError("init must be 'random' or '++'")

    rng = random.Random(seed)
    if init == "random":
        centroids = [points[index] for index in rng.sample(range(len(points)), k)]
    else:
        chosen = [rng.randrange(len(points))]
        while len(chosen) < k:
            centers = [points[index] for index in chosen]
            weights = []
            for point in points:
                nearest_sq = min(sum((x - y) ** 2 for x, y in zip(point, center))
                                 for center in centers)
                weights.append(nearest_sq)
            total = sum(weights)
            if total == 0:
                # All remaining points coincide with an existing center.
                remaining = [index for index in range(len(points)) if index not in chosen]
                chosen.append(rng.choice(remaining))
            else:
                threshold = rng.random() * total
                cumulative = 0.0
                selected = None
                for index, weight in enumerate(weights):
                    cumulative += weight
                    if cumulative > threshold:
                        selected = index
                        break
                if selected is None:
                    selected = max(range(len(weights)), key=weights.__getitem__)
                chosen.append(selected)
        centroids = [points[index] for index in chosen]

    labels = None
    kmeans.iterations = 0
    for iteration in range(1, max_iter + 1):
        new_labels = assign(points, centroids)
        new_centroids = update(points, new_labels, k, previous=centroids)
        kmeans.iterations = iteration
        unchanged = new_labels == labels
        labels, centroids = new_labels, new_centroids
        if unchanged:
            break
    return labels, centroids, sse_of(points, labels, centroids)


def sse_of(points, labels, centroids):
    """Sum of squared distances from each point to its assigned centroid."""
    return sum(sum((x - y) ** 2 for x, y in zip(point, centroids[label]))
               for point, label in zip(points, labels))


# ------------------------------------------------------------------- harness
def verify():
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<50} {detail}")
        fails += not ok

    try:
        check("distance in 2d", abs(euclidean((0, 0), (3, 4)) - 5) < 1e-9)
        check("distance in 5d",
              abs(euclidean((0,) * 5, (1,) * 5) - math.sqrt(5)) < 1e-9)
    except NotImplementedError:
        print("  euclidean is still a stub"); return 1

    try:
        labels, cents, sse = kmeans(BLOBS, 3, init="++", seed=1)
    except NotImplementedError:
        print("  kmeans is still a stub"); return 1

    groups = {}
    for p, l in zip(BLOBS, labels):
        groups.setdefault(l, []).append(p)
    check("three clusters of three", sorted(len(g) for g in groups.values()) == [3, 3, 3],
          sorted(len(g) for g in groups.values()))
    check("the three blobs were recovered",
          all(max(q[0] for q in g) - min(q[0] for q in g) < 1 and
              max(q[1] for q in g) - min(q[1] for q in g) < 1
              for g in groups.values()))
    check("sse is small when clusters are right", sse < 1.0, f"sse {sse:.4f}")

    # Bad luck with random starts should sometimes be visibly worse.
    randoms = [kmeans(BLOBS, 3, init="random", seed=s)[2] for s in range(40)]
    plusplus = [kmeans(BLOBS, 3, init="++", seed=s)[2] for s in range(40)]
    check("random init sometimes lands badly", max(randoms) > min(randoms) * 5,
          f"sse from {min(randoms):.3f} to {max(randoms):.3f}")
    check("k-means++ is more reliable than random",
          sum(plusplus) / len(plusplus) <= sum(randoms) / len(randoms),
          f"mean sse: ++ {sum(plusplus) / len(plusplus):.3f} vs "
          f"random {sum(randoms) / len(randoms):.3f}")

    print(f"\n  {'all ok' if not fails else str(fails) + ' failed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())
