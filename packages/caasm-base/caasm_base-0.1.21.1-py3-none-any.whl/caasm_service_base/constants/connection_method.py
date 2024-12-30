from caasm_tool.constants import StrEnum


class ConnectionType(StrEnum):
    Es = "es"
    Kafka = "kafka"
    Mongodb = "mongodb"
    Http = "http"
