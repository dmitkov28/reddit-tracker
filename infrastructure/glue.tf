resource "aws_glue_catalog_database" "glue-db" {
  name = "reddit"
}

resource "aws_iam_role" "glue-crawler-role" {
  name = "reddit-threads-glue-crawler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue-service-policy" {
  role       = aws_iam_role.glue-crawler-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "s3-access-policy" {
  role       = aws_iam_role.glue-crawler-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy" "glue-custom-s3-policy" {
  name = "reddit-glue-crawler-s3-policy"
  role = aws_iam_role.glue-crawler-role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.reddit-tracker-bucket.arn,
          "${aws_s3_bucket.reddit-tracker-bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_glue_crawler" "glue-crawler-threads" {
  database_name = aws_glue_catalog_database.glue-db.name
  name          = "reddit-threads-crawler"
  role          = aws_iam_role.glue-crawler-role.arn

  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }


  s3_target {
    path = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/threads/"
  }
}

resource "aws_glue_crawler" "glue-crawler-comments" {
  database_name = aws_glue_catalog_database.glue-db.name
  name          = "reddit-comments-crawler"
  role          = aws_iam_role.glue-crawler-role.arn

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }

  recrawl_policy {
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }


  s3_target {
    path = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/comments/"
  }
}
