# Query Optimization

The course system uses two composite PostgreSQL B-tree indexes:

```sql
CREATE INDEX idx_animal_state_record_aid_datetime
    ON public.animal_state_record (a_id, datetime DESC);
CREATE INDEX idx_feeding_records_aid_feeddate
    ON public.feeding_records (a_id, feed_date DESC);
```

Both are designed for filtering on an animal identifier and retrieving recent observations in descending time order. For a matching predicate and ordering, PostgreSQL may choose an index scan to reduce scanning and sorting work. The query planner's choice depends on data distribution, statistics, and the query.

## Reported course measurements

The course final report records five elapsed-time observations per condition for each of two workloads. The presentation identifies the workloads as feeding history and animal trends. The [raw timing table](../results/index_benchmark.csv) retains these observations; [summary statistics](../results/index_benchmark_summary.csv) use arithmetic means and sample standard deviations. The mean speedup is the unindexed mean divided by the indexed mean.

| Workload | Unindexed mean (ms) | Indexed mean (ms) | Speedup |
|---|---:|---:|---:|
| Feeding history | 9.58 | 1.58 | 6.06× |
| Animal trends | 9.68 | 1.24 | 7.81× |

These are workload-specific historical measurements from a small course benchmark. The exact timed commands, plans and cache conditions are not available. The [representative SQL queries](../sql/analytical_queries.sql) and [EXPLAIN examples](../sql/explain_examples.sql) illustrate relevant access patterns for plan inspection on a populated local database; they are not claimed as the exact historical benchmark queries.
