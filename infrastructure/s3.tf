resource "aws_s3_bucket" "reddit-tracker-bucket" {
  bucket = "rt-reddit-tracker-bucket"
}

resource "aws_s3_bucket_lifecycle_configuration" "reddit-tracker-bucket-lifecycle-config" {
  bucket = aws_s3_bucket.reddit-tracker-bucket.id

  rule {
    id = "expire-raw-threads-after-14-days"

    status = "Enabled"

    filter {
      prefix = "threads/"
    }

    expiration {
      days = 14
    }
  }

  rule {
    id = "expire-raw-subreddits-after-14-days"

    status = "Enabled"

    filter {
      prefix = "subreddits/"
    }

    expiration {
      days = 14
    }
  }

  rule {
    id = "expire-raw-comments-after-14-days"

    status = "Enabled"

    filter {
      prefix = "comments/"
    }

    expiration {
      days = 14
    }
  }

  rule {
    id = "expire-athena-outputs-after-14-days"

    status = "Enabled"

    filter {
      prefix = "athena/"
    }

    expiration {
      days = 14
    }
  }
}
