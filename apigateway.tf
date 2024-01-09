resource "aws_api_gateway_rest_api" "chronos" {
  body = jsonencode({
    openapi = "3.0.1"
    info = {
      title   = "example"
      version = "1.0"
    }
    paths = {
      "/horas" = {
        get = {
          x-amazon-apigateway-integration = {
            httpMethod           = "GET"
            payloadFormatVersion = "1.0"
            type                 = "HTTP_PROXY"
            uri                  = "https://ip-ranges.amazonaws.com/ip-ranges.json"
          }
        },
        post = {
          x-amazon-apigateway-integration = {
            httpMethod           = "POST"
            payloadFormatVersion = "1.0"
            type                 = "HTTP_PROXY"
            uri                  = "https://ip-ranges.amazonaws.com/ip-ranges.json"
          }
        }
      }
    }
  })

  name = "Chronos"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_deployment" "chronos" {
  rest_api_id = aws_api_gateway_rest_api.chronos.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.chronos.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "chronos-dev" {
  deployment_id = aws_api_gateway_deployment.chronos.id
  rest_api_id   = aws_api_gateway_rest_api.chronos.id
  stage_name    = "dev"
}