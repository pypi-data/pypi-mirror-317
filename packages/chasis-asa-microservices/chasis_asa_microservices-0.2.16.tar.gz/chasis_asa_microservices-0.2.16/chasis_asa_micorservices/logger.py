import logging
from typing import Any, Dict, Optional
from colorama import Fore, Style
from . import send_topic_message

class MyLogger:
    _instances = {}

    def __new__(cls, name: str, *args, **kwargs):
        if name in cls._instances:
            # Actualiza los valores si ya existe el logger
            instance = cls._instances[name]
            instance._update_config(**kwargs)
            return instance
        instance = super().__new__(cls)
        cls._instances[name] = instance
        return instance

    def __init__(self, name: str, rabbitmq_config: Optional[Dict[str, Any]] = None, routing_key: Optional[str] = None, 
                 exchange: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        if hasattr(self, "_initialized") and self._initialized:
            self._update_config(
                rabbitmq_config=rabbitmq_config,
                routing_key=routing_key,
                exchange=exchange,
                headers=headers
            )
            return  # Evita reinicialización en caso de reutilización
        self._initialized = True

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:  # Evita agregar múltiples handlers
            handler = logging.StreamHandler()
            handler.setFormatter(self._get_color_formatter())
            self.logger.addHandler(handler)

        # Configuración inicial
        self.rabbitmq_config = rabbitmq_config
        self.routing_key = routing_key
        self.exchange = exchange
        self.headers = headers or {}

    def _update_config(self, rabbitmq_config=None, routing_key=None, exchange=None, headers=None):
        if rabbitmq_config:
            self.rabbitmq_config = rabbitmq_config
        if routing_key:
            self.routing_key = routing_key
        if exchange:
            self.exchange = exchange
        if headers:
            self.headers.update(headers or {})

    def _get_color_formatter(self):
        class ColorFormatter(logging.Formatter):
            COLORS = {
                logging.DEBUG: Fore.CYAN,
                logging.INFO: Fore.GREEN,
                logging.WARNING: Fore.YELLOW,
                logging.ERROR: Fore.RED,
                logging.CRITICAL: Fore.MAGENTA
            }

            def format(self, record):
                color = self.COLORS.get(record.levelno, "")
                record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
                return super().format(record)

        return ColorFormatter('%(asctime)s - %(levelname)s - %(message)s')

    def log(self, level: str, message: str, rabbitmq_message: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        log_func = getattr(self.logger, level.lower(), self.logger.info)
        log_func(message)

        if self.rabbitmq_config and self.routing_key and self.exchange:
            # self.logger.info(f"Sending log to RabbitMQ: {level} - {message}")
            try:
                send_topic_message(
                    message=rabbitmq_message or message,
                    routing_key=f"logs.{level.lower()}.{self.logger.name}",
                    exchange=self.exchange,
                    config=self.rabbitmq_config,
                    headers={**self.headers, **(headers or {})}
                )
            except Exception as e:
                self.logger.error(f"Failed to send log to RabbitMQ: {e}")
