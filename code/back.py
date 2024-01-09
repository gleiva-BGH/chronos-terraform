import boto3
import json
from botocore.exceptions import ClientError
import datetime as dt

# Nombre de la tabla en DynamoDB
table_name  =   'HorasExtra-table'
healthPath  =   '/health'
dataPath    =   '/data'

def lambda_handler(event, context):
    # Fecha y hora de la consulta
    now = dt.datetime.now()
    # Obtiene los datos del formulario desde el evento
    #print('Event:',event)
    eventPath       =   event['path']
    eventMethod     =   event['httpMethod']
    eventParameters =   event['queryStringParameters']
    print('Parameters: ', eventParameters)
    if eventPath == dataPath and eventMethod == 'POST':
        # Configura el cliente de DynamoDB
        dynamodb = boto3.client('dynamodb') 
        body_json   = json.loads(event['body'])
        #print("Body: ", body_json)
        ahora           = now.strftime("%Y-%m-%d, %H:%M:%S")
        nombre          = body_json['nombre']
        inicio          = dt.datetime.strptime(body_json['fecha_inicio']+', '+body_json['hora_inicio'], "%Y-%m-%d, %H:%M")
        inicio_str      = inicio.strftime("%Y-%m-%d, %H:%M")
        #hora_inicio    = body_json['hora_inicio']
        fin             = dt.datetime.strptime(body_json['fecha_fin']+', '+body_json['hora_fin'], "%Y-%m-%d, %H:%M")
        fin_str         = fin.strftime("%Y-%m-%d, %H:%M")
        #hora_fin        = body_json['hora_fin']
        diferencia      = fin-inicio
        total_horas     = round(diferencia.total_seconds()/3600,1)
        proyecto        = body_json['proyecto']
        motivo          = body_json['motivo']
        tipo            = body_json['tipo']
        sub             = body_json['sub']
        
        print('Total horas: '+str(total_horas))
        # Guarda los datos en DynamoDB
        try:
            response = dynamodb.put_item(
                TableName=table_name,
                Item={
                    'Fecha Generacion': {'S': ahora},
                    'Nombre':           {'S': nombre},
                    'Inicio':           {'S': inicio_str},
                    'Fin':              {'S': fin_str},
                    'Total Horas':      {'S': str(total_horas)},
                    'Project':          {'S': proyecto},
                    'Reason':           {'S': motivo},
                    'Type':             {'S': tipo},
                    'Sub':              {'S': sub},
                }
            )
            res = {    
                'statusCode': 200,
                'headers': { 
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Headers':'Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods':'POST'
                },
                'body': 'Datos guardados exitosamente'
            };
            return res;
        except ClientError as e:
            print('Error al guardar los datos:', e.response['Error']['Message'])
            res = {    
                'statusCode': 500,
                'body': 'Error al guardar los datos'
            };
            return res;
    if eventPath == dataPath and eventMethod == 'GET':
        # Configura el cliente de DynamoDB
        dynamodb = boto3.resource('dynamodb')
        if eventParameters.get('sub') != None:
            try:
                sub = eventParameters['sub']
                # Lectura de tabla
                table = dynamodb.Table(table_name)
                response = table.scan(
                    FilterExpression='#col = :id',
                    ExpressionAttributeNames={'#col': 'Sub'},
                    ExpressionAttributeValues={':id': sub}
                )
                items = response['Items']
                # Si la tabla tiene más elementos de los que se pueden devolver en una sola respuesta,
                # se puede utilizar la paginación para obtener todos los elementos.
                while 'LastEvaluatedKey' in response:
                    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                    items.extend(response['Items'])
                
                # Convertir la lista de elementos a JSON
                json_data = json.dumps(items)
                
                # Devolver los datos como respuesta de la función Lambda
                res = {    
                    'statusCode': 200,
                    'headers': { 
                        #'Content-Type': 'application/json',
                        'Access-Control-Allow-Headers':'Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods':'GET'
                    },
                    'body': json_data
                };
                return res;
            except Exception as e:
                print(f"Error al leer los datos de la tabla {table_name}: {str(e)}")
                res = {    
                    'statusCode': 500,
                    'body': 'Error al leer los datos de la tabla'
                };
                return res;
                raise
        else:
            try:
                # Obtiene fecha de inicio y final
                fecha_inicio=eventParameters['fecha_inicio']+', 00:00'
                fecha_fin=eventParameters['fecha_fin']+', 23:59'
                #print("Fechas recibidas: "+fecha_inicio+'-'+fecha_fin)
                # Lectura de tabla
                table = dynamodb.Table(table_name)
                response = table.scan(
                    FilterExpression='#dateAttr between :start and :end',
                    ExpressionAttributeNames={'#dateAttr': 'Inicio'},
                    ExpressionAttributeValues={':start': fecha_inicio, ':end': fecha_fin}
                )
                items = response['Items']
                # Si la tabla tiene más elementos de los que se pueden devolver en una sola respuesta,
                # se puede utilizar la paginación para obtener todos los elementos.
                while 'LastEvaluatedKey' in response:
                    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                    items.extend(response['Items'])
                
                # Convertir la lista de elementos a JSON
                json_data = json.dumps(items)
                
                # Devolver los datos como respuesta de la función Lambda
                res = {    
                    'statusCode': 200,
                    'headers': { 
                        #'Content-Type': 'application/json',
                        'Access-Control-Allow-Headers':'Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods':'GET'
                    },
                    'body': json_data
                };
                return res;
            except Exception as e:
                print(f"Error al leer los datos de la tabla {table_name}: {str(e)}")
                res = {    
                    'statusCode': 500,
                    'body': 'Error al leer los datos de la tabla'
                };
                return res;
                raise
    return {
                'statusCode': 200,
                'body': 'No hay recurso y/o metodo correspondiente'
            }