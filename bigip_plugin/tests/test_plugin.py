########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


import os
import unittest

from bigip_plugin.bip_proxy import BigIpProxy
from bigip_plugin.external import bigsuds

from cloudify.workflows import local

""" Testcase for the BigIP plugin. """


class TestPlugin(unittest.TestCase):

    def setUp(self):
        # build blueprint path
        blueprint_path = os.path.join(os.path.dirname(__file__),
                                      'blueprint',
                                      'blueprint.yaml')

        # inject input from test
        self.inputs = {
            'host':             'cfy-bigip',
            'username':         'admin',
            'password':         'password',
            'pool_id':          'test',
            'port':             '80'
        }

        IGNORED_LOCAL_WORKFLOW_MODULES = (
            'worker_installer.tasks',
            'plugin_installer.tasks'
        )

        # setup local workflow execution environment
        self.env = local.init_env(blueprint_path,
                                  name=self._testMethodName,
                                  inputs=self.inputs,
                                  ignored_modules=IGNORED_LOCAL_WORKFLOW_MODULES)

    def test_pool_create_delete(self):

        # Ensure we don't have the test pool defined; otherwise
        # we can't run the test.

        bigip = bigsuds.BIGIP(hostname=self.inputs['host'],
                              username=self.inputs['username'],
                              password=self.inputs['password'])

        existing_pools = bigip.LocalLB.Pool.get_list()
        pool_id = self.inputs['pool_id']
        pool_name = BigIpProxy.get_pool_name(pool_id)

        if pool_name in existing_pools:
            self.fail('Test pool already exists: {0}'.format(pool_id))

        self.env.execute('install', task_retries=0)
        self.env.execute('uninstall', task_retries=0)
