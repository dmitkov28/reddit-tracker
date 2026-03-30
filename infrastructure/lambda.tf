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
