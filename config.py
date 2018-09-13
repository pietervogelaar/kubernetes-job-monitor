from flask_env import MetaFlaskEnv


class Configuration(object):
    __metaclass__ = MetaFlaskEnv

    DEBUG = False
    PORT = 5000
    JSONIFY_PRETTYPRINT_REGULAR = False
    STACKSTORM_URL = None
    STACKSTORM_API_KEY = None
    STACKSTORM_API_URL = None
