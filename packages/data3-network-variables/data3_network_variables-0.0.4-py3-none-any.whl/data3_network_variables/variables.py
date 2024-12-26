
import os
import redis
from dotenv import load_dotenv
load_dotenv()

class Data3Utils:
    '''
    Class to fetch environment variables for the user tools file
    Methods:
    fetch_env_variables: Fetch Single or all ("") tool env values from Redis
    '''
    def __init__(self):
        self.REDIS_HOST = os.getenv("REDIS_HOST")
        self.redis_client = redis.from_url(self.REDIS_HOST)

    def fetch_env_variables(self, field_name: str):
        """Fetch a value from Redis and handle errors."""
        try:
            if field_name == "":
                # fetch all fields
                all_envs = self.redis_client.hgetall("tools_env")
                return {k.decode('utf-8'): v.decode('utf-8') for k, v in all_envs.items()}
            
            value = self.redis_client.hget("tools_env", field_name)
            if value == None:
                return ValueError(f"Field {field_name} not found in tools environment")
            return value.decode('utf-8')
        except Exception as e:
            return f"Error: {e}"
        
    def fetch_port(self, agent_address: str):
        """Fetch a value from Redis and handle errors."""
        try:
            if agent_address:
                value = self.redis_client.hget("docker-compose-mappings", agent_address)
                if value == None:
                    return ValueError(f"Field {agent_address} not found in docker mappings")
                return value.decode('utf-8')
        except Exception as e:
            return f"Error: {e}"  