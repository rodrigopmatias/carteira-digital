import os
import json
import logging

os.environ.setdefault('APP_CONFIG', 'app.conf.json')
os.environ.setdefault('APP_ENV', 'development')

log = logging.getLogger(__name__)

class __Config:
    __config_map = None

    def _load_file_configuration(self):
        config_file = os.environ.get('APP_CONFIG')
        config_env = os.environ.get('APP_ENV')

        try:
            with open(config_file, 'rt') as fd:
                complete = json.load(fd)
                common = complete.get('common', {})
                selected = complete.get(config_env, {})

                self.__config_map = {
                    **common,
                    **selected
                }
        except json.JSONDecodeError as e:
            log.error(f'Error loading configuration from file "{config_file}"')
            log.error(e)
        except FileNotFoundError as e:
            log.info(f"can't load file {config_file}, its not exist")
        finally:
            if not self.__config_map:
                self.__config_map = {}

    def __init__(self):
        if not self.__config_map:
            self._load_file_configuration()
        else:
            log.debug('configuration already load')

    def value(self, key, default_value=None, cast=lambda x: x):
        if key not in self.__config_map:
            log.warn(f'key {key} configuration not found')

        return cast(self.__config_map.get(key, default_value))


def config(key, default_value=None, cast=lambda x: x):
    __config = __Config()

    return __config.value(key, default_value, cast)
