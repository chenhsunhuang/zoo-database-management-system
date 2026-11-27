# Transaction Management and Concurrency Control

The core team implementation is `ZooBackend.add_feeding_record` in [`DB_utils.py`](https://github.com/pollop123/zoo_db/blob/main/DB_utils.py). It validates a positive feeding amount and checks the employee's shift permission before opening the write workflow.

## Atomic update

Within the PostgreSQL connection, the method locks the selected feed master row and locks `feeding_records` and `feeding_inventory` in `SHARE ROW EXCLUSIVE` mode. It sums signed inventory movements for the feed and rolls back when stock is insufficient. When stock is sufficient, it allocates identifiers, inserts the feeding record and inserts a linked negative inventory movement before committing. Exceptions are handled through the connection context.

Representative lock and stock-check statements:

```sql
SELECT f_id FROM public.feeds WHERE f_id = 'F001' FOR UPDATE;
LOCK TABLE public.feeding_records, public.feeding_inventory
    IN SHARE ROW EXCLUSIVE MODE;
SELECT COALESCE(SUM(quantity_delta_kg), 0)
FROM public.feeding_inventory WHERE f_id = 'F001';
```

The statements are executed as part of the backend transaction, not as independent commands. The feed-row lock coordinates writers that follow the same locking protocol. The table locks serialize identifier generation based on the maximum existing numeric identifier and protect the associated insert path. This coarse-grained approach trades write concurrency for simpler coordination; database sequences would be a natural alternative for identifier allocation.

The original project includes a [concurrency demonstration](https://github.com/pollop123/zoo_db/blob/main/test/test_lock_demo.py) for concurrent feeding and lock waiting. It operates on demonstration data and may restore a database backup. Use an isolated local demonstration database when running it.
