import redis
import json
import redis
from config.load_env import Config

class RedisService:
    
    def __init__(self, host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB):
        self.redis_connection = redis.StrictRedis(
            host=host, port=port, db=db, decode_responses=True
        )

    def fetch_data(self, redis_key):
        try:
            data_string = self.redis_connection.get(redis_key)
            if not data_string:
                return None, "No data found for the provided key"
            return json.loads(data_string), None
        except json.JSONDecodeError:
            return None, "Error decoding data from Redis"
        except Exception as e:
            return None, f"Unexpected error: {e}"

    def save_data(self, redis_key, data):
        try:
            self.redis_connection.set(redis_key, json.dumps(data))
            print(f"Data successfully saved to Redis under the key '{redis_key}'.")
        except Exception as e:
            print(f"Error saving data to Redis: {e}")

    def delete_data(self, redis_key):
        try:
            self.redis_connection.delete(redis_key)
            print(f"Data with key '{redis_key}' deleted from Redis.")
        except Exception as e:
            print(f"Error deleting data from Redis: {e}")
