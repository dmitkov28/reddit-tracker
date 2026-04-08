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
        CAST(from_unixtime(created) AS DATE) AS created_date
      FROM reddit.threads
      WHERE year = year(CURRENT_DATE)
        AND month = month(CURRENT_DATE)
        AND day = day(CURRENT_DATE)
        AND CAST(from_unixtime(created) AS DATE) >= CURRENT_DATE - INTERVAL '2' DAY
    ) TO CONCAT(
        's3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/athena/',
        date_format(current_date, '%m-%d-%Y'),
        '/threads/',
        date_format(current_timestamp, '%H-%i-%s'),
        '/'
      )
      WITH (
        format = 'PARQUET',
        compression = 'SNAPPY'
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
        CAST(from_unixtime(created) AS DATE) AS created_date
    FROM comments
    WHERE year = year(CURRENT_DATE)
      AND month = month(CURRENT_DATE)
      AND day = day(CURRENT_DATE)
      AND CAST(from_unixtime(created) AS DATE) >= CURRENT_DATE - INTERVAL '2' DAY
    ) 
    TO CONCAT(
        's3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/athena/',
        date_format(current_date, '%m-%d-%Y'),
        '/comments/',
        date_format(current_timestamp, '%H-%i-%s'),
        '/'
      )
      WITH (
        format = 'PARQUET',
        compression = 'SNAPPY'
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
            subscribers
        FROM subreddits
        WHERE year = year(current_date)
          AND month = month(current_date)
          AND day = day(current_date)
      )
      TO CONCAT(
        's3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/athena/',
        date_format(current_date, '%m-%d-%Y'),
        '/subreddits/',
        date_format(current_timestamp, '%H-%i-%s'),
        '/'
      )
      WITH (
        format = 'PARQUET',
        compression = 'SNAPPY'
      );
  SQL
  )
}

