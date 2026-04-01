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

data "aws_iam_policy_document" "assume-role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam-for-lambda" {
  name               = "iam-for-transformer-function"
  assume_role_policy = data.aws_iam_policy_document.assume-role.json
}

resource "aws_lambda_permission" "allow-bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = module.transformer-lambda-function.lambda_function_arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.reddit-tracker-bucket.arn
}


resource "aws_s3_bucket_notification" "bucket-notification" {
  bucket = aws_s3_bucket.reddit-tracker-bucket.id

  lambda_function {
    lambda_function_arn = module.transformer-lambda-function.lambda_function_arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "_DONE"
    filter_suffix       = "_DONE"
  }

  depends_on = [aws_lambda_permission.allow-bucket]
}
