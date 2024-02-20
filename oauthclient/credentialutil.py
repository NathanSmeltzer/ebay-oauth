import yaml, json
import logging

from . import logger
from .model.model import Environment, Credentials
from decouple import config

logging.getLogger(config("LOGGER_NAME", default="ebay")).setLevel(config("LOG_LEVEL", default="INFO"))

user_config_ids = ["sandbox-user", "production-user"]

class CredentialUtil(object):
    """
    credential_list: dictionary key=string, value=credentials
    """
    _credential_list = {}
    
     
    @classmethod
    def load(cls, app_config_path):
        logger.info("Loading credential configuration file at: %s", app_config_path)
        with open(app_config_path, 'r') as f:
            if app_config_path.endswith('.yaml') or app_config_path.endswith('.yml'):
                content = yaml.load(f)
            elif app_config_path.endswith('.json'):
                content = json.loads(f.read())
            else:
                raise ValueError('Configuration file need to be in JSON or YAML')
            CredentialUtil._iterate(content)

    @classmethod
    def _iterate(cls, content):
        for key in content:
            logging.debug("Environment attempted: %s", key)
            
            if key in [Environment.PRODUCTION.config_id, Environment.SANDBOX.config_id]:
                client_id = content[key]['appid']
                dev_id = content[key]['devid']
                client_secret = content[key]['certid']
                ru_name = content[key]['redirecturi']

                app_info = Credentials(client_id, client_secret, dev_id, ru_name)
                cls._credential_list.update({key: app_info})

            

    @classmethod
    def get_credentials(cls, env_type):
        """
        env_config_id: environment.PRODUCTION.config_id or environment.SANDBOX.config_id
        """
        logger.debug(f"env_type in get_credentials: {env_type}")
        logger.debug(f"env_type __dict__: {env_type.__dict__}")
        if len(cls._credential_list) == 0:
            msg = "No environment loaded from configuration file"
            logging.error(msg)
            raise CredentialNotLoadedError(msg)
        return cls._credential_list[env_type.config_id]
    
class CredentialNotLoadedError(Exception):
    pass