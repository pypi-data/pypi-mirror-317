from datetime import datetime, timedelta
import logging
import ssl
from typing import Optional
import aio_pika
from fastapi import HTTPException, Header
import jwt
import pika
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from collections import namedtuple
import consul

### 
### Funciones para enviar mensajes a RabbitMQ ###
###

def get_rabbitmq_channel(exchange: str, exchange_type: str, config: dict):
    """
    Crea un canal de comunicación con RabbitMQ y declara un exchange con el tipo correspondiente.
    
    Args:
        exchange (str): Nombre del exchange.
        exchange_type (str): Tipo de exchange. Puede ser 'direct', 'topic', 'fanout' o 'headers'.
        config (dict): Configuración de RabbitMQ. Debe contener las claves 'RABBIT_HOST', 'RABBIT_USER' y 'RABBIT_PASSWORD'.
        
    Returns:
        pika.channel.Channel: Canal de comunicación con RabbitMQ.
    """
    # SSL
    context = ssl.create_default_context(cafile="/certs/ca_certificate.pem")
    context.load_cert_chain(certfile="/certs/client_certificate.pem", keyfile="/certs/client_key.pem", password="microservice")
    
    ssl_options = pika.SSLOptions(context, config.RABBIT_HOST)
    
    
    # Autenticación con credenciales
    credentials = pika.PlainCredentials(config.RABBIT_USER, config.RABBIT_PASSWORD)
    
    # Conexión con RabbitMQ
    connection_params = pika.ConnectionParameters(
        host=config.RABBIT_HOST,
        credentials=credentials,
        port=5671,
        ssl_options=ssl_options
    )
    
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    # Declarar el exchange con el tipo correspondiente
    try:
        channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)
    except Exception as e:
        print(f"Error declaring exchange: {e}")
    return channel

def send_topic_message(
    message: str, routing_key: str, exchange: str, config: dict, 
    reply_to: Optional[str] = None, headers: Optional[dict] = None
):
    """
    Envía un mensaje a un exchange de tipo 'topic' con una clave de enrutamiento.
    """
    # Construcción del mensaje que mantiene la compatibilidad
    message_payload = {
        "message": message
    }
    
    channel = get_rabbitmq_channel(exchange, 'topic', config=config)
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=json.dumps(message_payload),
        properties=pika.BasicProperties(
            reply_to=reply_to,
            headers=headers
        )
    )
    channel.close()
    
async def rabbit_keys_callback(message: aio_pika.IncomingMessage):
    """Callback asincrono para manejar mensajes recibidos de RabbitMQ."""
    async with message.process():  # Esto confirma el mensaje automáticamente
        body = json.loads(message.body)["message"]
        print(f"Received pieces data: {body}")
        
        public_key_decoded = body['public_key_pem']
        public_key = public_key_decoded.encode('utf-8')
        
        with open('public_key.pem', 'wb') as f:
            f.write(public_key)
            
###
### Funciones para consul
###

def set_public_key():
    c = consul.Consul(host='consul', port=8500)
    key, value = c.kv.get('auth/public_key')
    if value:  # Verifica si la clave existe y tiene un valor
        pub_key = value["Value"]
        logger.log(level='INFO', message=f"Public key found in Consul {pub_key}")
        with open('public_key.pem', 'wb') as public_key_file:
            public_key_file.write(pub_key)
    else:
        logger.log(level='ERROR', message="La clave 'auth/public_key' no existe o no tiene valor.")
    
    
###
### Funciones genericas de la base de datos ###
###

async def get_list(db: AsyncSession, model):
    """
    Retrieve a list of elements from database
    
    Args:
        db (AsyncSession): Database session
        model: Database model to retrieve
        
    Returns:
        list: List of elements
    """
    result = await db.execute(select(model))
    item_list = result.unique().scalars().all()
    return item_list


async def get_list_statement_result(db: AsyncSession, stmt):
    """
    Execute given statement and return list of items.
    
    Args:
        db (AsyncSession): Database session
        stmt: Statement to execute
        
    Returns:
        list: List of items
    """
    result = await db.execute(stmt)
    item_list = result.unique().scalars().all()
    return item_list


async def get_element_statement_result(db: AsyncSession, stmt):
    """
    Execute statement and return a single items
    
    Args:
        db (AsyncSession): Database session
        stmt: Statement to execute
        
    Returns:
        Any: Single item
    """
    result = await db.execute(stmt)
    item = result.scalar()
    return item


async def get_element_by_id(db: AsyncSession, model, element_id):
    """
    Retrieve any DB element by id.
    
    Args:
        db (AsyncSession): Database session
        model: Database model to retrieve
        element_id: ID of the element to retrieve
        
    Returns:
        Any: Element retrieved
    """
    if element_id is None:
        return None

    element = await db.get(model, element_id)
    return element

###
### Funciones de jwt ###
###

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
    
def create_access_token(data: dict, expires_delta: timedelta = None, private_key_pem: bytes = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, private_key_pem, algorithm=ALGORITHM)

def create_refresh_token(data: dict, private_key_pem: bytes = None):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, private_key_pem, algorithm=ALGORITHM)

# Esta funcion al chasis de la aplicacion
def decode_refresh_token(token: str, public_key_client_pem: bytes = None):
    try:
        payload = json.loads(json.dumps(jwt.decode(token, public_key_client_pem, [ALGORITHM])))
        return payload
    except Exception as exc:  # @ToDo: To broad exception
        logging.error(f"Error decoding the token: {exc}")
        # raise_and_log_error(logger, status.HTTP_403_CONFLICT, f"Error decoding the token: {exc}")
        
def decode_jwt(token: str, public_key_client_pem: bytes = None):
    try:
        payload = json.loads(json.dumps(jwt.decode(token, public_key_client_pem, [ALGORITHM])))
        return payload
    except Exception as exc:  # @ToDo: To broad exception
        logging.error(f"Error decoding the token: {exc}")
    
async def get_user_info(Authorization: str = Header(..., description="JWT Token")):
    try:
        with open("public_key.pem", "rb") as f:
            public_key = f.read()

        if public_key is None:
            logging.error("No se ha encontrado la clave pública")
            raise HTTPException(status_code=401, detail="No se ha encontrado la clave pública")
        payload = jwt.decode(Authorization, public_key, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")  # Extrae el user_id
        role = payload.get("role")  # Extrae el rol del payload
        if role == 1:
            is_admin = True
        else:
            is_admin = False
            
        # logging.info(f"User ID: {user_id}, Is admin: {is_admin}")
        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Token inválido: faltante user_id o role")
        # return user_id, is_admin  # Devuelve ambos valores como una tupla
        # return {'user_id': user_id, 'is_admin': is_admin}
        return namedtuple('UserInfo', ['user_id', 'is_admin'])(user_id, is_admin)
    except jwt.ExpiredSignatureError as e:
        logging.error(f"Token expirado: {e}")
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    except Exception as e:
        logging.error(f"Error: {e}")
        
        