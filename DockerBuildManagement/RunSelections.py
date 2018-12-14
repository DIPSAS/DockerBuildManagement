from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

RUN_KEY = 'run'
ABORT_ON_CONTAINER_EXIT_KEY = 'abortOnContainerExit'
DETACHED_KEY = 'detached'

def GetInfoMsg():
    infoMsg = "Run selections is configured by adding a 'run' property to the .yaml file.\r\n"
    infoMsg += "The 'run' property is a dictionary of run selections.\r\n"
    return infoMsg


def GetRunSelections(arguments):
    runProperty = BuildTools.GetProperties(arguments, RUN_KEY, GetInfoMsg())
    if BuildTools.SELECTIONS_KEY in runProperty:
        return runProperty[BuildTools.SELECTIONS_KEY]
    return {}


def RunSelections(selectionsToRun, runSelections):
    if len(selectionsToRun) == 0:
        for runSelection in runSelections:
            RunSelection(runSelections[runSelection])
    else:
        for selectionToRun in selectionsToRun:
            if selectionToRun in runSelections:
                RunSelection(runSelections[selectionToRun])


def RunSelection(runSelection):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(runSelection)
    DockerComposeTools.DockerComposeUp(
        runSelection[BuildTools.FILES_KEY],
        BuildTools.TryGetFromDictionary(runSelection, ABORT_ON_CONTAINER_EXIT_KEY, True), 
        BuildTools.TryGetFromDictionary(runSelection, DETACHED_KEY, False))
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
