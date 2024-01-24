provider "aws" { 
  region  = "us-east-2"
  
  default_tags {
    tags = {
      IAC = "true"
      Aplicacion = "Chronos"
    }
  }
}

terraform {
  cloud {
    organization = "BGH-Cloud-Tech"
    workspaces {
      name = "chronos-terraform"
    }
  }

  required_version = ">= 1.1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}