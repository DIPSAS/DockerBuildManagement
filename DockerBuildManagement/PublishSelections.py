from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

PUBLISH_KEY = 'publish'
CONTAINER_ARTIFACT_KEY = 'containerArtifact'

def GetInfoMsg():
    infoMsg = "Publish selections is configured by adding a 'publish' property to the .yaml file.\r\n"
    infoMsg += "The 'publish' property is a dictionary of publish selections.\r\n"
    infoMsg += "Add '-publish' to the arguments to publish all selections in sequence, or add spesific selection names to publish those only.\r\n"
    infoMsg += "Example: 'dbm -publish myPublishSelection'.\r\n"
    return infoMsg


def GetPublishSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, [BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILE])
    publishProperty = SwarmTools.GetProperties(arguments, PUBLISH_KEY, GetInfoMsg(), yamlData)
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


def PublishSelection(publishSelection, publishSelectionKey):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(publishSelection)
    BuildTools.HandleTerminalCommandsSelection(publishSelection)
    if BuildTools.TryGetFromDictionary(publishSelection, CONTAINER_ARTIFACT_KEY, True):
        PublishContainerSelection(publishSelection, publishSelectionKey)
    else:
        PublishArtifactSelection(publishSelection)

    BuildTools.HandleCopyFromContainer(publishSelection)
    
    os.chdir(cwd)


def PublishContainerSelection(publishSelection, publishSelectionKey):
    composeFiles = publishSelection[BuildTools.FILES_KEY]
    publishComposeFile = 'docker-compose.publish.' + publishSelectionKey + '.yml'
    DockerComposeTools.MergeComposeFiles(composeFiles, publishComposeFile)
    DockerComposeTools.PublishDockerImages(publishComposeFile)
    if BuildTools.ADDITIONAL_TAG_KEY in publishSelection:
        DockerComposeTools.PublishDockerImagesWithNewTag(publishComposeFile, publishSelection[BuildTools.ADDITIONAL_TAG_KEY])


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
