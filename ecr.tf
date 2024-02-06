resource "aws_ecr_repository" "api" {
  name                 = "chronos-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}