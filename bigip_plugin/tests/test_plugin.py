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

from cloudify.workflows import local

""" Testcase for the BigIP plugin. """

class TestPlugin(unittest.TestCase):

    def setUp(self):
        # build blueprint path
        blueprint_path = os.path.join(os.path.dirname(__file__),
                                      'blueprint', 'blueprint.yaml')

        # inject input from test
        inputs = {
            'host':         '54.174.182.15',
            'username':     'admin',
            'password':     'password',
        }

        # setup local workflow execution environment
        self.env = local.init_env(blueprint_path,
                                  name=self._testMethodName,
                                  inputs=inputs)

    def test_pool_create_delete(self):

        self.env.execute('install', task_retries=0)
        self.env.execute('uninstall', task_retries=0)
