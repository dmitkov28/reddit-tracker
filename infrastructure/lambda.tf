module "fetcher-lambda-function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "8.7.0"

  function_name = "reddit-tracker-fetcher"
  description   = "Reddit Tracker Fetcher"
  architectures = ["arm64"]

  create_package = false
  memory_size    = 1024
  timeout        = 120

  environment_variables = {
    "HTTP_PROXY" = var.http_proxy
    "BUCKET"     = aws_s3_bucket.reddit-tracker-bucket.bucket
  }

  image_uri    = "${module.reddit-tracker-ecr.repository_url}:${var.image_tag}"
  package_type = "Image"

  ignore_source_code_hash = true

  cloudwatch_logs_retention_in_days = 5

  attach_policy_statements = true
  policy_statements = {
    ecr_pull = {
      effect = "Allow"
      actions = [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetAuthorizationToken"
      ]
      resources = ["*"]
    }
    bucket_rw = {
      effect = "Allow"
      actions = [
        "s3:GetObject",
        "s3:PutObject"
      ]
      resources = ["${aws_s3_bucket.reddit-tracker-bucket.arn}/*"]
    }
  }

  tags = { "Terraform" : true }
}

module "dispatcher-lambda-function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "8.7.0"

  function_name = "reddit-tracker-dispatcher"
  description   = "Reddit Tracker Dispatcher"
  architectures = ["arm64"]

  create_package = true
  source_path    = "../dispatcher/main.py"
  trigger_on_package_timestamp = false

  memory_size    = 128
  timeout        = 15

  runtime = "python3.13"
  handler = "main.lambda_handler"

  environment_variables = {
    "BUCKET"  = aws_s3_bucket.reddit-tracker-bucket.bucket
    "FETCHER" = module.fetcher-lambda-function.lambda_function_name
  }

  package_type = "Zip"

  cloudwatch_logs_retention_in_days = 5

  attach_policy_statements = true
  policy_statements = {
    bucket_read = {
      effect = "Allow"
      actions = [
        "s3:GetObject",
        "s3:ListBucket"
      ]
      resources = [
        aws_s3_bucket.reddit-tracker-bucket.arn,
        "${aws_s3_bucket.reddit-tracker-bucket.arn}/*"
      ]
    }
    invoke_lambda = {
      effect = "Allow"
      actions = [
        "lambda:InvokeFunction"
      ]
      resources = [
        module.fetcher-lambda-function.lambda_function_arn
      ]
    }
  }

  tags = { "Terraform" : true }
}

module "transformer-lambda-function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "8.7.0"

  function_name = "reddit-tracker-transformer"
  description   = "Reddit Tracker Transformer"
  architectures = ["arm64"]

  create_package = true
  source_path    = "../transformer/main.py"
  trigger_on_package_timestamp = false
  
  memory_size    = 128
  timeout        = 15

  runtime = "python3.13"
  handler = "main.lambda_handler"

  environment_variables = {
    "BUCKET"    = aws_s3_bucket.reddit-tracker-bucket.bucket
    "ATHENA_DB" = aws_glue_catalog_database.reddit.name
  }

  package_type = "Zip"

  cloudwatch_logs_retention_in_days = 5

  attach_policy_statements = true
  policy_statements = {
    bucket_read = {
      effect = "Allow"
      actions = [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutObject"
      ]
      resources = [
        aws_s3_bucket.reddit-tracker-bucket.arn,
        "${aws_s3_bucket.reddit-tracker-bucket.arn}/*"
      ]
    }
    glue_read = {
      effect = "Allow"
      actions = [
        "glue:GetTable",
        "glue:GetDatabase",
        "glue:GetPartitions"
      ]
      resources = [
        aws_glue_catalog_database.reddit.arn
      ]
    }
    athena_query = {
      effect = "Allow"
      actions = [
        "athena:StartQueryExecution"
      ]
      resources = [
        "*"
      ]
    }

  }

  tags = { "Terraform" : true }
}
