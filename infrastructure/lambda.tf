module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "8.7.0"

  function_name = "reddit-tracker"
  description   = "Reddit Tracker"
  architectures = ["arm64"]

  create_package = false
  memory_size    = 1024
  timeout        = 120

  image_uri    = "${reddit_tracker_ecr.reddit_tracker_ecr_uri}:${var.image_tag}"
  package_type = "Image"

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
  }

  tags = { "Terraform" : true }
}
