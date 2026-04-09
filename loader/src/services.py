from typing import Literal

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

    subreddits = ddb.query(
        """
    SELECT 
        DISTINCT(id),
        name,
        subscribers,
        MAKE_DATE(year, month, day) AS date
    FROM read_parquet(?)
    ORDER BY date DESC
    """,
        params=[src_path],
    )

    ddb.register("subreddits", subreddits)

    ddb.execute(
        """
    INSERT INTO pg.public.subreddit_subscribers(subreddit_id, subscriber_count, date)
       SELECT 
           id AS subreddit_id, 
           subscribers AS subscriber_count, 
           date 
       FROM subreddits
       WHERE (id, date) NOT IN (
           SELECT subreddit_id, date 
           FROM pg.public.subreddit_subscribers
       );
    """
    )


def upsert_threads(ddb: DuckDBPyConnection, src_path: str):
    threads = ddb.query(
        """
    SELECT
        DISTINCT(id),
        title,
        text,
        author,
        permalink,
        comments,
        upvotes,
        downvotes,
        subreddit,
        created_date
    FROM read_parquet(?)
    """,
        params=[src_path],
    )

    ddb.register("threads", threads)

    ddb.query(
        """
    INSERT INTO pg.public.threads (id, title, text, author, permalink, comments, upvotes, downvotes, subreddit, created_date)
    SELECT
        id,
        title,
        text,
        author,
        permalink,
        comments,
        upvotes,
        downvotes,
        subreddit,
        created_date
    FROM threads
    ON CONFLICT DO NOTHING
    """
    )


def upsert_comments(ddb: DuckDBPyConnection, src_path: str):
    comments = ddb.query(
        """
    SELECT
        DISTINCT(id),
        thread_id,
        text,
        author,
        permalink,
        upvotes,
        downvotes,
        created_date
    FROM read_parquet(?)
    """,
        params=[src_path],
    )

    ddb.register("comments", comments)

    ddb.query(
        """
    INSERT INTO pg.public.comments (id, thread_id, text, author, permalink, upvotes, downvotes, created_date)
    SELECT
        id,
        thread_id,
        text,
        author,
        permalink,
        upvotes,
        downvotes,
        created_date
    FROM comments
    ON CONFLICT DO NOTHING
    """
    )


def get_service(query_type: Literal["subreddits", "threads", "comments"]):
    services = {
        "subreddits": upsert_subreddit_subscribers,
        "threads": upsert_threads,
        "comments": upsert_comments,
    }
    return services[query_type]
