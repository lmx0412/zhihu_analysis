import yaml
import logging
import logger

log = logging.getLogger()

class DbConfig():
    db_config = None
    try:
        yamlreader = open('config.yaml')
        config_s = yaml.load(yamlreader, Loader=yaml.FullLoader)
        db_config = config_s["db-config"]
    except Exception as e:
        log.exception(e)

    log.debug(db_config)

config = {
    'db_config': DbConfig,
}
