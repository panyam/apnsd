#!/bin/env python2.5
###############################################################################
#
# Copyright 2009, Sri Panyam
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

import constants, errors, daemon

def read_config_file(apns_daemon, config_file):
    """
    Reads the config file and loads config data about all the apps we want
    to support.
    """
    import os
    if not os.path.isfile(config_file):
        raise errors.ConfigFileError(config_file, "File not found")

    configs = eval(open(config_file).read())
    if 'listeners' not in configs:
        raise errors.ConfigFileError(config_file, "'listeners' section not found")

    if 'apps' not in configs:
        raise errors.ConfigFileError(config_file, "'apps' section not found")

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

        print "Creating listener: ", listener_class
        listener = listener_class(apns_daemon, **listener_data)
        print "Listener Created: ", listener
        print "----------------------"
        
    apps = configs['apps']
    for app_key in apps:
        app         = apps[app_key]
        app_id      = app['app_id']
        cert_file   = app['certificate_file']
        pkey_file   = app.get("privatekey_file", None)
        apns_daemon.registerApp(app_id, cert_file, pkey_file)


def parse_options(apns_daemon):
    from optparse import OptionParser

    parser = OptionParser(version = "%prog 0.1")
    parser.add_option("-c", "--config", dest = "configfile",
                      help="Config file to read application info from.", metavar = "CONFIG-FILE")

    (options, args) = parser.parse_args()

    if not options.configfile:
        parser.error("Please specify a valid config filename with the -c option")
        
    read_config_file(apns_daemon, options.configfile)

def main():
    from twisted.internet import reactor
    apns_daemon = daemon.APNSDaemon(reactor)
    parse_options(apns_daemon)
    apns_daemon.run()

if __name__ == "__main__":
    main()

