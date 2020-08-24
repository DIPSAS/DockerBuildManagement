from DockerBuildSystem import DockerComposeTools, DockerImageTools, YamlTools, TerminalTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

RUN_KEY = 'run'
ABORT_ON_CONTAINER_EXIT_KEY = 'abortOnContainerExit'
DETACHED_KEY = 'detached'
VERIFY_CONTAINER_EXIT_CODE = 'verifyContainerExitCode'

def GetInfoMsg():
    infoMsg = "Run selections is configured by adding a 'run' property to the .yaml file.\r\n"
    infoMsg += "The 'run' property is a dictionary of run selections.\r\n"
    infoMsg += "Add '-run' to the arguments to run all runnable selections in sequence, \r\n"
    infoMsg += "or add specific selection names to run those only.\r\n"
    infoMsg += "Example: 'dbm -run myRunnableSelection'.\r\n"
    return infoMsg


def GetRunSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    runProperty = YamlTools.GetProperties(RUN_KEY, yamlData)
    if BuildTools.SELECTIONS_KEY in runProperty:
        return runProperty[BuildTools.SELECTIONS_KEY]
    return {}


def RunSelections(selectionsToRun, runSelections):
    if len(selectionsToRun) == 0:
        for runSelection in runSelections:
            RunSelection(runSelections[runSelection], runSelection)
    else:
        for selectionToRun in selectionsToRun:
            if selectionToRun in runSelections:
                RunSelection(runSelections[selectionToRun], selectionToRun)


def RunSelection(runSelection, selectionToRun):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(runSelection)
    BuildTools.HandleTerminalCommandsSelection(runSelection)
    TerminalTools.LoadDefaultEnvironmentVariablesFile()

    if BuildTools.FILES_KEY in runSelection:
        runComposeFile = BuildTools.GetAvailableComposeFilename('run', selectionToRun)
        composeFiles = runSelection[BuildTools.FILES_KEY]
        if YamlTools.TryGetFromDictionary(runSelection, VERIFY_CONTAINER_EXIT_CODE, False):
            containerNames = BuildTools.MergeAndPopulateWithContainerNames(composeFiles, runComposeFile)
            if BuildTools.CONTAINER_NAMES_KEY in runSelection:
                containerNames = runSelection[BuildTools.CONTAINER_NAMES_KEY]
        else:
            containerNames = []
            DockerComposeTools.MergeComposeFiles(composeFiles, runComposeFile)

        try:
            DockerComposeTools.DockerComposeUp(
                [runComposeFile],
                YamlTools.TryGetFromDictionary(runSelection, ABORT_ON_CONTAINER_EXIT_KEY, True),
                YamlTools.TryGetFromDictionary(runSelection, DETACHED_KEY, False))
        except:
            BuildTools.RemoveComposeFileIfNotPreserved(runComposeFile, runSelection)
            raise

        DockerImageTools.VerifyContainerExitCode(containerNames, assertExitCodes=True)
        BuildTools.HandleCopyFromContainer(runSelection)

        if YamlTools.TryGetFromDictionary(runSelection, BuildTools.REMOVE_CONTAINERS_KEY, False):
            DockerComposeTools.DockerComposeRemove([runComposeFile])

        BuildTools.RemoveComposeFileIfNotPreserved(runComposeFile, runSelection)
    
    os.chdir(cwd)


def HandleRunSelections(arguments):
    if len(arguments) == 0:
        return
    if not('-run' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    selectionsToRun = SwarmTools.GetArgumentValues(arguments, '-run')
    selectionsToRun += SwarmTools.GetArgumentValues(arguments, '-r')

    runSelections = GetRunSelections(arguments)
    RunSelections(selectionsToRun, runSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleRunSelections(arguments)
