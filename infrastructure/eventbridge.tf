resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = module.dispatcher-lambda-function.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = module.eventbridge.eventbridge_rule_arns["schedule"]
}

module "eventbridge" {
  source  = "terraform-aws-modules/eventbridge/aws"
  version = "4.3.0"

  create_bus           = false
  attach_lambda_policy = true
  lambda_target_arns = [
    module.dispatcher-lambda-function.lambda_function_arn
  ]
  rules = {
    schedule = {
      description         = "Trigger every day"
      schedule_expression = "rate(1 day)"
      enabled             = true
    }
  }

  targets = {
    schedule = [
      {
        name = "Dispatcher Lambda"
        arn  = module.dispatcher-lambda-function.lambda_function_arn
      }
    ]
  }
}
