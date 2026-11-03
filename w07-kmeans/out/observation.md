# Week 7 observations

## Task 1

- Empty clusters keep their previous centroid; moving one to the farthest point could reseed it, but would change later assignments.
- Across 40 seeds, random initialization found the three blobs (SSE < 1) 24 times; k-means++ did so 40 times. Its extra initial distance calculations make better starts more reliable, which is useful when bad local optima are costly; random starts are cheaper when many restarts or a quick rough result is acceptable.
- SSE cannot select `k`: it never increases when `k` grows, and reaches zero at `k = n`. Use a separate criterion or validation goal to balance fit and complexity.

## Task 2

- At 1,000 points, contrast fell below 1 at 50 dimensions and below 0.5 at 200; at 20 dimensions it rose from 1.787 (200 points) to 2.448 (2,000 points), showing that extremes depend on sample size too.
- Mean distance tracked roughly `sqrt(d)`, while relative SD fell from 0.476 (2D) to 0.041 (200D). Relative SD captures typical distance concentration; contrast is more sensitive to `n` and sampled extremes.
- Euclidean cube measurements do not directly threaten Jaccard LSH: shingle sets have a different similarity and distribution. Measure contrast on those sets before drawing a conclusion.

## Task 3

- Per point, the algorithm stores an upper bound to its assigned center and a lower bound to every competing center, in addition to the label. Updating these costs two scalar adjustments per point; center movement costs `k` distances per pass, and separation costs `k(k−1)/2` distances.
- The lower bound did more pruning: 465,980 lower-only decisions versus 37,273 separation-only; both bounds passed on 242,930 decisions. These counts are pruning decisions, not distance calls.
- SSE exactly matched the baseline (10,737,882.94) while calls fell 86.7%. The first iteration used about 17.5% of all calls because no point has a valid bound before its first full assignment.
