resource "aws_instance" "web" {
  ami           = "ami-05fb0b8c1424f266b"
  instance_type = "t3.micro"

  tags = {
    Name = "Chronos"
  }
}