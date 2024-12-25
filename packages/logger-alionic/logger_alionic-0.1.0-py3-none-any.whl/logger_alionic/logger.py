from loguru._logger import Logger, Core
import socket
import json
from dotenv import load_dotenv
import os
import sys


class LogstashLogger(Logger):
    def __init__(self, class_name):
        """
        initial parameters: load_dotenv()
        cred_env:
            LOGSTASH_HOST: <logstash_host> (bash: export LOGSTASH_HOST)
            LOGSTASH_PORT: <logstash_port> (bash: export LOGSTASH_PORT)
        """
        self.class_name = class_name
        super().__init__(
            core=Core(),
            exception=None,
            depth=0,
            record=False,
            lazy=False,
            colors=False,
            raw=False,
            capture=True,
            patchers=[],
            extra={},
        )
        self.logger_init()

    def logger_init(self):
        self.remove()
        self.add(self.logstash_sink, format="{message}")

    def load_env(self):
        load_dotenv()
        self.name_space = []
        try:
            for namespace in ("LOGSTASH_HOST", "LOGSTASH_PORT"):
                if os.getenv(namespace) is None:
                    with open(".env", "a") as f:
                        f.write(f"{namespace}=\n")
                    raise Exception(f"Environment variable {namespace} not set")
                if namespace == "LOGSTASH_PORT":
                    self.name_space.append(int(os.getenv(namespace)))
                else:
                    self.name_space.append(os.getenv(namespace))
        except Exception as e:
            sys.exit(f"Failed to load environment variables: {e}")

    def logstash_sink(self, message):
        try:
            log_data = json.dumps(
                {
                    "message": message.record["message"],
                    "level": message.record["level"].name,
                    "time": message.record["time"].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "class": self.class_name,
                    "function": message.record["function"],
                }
            )
            self.load_env()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(tuple(self.name_space))
                sock.sendall((log_data + "\n").encode("utf-8"))
        except Exception as e:
            print(f"Failed to send log to Logstash: {e}")