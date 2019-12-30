import unittest
import os
from tests import TestTools
from DockerBuildManagement import BuildManager

class TestBuildManager(unittest.TestCase):

    def test_a_GetPositionalActionArguments_NoSwarmArguments(self):
        arguments = ['-start', 'selection1', '-run', '-build', 'selection2']
        i = 0
        while i < len(arguments):
            actionArgs, newIndex = BuildManager.GetPositionalActionArguments(arguments, i)
            if i == 0:
                self.assertTrue('-start' in actionArgs and 'selection1' in actionArgs)
                self.assertFalse('-build' in actionArgs or 'selection2' in actionArgs)
            if i == 1:
                self.assertTrue(len(actionArgs) == 0)
            if i == 2:
                self.assertTrue('-run' in actionArgs and 'selection2' in actionArgs)
                self.assertFalse('-build' in actionArgs or '-start' in actionArgs or 'selection1' in actionArgs)
            if i == 3:
                self.assertTrue('-build' in actionArgs and 'selection2' in actionArgs)
                self.assertFalse('-start' in actionArgs or 'selection1' in actionArgs)
            if i == 4:
                self.assertTrue(len(actionArgs) == 0)
            i = newIndex


    def test_b_GetPositionalActionArguments_SwarmArguments(self):
        arguments = ['-swarm', '-start', 'selection1', '-build', 'selection2', '-swarm', '-stop', 'selection3', '-swarm']
        i = 0
        while i < len(arguments):
            actionArgs, newIndex = BuildManager.GetPositionalActionArguments(arguments, i)
            if i == 0:
                self.assertTrue(len(actionArgs) == 3)
                self.assertTrue('-swarm' in actionArgs and '-start' in actionArgs and 'selection1' in actionArgs)
                self.assertFalse('-stop' in actionArgs or '-build' in actionArgs or 'selection2' in actionArgs or 'selection3' in actionArgs)
            if i == 1:
                raise Exception('Should not end up here.')
            if i == 2:
                self.assertTrue(len(actionArgs) == 0)
            if i == 3:
                self.assertTrue('-build' in actionArgs and 'selection2' in actionArgs)
                self.assertFalse('-start' in actionArgs or 'selection1' in actionArgs or 'selection3' in actionArgs)
            if i == 4:
                self.assertTrue(len(actionArgs) == 0)
            if i == 5:
                self.assertTrue('-swarm' in actionArgs and '-stop' in actionArgs and 'selection3' in actionArgs)
                self.assertFalse('-start' in actionArgs or '-build' in actionArgs or 'selection2' in actionArgs)
            if i == 6:
                raise Exception('Should not end up here.')
            if i == 7:
                self.assertTrue(len(actionArgs) == 0)
            if i == 8:
                self.assertTrue('-swarm' in actionArgs and len(actionArgs) == 1)
            i = newIndex

    def test_c_start_test_build_run_stop(self):
        print('EXECUTING ALL SELECTIONS TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-swarm', '-start', '-test', '-build', '-run', '-stop']
        BuildManager.HandleManagement(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING ALL SELECTIONS TEST')

if __name__ == '__main__':
    unittest.main()