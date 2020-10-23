from DockerBuildSystem import DockerComposeTools, YamlTools, TerminalTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

TEST_KEY = 'test'


def GetInfoMsg():
    infoMsg = "Test selections is configured by adding a 'test' property to the .yaml file.\r\n"
    infoMsg += "The 'test' property is a dictionary of test selections.\r\n"
    infoMsg += "Add '-test' to the arguments to run all test selections in sequence, \r\n"
    infoMsg += "or add specific selection names to test those only.\r\n"
    infoMsg += "Example: 'dbm -test myTestSelection'.\r\n"
    return infoMsg


def GetTestSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    testProperty = YamlTools.GetProperties(TEST_KEY, yamlData)
    if BuildTools.SELECTIONS_KEY in testProperty:
        return testProperty[BuildTools.SELECTIONS_KEY]
    return {}


def TestSelections(selectionsToTest, testSelections):
    if len(selectionsToTest) == 0:
        for testSelection in testSelections:
            TestSelection(testSelections[testSelection], testSelection)
    else:
        for selectionToTest in selectionsToTest:
            if selectionToTest in testSelections:
                TestSelection(testSelections[selectionToTest], selectionToTest)


def TestSelection(testSelection, selectionToTest):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(testSelection)
    BuildTools.HandleTerminalCommandsSelection(testSelection)
    TerminalTools.LoadDefaultEnvironmentVariablesFile()

    if BuildTools.FILES_KEY in testSelection:
        testComposeFile = BuildTools.GetAvailableComposeFilename('test', selectionToTest)
        composeFiles = testSelection[BuildTools.FILES_KEY]
        containerNames = BuildTools.MergeAndPopulateWithContainerNames(composeFiles, testComposeFile)
        if BuildTools.CONTAINER_NAMES_KEY in testSelection:
            containerNames = testSelection[BuildTools.CONTAINER_NAMES_KEY]

        try:
            DockerComposeTools.ExecuteComposeTests([testComposeFile],
                                                   testContainerNames=containerNames,
                                                   removeTestContainers=False,
                                                   buildCompose=True,
                                                   downCompose=False)
        except:
            BuildTools.RemoveComposeFileIfNotPreserved(testComposeFile, testSelection)
            raise

        BuildTools.HandleCopyFromContainer(testSelection)
        DockerComposeTools.DockerComposeDown([testComposeFile])
        if YamlTools.TryGetFromDictionary(testSelection, BuildTools.REMOVE_CONTAINERS_KEY, False):
            DockerComposeTools.DockerComposeRemove([testComposeFile])

        BuildTools.RemoveComposeFileIfNotPreserved(testComposeFile, testSelection)

    os.chdir(cwd)


def HandleTestSelections(arguments):
    if len(arguments) == 0:
        return
    if not('-test' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    selectionsToTest = SwarmTools.GetArgumentValues(arguments, '-test')
    selectionsToTest += SwarmTools.GetArgumentValues(arguments, '-t')

    testSelections = GetTestSelections(arguments)
    TestSelections(selectionsToTest, testSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleTestSelections(arguments)
