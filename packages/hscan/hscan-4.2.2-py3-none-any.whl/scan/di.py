from dependency_injector import containers, providers
from scan.database import MongoDB, Redis, RabbitMQ

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    mongodb = providers.Singleton(
        MongoDB,
        host=config.mongo.host,
        port=config.mongo.port
    )
    
    redis = providers.Singleton(
        Redis,
        host=config.redis.host,
        port=config.redis.port
    )
