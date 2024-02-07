# #IMPORT API GATEWAY - REST
# import {
#   to = aws_api_gateway_rest_api.chronos
#   id = "z218y79q98"
# }
# import {
#   to = aws_dynamodb_table.basic-dynamodb-table
#   id = "HorasExtra-table"
# }
import {
  to = aws_instance.api
  id = "i-08a595754c85377a4"
}