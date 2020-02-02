from DockerBuildSystem import DockerComposeTools, YamlTools, TerminalTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

PROMOTE_KEY = 'promote'
CONTAINER_ARTIFACT_KEY = 'containerArtifact'

def GetInfoMsg():
    infoMsg = "Promote selections is configured by adding a 'promote' property to the .yaml file.\r\n"
    infoMsg += "The 'promote' property is a dictionary of promote selections.\r\n"
    infoMsg += "Add '-promote' to the arguments to promote all selections in sequence, \r\n"
    infoMsg += "or add specific selection names to promote those only.\r\n"
    infoMsg += "Example: 'dbm -promote myPromoteSelection'.\r\n"
    return infoMsg


def GetPromoteSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    promoteProperty = YamlTools.GetProperties(PROMOTE_KEY, yamlData)
    if BuildTools.SELECTIONS_KEY in promoteProperty:
        return promoteProperty[BuildTools.SELECTIONS_KEY]
    return {}


def PromoteSelections(selectionsToPromote, promoteSelections):
    if len(selectionsToPromote) == 0:
        for promoteSelection in promoteSelections:
            PromoteSelection(promoteSelections[promoteSelection], promoteSelection)
    else:
        for selectionToPromote in selectionsToPromote:
            if selectionToPromote in promoteSelections:
                PromoteSelection(promoteSelections[selectionToPromote], selectionToPromote)


def PromoteSelection(promoteSelection, selectionToPromote):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(promoteSelection)
    BuildTools.HandleTerminalCommandsSelection(promoteSelection)
    TerminalTools.LoadDefaultEnvironmentVariablesFile()


    if BuildTools.FILES_KEY in promoteSelection:
        if YamlTools.TryGetFromDictionary(promoteSelection, CONTAINER_ARTIFACT_KEY, True):
            PromoteImageSelection(promoteSelection, selectionToPromote)
        else:
            print('Only image promotion is supported')
    
    os.chdir(cwd)


def PromoteImageSelection(promoteSelection, selectionToPromote):
    print("selection to promote: {}".format(selectionToPromote))

    composeFiles = promoteSelection[BuildTools.FILES_KEY]
    promoteComposeFile = BuildTools.GetAvailableComposeFilename('promote', selectionToPromote)
    DockerComposeTools.MergeComposeFiles(composeFiles, promoteComposeFile)

    sourceFeed = YamlTools.TryGetFromDictionary(promoteSelection, BuildTools.SOURCE_FEED_KEY, None)
    targetFeed = YamlTools.TryGetFromDictionary(promoteSelection, BuildTools.TARGET_FEED_KEY, None)
    user = YamlTools.TryGetFromDictionary(promoteSelection, BuildTools.USER_KEY, None)
    password = YamlTools.TryGetFromDictionary(promoteSelection, BuildTools.PASSWORD_KEY, None)
    logout = YamlTools.TryGetFromDictionary(promoteSelection, BuildTools.LOGOUT_KEY, False)
    dryRun = YamlTools.TryGetFromDictionary(promoteSelection, BuildTools.DRY_RUN_KEY, False)
    
    DockerComposeTools.PromoteDockerImages(
        composeFile=promoteComposeFile,
        targetTags=promoteSelection[BuildTools.TARGET_TAGS_KEY],
        sourceFeed=sourceFeed,
        targetFeed=targetFeed,
        user=user,
        password=password,
        logoutFromFeeds=logout,
        dryRun=dryRun)

    BuildTools.RemoveComposeFileIfNotPreserved(promoteComposeFile, promoteSelection)


def HandlePromoteSelections(arguments):
    if len(arguments) == 0:
        return
    if not('-promote' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    selectionsToPromote = SwarmTools.GetArgumentValues(arguments, '-promote')
    selectionsToPromote += SwarmTools.GetArgumentValues(arguments, '-pr')

    promoteSelections = GetPromoteSelections(arguments)
    PromoteSelections(selectionsToPromote, promoteSelections)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandlePromoteSelections(arguments)
