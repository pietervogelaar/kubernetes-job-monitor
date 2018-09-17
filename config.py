import os


class Configuration(object):

    if 'KUBERNETES_DASHBOARD_URL' in os.environ:
        KUBERNETES_DASHBOARD_URL = os.environ['KUBERNETES_DASHBOARD_URL']
    else:
        KUBERNETES_DASHBOARD_URL = None
