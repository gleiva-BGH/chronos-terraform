resource "aws_eip" "api" {
  instance = aws_instance.api.id
  domain   = "vpc"
  tags = {
    Name = "eip-Chronos"
  }
}