from DockerBuildSystem import DockerComposeTools, YamlTools, TerminalTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

PUBLISH_KEY = 'publish'
CONTAINER_ARTIFACT_KEY = 'containerArtifact'

def GetInfoMsg():
    infoMsg = "Publish selections is configured by adding a 'publish' property to the .yaml file.\r\n"
    infoMsg += "The 'publish' property is a dictionary of publish selections.\r\n"
    infoMsg += "Add '-publish' to the arguments to publish all selections in sequence, \r\n"
    infoMsg += "or add specific selection names to publish those only.\r\n"
    infoMsg += "Example: 'dbm -publish myPublishSelection'.\r\n"
    return infoMsg


def GetPublishSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    publishProperty = YamlTools.GetProperties(PUBLISH_KEY, yamlData)
    if BuildTools.SELECTIONS_KEY in publishProperty:
        return publishProperty[BuildTools.SELECTIONS_KEY]
    return {}


def PublishSelections(selectionsToPublish, publishSelections):
    if len(selectionsToPublish) == 0:
        for publishSelection in publishSelections:
            PublishSelection(publishSelections[publishSelection], publishSelection)
    else:
        for selectionToPublish in selectionsToPublish:
            if selectionToPublish in publishSelections:
                PublishSelection(publishSelections[selectionToPublish], selectionToPublish)


def PublishSelection(publishSelection, selectionToPublish):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(publishSelection)
    BuildTools.HandleTerminalCommandsSelection(publishSelection)
    TerminalTools.LoadDefaultEnvironmentVariablesFile()

    if BuildTools.FILES_KEY in publishSelection:
        if YamlTools.TryGetFromDictionary(publishSelection, CONTAINER_ARTIFACT_KEY, True):
            PublishContainerSelection(publishSelection, selectionToPublish)
        else:
            PublishArtifactSelection(publishSelection)

        BuildTools.HandleCopyFromContainer(publishSelection)
    
    os.chdir(cwd)


def PublishContainerSelection(publishSelection, selectionToPublish):
    composeFiles = publishSelection[BuildTools.FILES_KEY]
    publishComposeFile = BuildTools.GetAvailableComposeFilename('publish', selectionToPublish)
    DockerComposeTools.MergeComposeFiles(composeFiles, publishComposeFile)

    try:
        DockerComposeTools.PublishDockerImages(publishComposeFile)
    except:
        BuildTools.RemoveComposeFileIfNotPreserved(publishComposeFile, publishSelection)
        raise

    if BuildTools.ADDITIONAL_TAG_KEY in publishSelection:
        DockerComposeTools.PublishDockerImagesWithNewTag(publishComposeFile, publishSelection[BuildTools.ADDITIONAL_TAG_KEY])
    if BuildTools.ADDITIONAL_TAGS_KEY in publishSelection:
        for tag in publishSelection[BuildTools.ADDITIONAL_TAGS_KEY]:
            DockerComposeTools.PublishDockerImagesWithNewTag(publishComposeFile, tag)
    if BuildTools.COMPOSE_FILE_WITH_DIGESTS_KEY in publishSelection:
        composeFileWithDigests = publishSelection[BuildTools.COMPOSE_FILE_WITH_DIGESTS_KEY]
        BuildTools.GenerateComposeFileWithDigests(composeFiles, composeFileWithDigests)

    BuildTools.RemoveComposeFileIfNotPreserved(publishComposeFile, publishSelection)



def PublishArtifactSelection(publishSelection):
    DockerComposeTools.DockerComposeBuild(
        publishSelection[BuildTools.FILES_KEY])
    DockerComposeTools.DockerComposeUp(
        publishSelection[BuildTools.FILES_KEY], False)


def HandlePublishSelections(arguments):
    if len(arguments) == 0:
        return
    if not('-publish' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    selectionsToPublish = SwarmTools.GetArgumentValues(arguments, '-publish')
    selectionsToPublish += SwarmTools.GetArgumentValues(arguments, '-p')

    publishSelections = GetPublishSelections(arguments)
    PublishSelections(selectionsToPublish, publishSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandlePublishSelections(arguments)
