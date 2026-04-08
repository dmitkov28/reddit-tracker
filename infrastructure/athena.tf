resource "aws_athena_workgroup" "athena_wg" {
  name = "reddit-tracker"
  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/athena/"
    }
  }
}

resource "aws_athena_named_query" "threads_named_query" {
  name      = "LastTwoDaysFetchedThreads"
  database  = aws_glue_catalog_database.reddit.name
  workgroup = aws_athena_workgroup.athena_wg.id

  query = trimspace(<<-SQL
    UNLOAD (
      SELECT 
        id,
        title,
        selftext AS text,
        author,
        permalink,
        comments,
        upvotes,
        downvotes,
        CAST(from_unixtime(created) AS DATE) AS created_date,
        year,
        month,
        day
      FROM reddit.threads
      WHERE year = year(CURRENT_DATE)
        AND month = month(CURRENT_DATE)
        AND day = day(CURRENT_DATE)
        AND CAST(from_unixtime(created) AS DATE) >= CURRENT_DATE - INTERVAL '2' DAY
    ) TO 's3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/athena/threads/'
      WITH (
        format = 'PARQUET',
        compression = 'SNAPPY',
        partitioned_by = ARRAY['year', 'month', 'day']
      );
  SQL
  )
}

resource "aws_athena_named_query" "comments_named_query" {
  name      = "LastTwoDaysComments"
  database  = aws_glue_catalog_database.reddit.name
  workgroup = aws_athena_workgroup.athena_wg.id

  query = trimspace(<<-SQL
    UNLOAD (
      SELECT 
        id,
        thread_id,
        text,
        author,
        permalink,
        upvotes,
        downvotes,
        CAST(from_unixtime(created) AS DATE) AS created_date,
        year,
        month,
        day
    FROM reddit.comments
    WHERE year = year(CURRENT_DATE)
      AND month = month(CURRENT_DATE)
      AND day = day(CURRENT_DATE)
      AND CAST(from_unixtime(created) AS DATE) >= CURRENT_DATE - INTERVAL '2' DAY
    ) 
    TO 's3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/athena/comments/'
      WITH (
        format = 'PARQUET',
        compression = 'SNAPPY',
        partitioned_by = ARRAY['year', 'month', 'day']
      );
  SQL
  )
}


resource "aws_athena_named_query" "subreddits_named_query" {
  name      = "TodaySubreddits"
  database  = aws_glue_catalog_database.reddit.name
  workgroup = aws_athena_workgroup.athena_wg.id

  query = trimspace(<<-SQL
      UNLOAD (
        SELECT 
            id,
            name,
            subscribers,
            year(current_date) AS year,
            month(current_date) AS month,
            day(current_date) AS day
        FROM reddit.subreddits
        WHERE year = year(current_date)
          AND month = month(current_date)
          AND day = day(current_date)
      )
    TO 's3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/athena/subreddits'
    WITH (
      format = 'PARQUET',
      compression = 'SNAPPY',
      partitioned_by = ARRAY['year', 'month', 'day']
    );
  SQL
  )
}

