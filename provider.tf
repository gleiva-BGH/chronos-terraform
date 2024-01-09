terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" { 
  region  = "us-east-2"

  # default_tags {
  #   tags = {
  #     IAC = "true"
  #     Aplicacion = "Chronos"
  #   }
  # }
}

output "hello_world" {
  value = "Hello, World!"
}