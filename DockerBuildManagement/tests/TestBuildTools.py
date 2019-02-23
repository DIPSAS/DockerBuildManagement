import unittest
import os
from .. import BuildTools

class TestBuildTools(unittest.TestCase):

    def test_getInforMsg_success(self):
        self.assertIsNotNone(BuildTools.GetInfoMsg())

    def test_TryChangeToDirectoryAndGetCwd_success(self):
        directory = 'DockerBuildManagement'
        selection = {BuildTools.DIRECTORY_KEY: directory}
        oldCwd = BuildTools.TryChangeToDirectoryAndGetCwd(selection)
        cwd = os.getcwd()
        self.assertEqual(cwd, os.path.join(oldCwd, directory))
        os.chdir(oldCwd)

    def test_TryGetFromDictionary_success(self):
        selection = {'validKey': 'value'}
        value = BuildTools.TryGetFromDictionary(selection, 'validKey', 'defaultValue')
        self.assertEqual(value, 'value')
        value = BuildTools.TryGetFromDictionary(selection, 'invalidKey', 'defaultValue')
        self.assertEqual(value, 'defaultValue')


if __name__ == '__main__':
    unittest.main()