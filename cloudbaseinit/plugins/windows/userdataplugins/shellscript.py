# Copyright 2013 Mirantis Inc.
# Copyright 2014 Cloudbase Solutions Srl
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import tempfile
import os

from cloudbaseinit.openstack.common import log as logging
from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins.windows.userdataplugins import base
from cloudbaseinit.plugins.windows import userdatautils

LOG = logging.getLogger(__name__)


class ShellScriptPlugin(base.BaseUserDataPlugin):
    def __init__(self):
        super(ShellScriptPlugin, self).__init__("text/x-shellscript")

    def process(self, part):
        osutils = osutils_factory.get_os_utils()

        file_name = part.get_filename()
        target_path = os.path.join(tempfile.gettempdir(), file_name)

        shell = False
        powershell = False

        if file_name.endswith(".cmd"):
            args = [target_path]
            shell = True
        if file_name.endswith(".cmf"):
            return userdatautils.execute_user_data_script(part.get_payload())
        elif file_name.endswith(".sh"):
            args = ['bash.exe', target_path]
        elif file_name.endswith(".py"):
            args = ['python.exe', target_path]
        elif file_name.endswith(".ps1"):
            powershell = True
        else:
            # Unsupported
            LOG.warning('Unsupported script type')
            return 0

        try:
            with open(target_path, 'wb') as f:
                f.write(part.get_payload())

            if powershell:
                (out, err,
                 ret_val) = osutils.execute_powershell_script(target_path)
            else:
                (out, err, ret_val) = osutils.execute_process(args, shell)

            LOG.info('User_data script ended with return code: %d' % ret_val)
            LOG.debug('User_data stdout:\n%s' % out)
            LOG.debug('User_data stderr:\n%s' % err)

            return ret_val
        except Exception, ex:
            LOG.warning('An error occurred during user_data execution: \'%s\''
                        % ex)
        finally:
            if os.path.exists(target_path):
                os.remove(target_path)
