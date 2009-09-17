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
            'interface': "localhost",  #default
            'port': 90
        },
        'http': {
            'class': 'listeners.http.site.APNSSite',
            'interface': "localhost",  #default
            'secure': False,
            'port': 99
        },
    },

    'apps': {
        'app1': {
            'app_id':           "apnstest",
            'certificate_file': "../../../certs/apnstest/Certificates.pem",
            'privatekey_file':  "../../../certs/apnstest/PrivateKey.unenc.pem",
        },
    }
}
