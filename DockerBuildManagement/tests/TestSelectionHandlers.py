import unittest
import os
from . import TestTools
from .. import BuildTools
from .. import ChangelogSelections
from .. import TestSelections
from .. import BuildSelections
from .. import RunSelections
from .. import SwarmSelections

class TestSelectionHandlers(unittest.TestCase):

    def test_a_changelog(self):
        print('EXECUTING CHANGELOG TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = []
        ChangelogSelections.HandleChangelogSelections(arguments)
        self.assertEqual(os.environ['VERSION'], '1.0.0')
        os.chdir(cwd)
        print('DONE EXECUTING CHANGELOG TEST')

    def test_b_test(self):
        print('EXECUTING TEST SELECTION TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-test']
        TestSelections.HandleTestSelections(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING TEST SELECTION TEST')

    def test_c_build(self):
        print('EXECUTING BUILD SELECTION TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-build']
        BuildSelections.HandleBuildSelections(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING BUILD SELECTION TEST')

    def test_d_run(self):
        print('EXECUTING RUN SELECTION TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-run']
        RunSelections.HandleRunSelections(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING RUN SELECTION TEST')

    def test_e_swarm(self):
        print('EXECUTING SWARM SELECTION TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-start']
        SwarmSelections.HandleSwarmSelections(arguments)
        arguments = ['-stop']
        SwarmSelections.HandleSwarmSelections(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING SWARM SELECTION TEST')

if __name__ == '__main__':
    unittest.main()