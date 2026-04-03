from duckdb import DuckDBPyConnection


def upsert_subreddits(ddb: DuckDBPyConnection, src_path: str):
    return ddb.execute(
        """INSERT INTO pg.public.subreddits(id, name)
       SELECT id, name FROM read_parquet(?)
       ON CONFLICT DO NOTHING;
    """,
        parameters=[src_path],
    )


def upsert_subreddit_subscribers(ddb: DuckDBPyConnection, src_path: str):
    return ddb.execute(
        """
    INSERT INTO pg.public.subreddit_subscribers (subreddit_id, subscriber_count)
    SELECT id, subscribers FROM read_parquet(?)
    """,
        parameters=[src_path],
    )


def upsert_threads(ddb: DuckDBPyConnection):
    return ddb.execute(
        """
    INSERT INTO pg.public.threads (id, title, text, author, permalink, comments, upvotes, downvotes, subreddit, created_date)
    SELECT
        t.id, t.title, t.text, t.author, t.permalink, t.comments, t.upvotes, t.downvotes,
        s.id, t.created_date
    FROM read_parquet(?) AS t
    JOIN read_parquet(?) AS s
        ON s.name = TRIM(SPLIT_PART(t.permalink, 'comments', 1), '/')
    ON CONFLICT DO NOTHING;
    """,
        parameters=[
            "s3://rt-reddit-tracker-bucket/athena/looker/threads/*",
            "s3://rt-reddit-tracker-bucket/athena/looker/subreddits/*",
        ],
    )


def upsert_comments(ddb: DuckDBPyConnection): ...
