resource "aws_dynamodb_table" "chronos-horas" {
  name                        = "Chronos-Horas"
  billing_mode                = "PROVISIONED"
  deletion_protection_enabled = false
  hash_key                    = "Fecha Generacion"
  read_capacity               = 1
  stream_enabled              = false
  table_class                 = "STANDARD"
  write_capacity              = 1
  attribute {
    name = "Fecha Generacion"
    type = "S"
  }
  point_in_time_recovery {
    enabled = false
  }
  ttl {
    attribute_name = ""
    enabled        = false
  }
}