import os
import logging
import graypy
import json
import traceback

class GraylogFilter(logging.Filter):
    def filter(self, record):
        # Aqui você pode adicionar lógica para filtrar logs, se necessário
        return True

    @staticmethod
    def handle_error(arg):
        error_message = str(arg)
        backtrace = ''.join(traceback.format_exception(type(arg), arg, arg.__traceback__))
        return error_message, backtrace

class GraylogTelemidia:
    _instance = None

    def __new__(cls, graylog_config=None):
        if cls._instance is None:
            cls._instance = super(GraylogTelemidia, cls).__new__(cls)
            cls._instance.initialize_logger(graylog_config or cls.get_default_config())
        return cls._instance

    @staticmethod
    def get_default_config():
        return {
            'server': os.getenv('GRAYLOG_SERVER'),
            'inputPort': os.getenv('GRAYLOG_INPUT_PORT'),
            'appName': os.getenv('GRAYLOG_APP_NAME'),
            'environment': os.getenv('GRAYLOG_ENVIRONMENT')
        }

    def initialize_logger(self, graylog_config):
        self.logger = logging.getLogger('graylog')
        self.logger.setLevel(logging.DEBUG)

        handler = graypy.GELFUDPHandler(graylog_config['server'], graylog_config['inputPort'])
        handler.addFilter(GraylogFilter())
        self.logger.addHandler(handler)

        self.app_name = graylog_config['appName']
        self.environment = graylog_config['environment']

        # Armazenar erros e stack traces
        self.error_messages = []
        self.back_traces = []

    def __getattr__(self, name):
        # Redireciona chamadas para métodos do logger
        if hasattr(self.logger, name):
            return lambda *args: self.log(name, *args)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def log(self, level, *args):
        payload = self.prepare_payload(args)
        message = self.extract_message(args)

        if hasattr(self.logger, level):
            getattr(self.logger, level)(message, extra=payload)
        else:
            raise ValueError(f"Method '{level}' does not exist.")

    def extract_message(self, args):
        return str(args[0]) if args else "No message provided"

    def prepare_payload(self, args):
        arguments = []

        for i, arg in enumerate(args):
            if i == 0 and not isinstance(arg, (Exception,)):
                continue  # Ignora o primeiro parâmetro se não for uma mensagem de log

            if isinstance(arg, Exception):
                error_message, backtrace = GraylogFilter.handle_error(arg)
                self.error_messages.append(error_message)
                self.back_traces.append(backtrace)
                continue

            if isinstance(arg, dict):
                arguments.append(arg)
            else:
                arguments.append(str(arg))

        return self.build_payload(arguments)

    def build_payload(self, arguments):
        payload = {
            'app_language': 'Python',
            'facility': self.app_name,
            'environment': self.environment
        }

        if self.error_messages:
            payload['error_message'] = self.format_error_messages(self.error_messages)
        if self.back_traces:
            payload['error_stack'] = self.format_back_traces(self.back_traces, self.error_messages)
        if arguments:
            payload['extra_info'] = json.dumps(arguments, indent=4)

        return payload

    def format_error_messages(self, error_messages):
        return ' | '.join(f"[Erro #{i + 1}]: {msg}" for i, msg in enumerate(error_messages))

    def format_back_traces(self, back_traces, error_messages):
        return ''.join(
            f"[Traceback do erro #{i + 1} '{error_messages[i]}']:\n{bt}\n"
            for i, bt in enumerate(back_traces)
        )