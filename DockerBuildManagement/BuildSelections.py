from DockerBuildSystem import DockerComposeTools, YamlTools, TerminalTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

BUILD_KEY = 'build'
SAVE_IMAGES_KEY = 'saveImages'


def GetInfoMsg():
    infoMsg = "Build selections is configured by adding a 'build' property to the .yaml file.\r\n"
    infoMsg += "The 'build' property is a dictionary of build selections.\r\n"
    infoMsg += "Add '-build' to the arguments to build all selections in sequence, \r\n"
    infoMsg += "or add specific selection names to build those only.\r\n"
    infoMsg += "Example: 'dbm -build myBuildSelection'.\r\n"
    return infoMsg


def GetBuildSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    buildProperty = YamlTools.GetProperties(BUILD_KEY, yamlData)
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
    TerminalTools.LoadDefaultEnvironmentVariablesFile()

    if BuildTools.FILES_KEY in buildSelection:
        composeFiles = buildSelection[BuildTools.FILES_KEY]
        buildComposeFile = BuildTools.GetAvailableComposeFilename('build', selectionToBuild)
        DockerComposeTools.MergeComposeFiles(composeFiles, buildComposeFile)

        try:
            DockerComposeTools.DockerComposeBuild([buildComposeFile])
        except:
            BuildTools.RemoveComposeFileIfNotPreserved(buildComposeFile, buildSelection)
            raise

        if BuildTools.ADDITIONAL_TAG_KEY in buildSelection:
            DockerComposeTools.TagImages(buildComposeFile, buildSelection[BuildTools.ADDITIONAL_TAG_KEY])
        if BuildTools.ADDITIONAL_TAGS_KEY in buildSelection:
            for tag in buildSelection[BuildTools.ADDITIONAL_TAGS_KEY]:
                DockerComposeTools.TagImages(buildComposeFile, tag)
        if SAVE_IMAGES_KEY in buildSelection:
            outputFolder = buildSelection[SAVE_IMAGES_KEY]
            DockerComposeTools.SaveImages(buildComposeFile, outputFolder)

        if BuildTools.COMPOSE_FILE_WITH_DIGESTS_KEY in buildSelection:
            composeFileWithDigests = buildSelection[BuildTools.COMPOSE_FILE_WITH_DIGESTS_KEY]
            BuildTools.GenerateComposeFileWithDigests(composeFiles, composeFileWithDigests)

        BuildTools.RemoveComposeFileIfNotPreserved(buildComposeFile, buildSelection)
            
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
