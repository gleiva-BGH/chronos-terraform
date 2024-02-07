resource "aws_ecr_repository" "api" {
  name                 = "chronos-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}
resource "aws_ecr_lifecycle_policy" "api" {
  repository = aws_ecr_repository.api.name

  policy = file("policies/ecr-lifecycle-policy-expire-untagged.json")
}