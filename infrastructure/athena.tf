resource "aws_athena_workgroup" "athena_wg" {
  name = "reddit-tracker"
  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.reddit-tracker-bucket.bucket}/athena/"
    }
  }
}

