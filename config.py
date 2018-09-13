from flask_env import MetaFlaskEnv


class Configuration(object):
    __metaclass__ = MetaFlaskEnv

    DEBUG = False
    PORT = 5000
    JSONIFY_PRETTYPRINT_REGULAR = False
    KUBERNETES_DASHBOARD_URL = None
