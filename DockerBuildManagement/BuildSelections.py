from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

BUILD_KEY = 'build'


def GetInfoMsg():
    infoMsg = "Build selections is configured by adding a 'build' property to the .yaml file.\r\n"
    infoMsg += "The 'build' property is a dictionary of build selections.\r\n"
    infoMsg += "Add '-build' to the arguments to build all selections in sequence, or add spesific selection names to build those only.\r\n"
    infoMsg += "Example: 'dbm -build myBuildSelection'.\r\n"
    return infoMsg


def GetBuildSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, [BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILE])
    buildProperty = SwarmTools.GetProperties(arguments, BUILD_KEY, GetInfoMsg(), yamlData)
    if BuildTools.SELECTIONS_KEY in buildProperty:
        return buildProperty[BuildTools.SELECTIONS_KEY]
    return {}


def BuildSelections(selectionsToBuild, buildSelections):
    if len(selectionsToBuild) == 0:
        for buildSelection in buildSelections:
            BuildSelection(buildSelections[buildSelection], buildSelection)
    else:
        for selectionToBuild in selectionsToBuild:
            if selectionToBuild in buildSelections:
                BuildSelection(buildSelections[selectionToBuild], selectionToBuild)


def BuildSelection(buildSelection, selectionToBuild):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(buildSelection)
    BuildTools.HandleTerminalCommandsSelection(buildSelection)

    if BuildTools.FILES_KEY in buildSelection:
        composeFiles = buildSelection[BuildTools.FILES_KEY]
        buildComposeFile = 'docker-compose.build.' + selectionToBuild + '.yml'
        DockerComposeTools.MergeComposeFiles(composeFiles, buildComposeFile)
        DockerComposeTools.DockerComposeBuild([buildComposeFile])
        if BuildTools.ADDITIONAL_TAG_KEY in buildSelection:
            DockerComposeTools.TagImages(buildComposeFile, buildSelection[BuildTools.ADDITIONAL_TAG_KEY])
            
    os.chdir(cwd)


def HandleBuildSelections(arguments):
    if len(arguments) == 0:
        return
    if not('-build' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    selectionsToBuild = SwarmTools.GetArgumentValues(arguments, '-build')
    selectionsToBuild += SwarmTools.GetArgumentValues(arguments, '-b')

    buildSelections = GetBuildSelections(arguments)
    BuildSelections(selectionsToBuild, buildSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleBuildSelections(arguments)
