module "reddit-tracker-ecr" {
  source  = "terraform-aws-modules/ecr/aws"
  version = "3.2.0"

  repository_name          = "reddit-tracker-ecr"
  repository_force_delete  = true
  attach_repository_policy = false

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep latest tag forever (1 max)",
        selection = {
          tagStatus     = "tagged",
          tagPrefixList = ["latest"],
          countType     = "imageCountMoreThan",
          countNumber   = 1
        },
        action = { type = "expire" }
      },
      {
        rulePriority = 2,
        description  = "Keep last 3 sha- images",
        selection = {
          tagStatus     = "tagged",
          tagPrefixList = ["sha-"],
          countType     = "imageCountMoreThan",
          countNumber   = 3
        },
        action = { type = "expire" }
      },
      {
        rulePriority = 3,
        description  = "Delete untagged images after 1 day",
        selection = {
          tagStatus   = "untagged",
          countType   = "sinceImagePushed",
          countUnit   = "days",
          countNumber = 1
        },
        action = { type = "expire" }
      }
    ]
  })

  tags = {
    Terraform = "true"
  }
}

output "reddit-tracker-ecr-uri" {
  value = module.reddit-tracker-ecr.repository_url
}
