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

{
    'listeners': {
        'line': {
            'class': 'listeners.line.LineProtocolFactory',
            'interface': "localhost",  #default: all interface
            'port': 9999,
        },
        'http': {
            'class': 'listeners.http.site.APNSSite',
            'interface': "localhost",  #default: all interface
            'secure': False,
            'port': 99,

            # where is the tyrant server running?
            # why do we need a tyrant server?  the http interface allows
            # one to register users and apps dynamically at runtime
            'tyrant_host': "localhost",     #   default - localhost
            'tyrant_port': 1978,            #   default - 1978
            'cert_folder': "/tmp/apnsd.certificates",
        },
    },

    'apps': {
        'app1': {
            'app_id':           "App1 ID",
            'certificate_file': "path_to_certificate_file_1.pem",
            'privatekey_file':  "path_to_privatekey_file_1.pem"
        },
        'app2': {
            'app_id':           "App2 ID",
            'certificate_file': "path_to_certificate_file_2.pem",
            'privatekey_file':  "path_to_privatekey_file_2.pem"
        },
    }
}

