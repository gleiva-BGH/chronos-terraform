terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  profile = "default"  
  region  = "us-east-2"
}

output "hello_world" {
  value = "Hello, World!"
}