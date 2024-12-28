# OPS by Sample Size

```bash
benchman report --columns=full_name,python,best,ops,ops_rel,stdev --sort=-ops_rel --filter="python ^= 3.12"
```

| Full Name                     | Python   |        Best |           maxOPS |           OPSrel |   Std Dev (σ) |
|:------------------------------|:---------|------------:|-----------------:|-----------------:|--------------:|
| sort(builtin, n=10)           | 3.12.6   | 6.44051e-08 |      7.76336e+13 |      7.76336e+12 |   1.37284e-09 |
| sort(insertion_sort, n=10)    | 3.12.6   | 4.34405e-07 |      1.151e+12   |      1.151e+11   |   8.15995e-10 |
| sort(builtin, n=100)          | 3.12.6   | 2.51645e-07 |      3.97386e+12 |      3.97386e+10 |   9.16946e-10 |
| sort(bubble_sort, n=10)       | 3.12.6   | 1.66536e-06 |      1.20094e+11 |      1.20094e+10 |   4.22077e-08 |
| sort(quick_sort, n=10)        | 3.12.6   | 3.32875e-06 |      3.00413e+10 |      3.00413e+09 |   1.55785e-08 |
| sort(insertion_sort, n=100)   | 3.12.6   | 3.78641e-06 |      2.64102e+10 |      2.64102e+08 |   9.66475e-07 |
| sort(builtin, n=1,000)        | 3.12.6   | 1.89847e-06 |      1.05348e+11 |      1.05348e+08 |   8.71486e-09 |
| sort(quick_sort, n=100)       | 3.12.6   | 4.23774e-05 |      1.17987e+08 |      1.17987e+06 |   2.15686e-07 |
| sort(bubble_sort, n=100)      | 3.12.6   | 0.000101348 |      1.9734e+07  | 197340           |   4.24434e-07 |
| sort(insertion_sort, n=1,000) | 3.12.6   | 5.85265e-05 |      8.54314e+07 |  85431.4         |   2.57419e-07 |
| sort(quick_sort, n=1,000)     | 3.12.6   | 0.000700299 | 713980           |    713.98        |   1.34063e-05 |
| sort(bubble_sort, n=1,000)    | 3.12.6   | 0.0150056   |   1332.84        |      1.33284     |   1.5607e-05  |

Filter: 'python ^= 3.12', 60 -> 12 rows


# Ops by python

> Client: arm64_16_GB, Darwin_24.1.0

| Name   | Variant        | Samples   | 3.9.20   | 3.10.15   | 3.11.10   | 3.12.6   | 3.13.0   |
|:-------|:---------------|:----------|:---------|:----------|:----------|:---------|:---------|
| sort   | builtin        | 10        | 9.648 M  | 9.904 M   | 14.424 M  | 15.651 M | 16.767 M |
| sort   | bubble_sort    | 1,000     | 0.000 M  | 0.000 M   | 0.000 M   | 0.000 M  | 0.000 M  |
| sort   | builtin        | 100       | 2.621 M  | 2.638 M   | 2.849 M   | 3.973 M  | 3.829 M  |
| sort   | quick_sort     | 10        | 0.224 M  | 0.211 M   | 0.251 M   | 0.298 M  | 0.253 M  |
| sort   | quick_sort     | 1,000     | 0.001 M  | 0.001 M   | 0.001 M   | 0.001 M  | 0.001 M  |
| sort   | insertion_sort | 1,000     | 0.012 M  | 0.013 M   | 0.020 M   | 0.017 M  | 0.013 M  |
| sort   | builtin        | 1,000     | 0.332 M  | 0.332 M   | 0.335 M   | 0.528 M  | 0.474 M  |
| sort   | insertion_sort | 10        | 1.260 M  | 1.269 M   | 1.743 M   | 2.310 M  | 1.598 M  |
| sort   | quick_sort     | 100       | 0.019 M  | 0.017 M   | 0.021 M   | 0.024 M  | 0.015 M  |
| sort   | insertion_sort | 100       | 0.141 M  | 0.145 M   | 0.217 M   | 0.264 M  | 0.165 M  |
| sort   | bubble_sort    | 10        | 0.355 M  | 0.352 M   | 0.452 M   | 0.601 M  | 0.516 M  |
| sort   | bubble_sort    | 100       | 0.005 M  | 0.005 M   | 0.007 M   | 0.010 M  | 0.007 M  |

Benchmark date: 2024-12-27T08:25:55.590253+00:00
Fixed dataset values: client='61bdee7c56e0e5f7', debug_mode=False, hardware='arm64_16_GB', name='sort', project='benchman', system='Darwin_24.1.0', tag='latest', version='0.0.1'.
Variant dataset values: python, sample_size, variant.
: Showing 12 of 60 rows.
Sort order: name.