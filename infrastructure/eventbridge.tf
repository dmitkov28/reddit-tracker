module "eventbridge" {
  source  = "terraform-aws-modules/eventbridge/aws"
  version = "4.3.0"

  create_bus      = false
  attach_sfn_policy = true
  sfn_target_arns = [
    module.step-functions.state_machine_arn
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
        name            = "Reddit Tracker Step Function"
        arn             = module.step-functions.state_machine_arn
        attach_role_arn = true
      }
    ]
  }
}
