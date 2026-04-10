module "step-functions" {
  source  = "terraform-aws-modules/step-functions/aws"
  version = "5.1.0"
  name    = "Reddit_Tracker_Step_Function"

  type = "STANDARD"

  create_role = true
  role_name   = "reddit-tracker-step-function-role"

  definition = templatefile("${path.module}/step_function.asl.json", {
    fetcher_function_name = module.fetcher-lambda-function.lambda_function_name
    loader_function_name  = module.loader-lambda-function.lambda_function_name
    bucket_name           = aws_s3_bucket.reddit-tracker-bucket.bucket
    subreddits_query_id   = aws_athena_named_query.subreddits_named_query.id
    threads_query_id      = aws_athena_named_query.threads_named_query.id
    comments_query_id     = aws_athena_named_query.comments_named_query.id
  })

  attach_policy_statements = true
  policy_statements = {
    stepfunction = {
      effect    = "Allow"
      actions   = ["states:StartExecution"]
      resources = [module.step-functions.state_machine_arn]
    }
    athena = {
      effect = "Allow"
      actions = [
        "athena:GetNamedQuery",
        "athena:GetQueryExecution"
      ]
      resources = [aws_athena_workgroup.athena_wg.arn]
    }
  }

  service_integrations = {
    lambda = {
      lambda = [
        module.fetcher-lambda-function.lambda_function_arn,
        module.loader-lambda-function.lambda_function_arn
      ]
    }
    

    athena_StartQueryExecution = {
      athena = [aws_athena_workgroup.athena_wg.arn]
      s3 = [
        aws_s3_bucket.reddit-tracker-bucket.arn,
        "${aws_s3_bucket.reddit-tracker-bucket.arn}/*"
      ]
      glue = [
        "arn:aws:glue:eu-central-1:${data.aws_caller_identity.current.account_id}:catalog",
        aws_glue_catalog_database.reddit.arn,
        "arn:aws:glue:eu-central-1:${data.aws_caller_identity.current.account_id}:table/${aws_glue_catalog_database.reddit.name}/*"
      ]
    }

    athena_GetQueryExecution = {
      athena = [aws_athena_workgroup.athena_wg.arn]
    }

    athena_GetQueryResults = {
      athena = [aws_athena_workgroup.athena_wg.arn]
      s3 = [
        aws_s3_bucket.reddit-tracker-bucket.arn,
        "${aws_s3_bucket.reddit-tracker-bucket.arn}/*"
      ]
    }
  }

  tags = {
    Terraform = true
  }
}
