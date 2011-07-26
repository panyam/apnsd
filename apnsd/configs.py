
import os, logging
from twisted.application import internet
import errors

def read_listeners_in_config(config_file, apns_daemon, service_parent):
    """
    Reads the config file and return all the listeners in it one by one.
    """
    if not os.path.isfile(config_file):
        raise errors.ConfigFileError(config_file, "File not found: %s" % config_file)

    configs = eval(open(config_file).read())
    if 'listeners' not in configs:
        raise errors.ConfigFileError(config_file, "'listeners' section not found")

    listeners = configs['listeners']
    for listener_name in listeners:
        listener_data     = listeners[listener_name]
        listener_class    = listener_data['class']
        parts = listener_class.split(".")
        if len(parts) > 1:
            listener_pkg      = ".".join(parts[:-1])
            listener_module   = __import__(listener_pkg, {}, {}, [''])
            listener_class    = getattr(listener_module, parts[-1])
        else:
            listener_class    = eval(parts[-1])

        logging.debug("Creating listener: " + str(listener_class))

        listener = listener_class(apns_daemon, **listener_data)
        if listener_data.get("secure", False):
            server = internet.SSLServer(listener_data["port"], listener)
        else:
            server = internet.TCPServer(listener_data["port"], listener)
        server.setServiceParent(service_parent)

        logging.debug("Listener Created: " + str(listener))
        apns_daemon.registerListener(listener_name, listener)

def read_apps_in_config(config_file, apns_daemon):
    """
    Reads the config file and loads config data about all the apps we want
    to support.
    """
    """
    Reads the config file and return all the listeners in it one by one.
    """
    if not os.path.isfile(config_file):
        raise errors.ConfigFileError(config_file, "File not found")

    configs = eval(open(config_file).read())
    if 'apps' not in configs:
        raise errors.ConfigFileError(config_file, "'apps' section not found")
        
    apps = configs['apps']
    for app_key in apps:
        app             = apps[app_key]
        app_id          = app['app_id']
        dev_cert_file   = app.get('dev_certificate_file', None)
        dev_pkey_file   = app.get("dev_privatekey_file", None)
        rel_cert_file   = app.get('rel_certificate_file', None)
        rel_pkey_file   = app.get("rel_privatekey_file", None)
        if dev_cert_file and dev_pkey_file:
            logging.warning("Dev certificate and private key files not found...")
        else:
            apns_daemon.registerApp("dev:" + app_id, dev_cert_file, dev_pkey_file)
        if rel_cert_file and rel_pkey_file:
            logging.warning("Release certificate and private key files not found...")
        else:
            apns_daemon.registerApp("rel:" + app_id, rel_cert_file, rel_pkey_file)

