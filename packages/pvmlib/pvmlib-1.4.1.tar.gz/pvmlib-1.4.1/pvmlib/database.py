import motor.motor_asyncio
from pvmlib.logger import LoggerSingleton
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError

logger = LoggerSingleton().get_logger()

class DatabaseManager:
    def __init__(self):
        self.mongo_database = None
        self.mongo_client = None

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def connect_to_mongo(self, settings_env):
        try:
            self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings_env.url_db)
            self.mongo_database = self.mongo_client[settings_env.nm_db]
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def disconnect_from_mongo(self):
        self.mongo_client.close()    

database_manager = DatabaseManager()