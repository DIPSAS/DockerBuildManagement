from DockerBuildSystem import DockerComposeTools, YamlTools, TerminalTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os
import requests
from requests.exceptions import HTTPError

PROMOTE_KEY = 'promote'

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


    if BuildTools.IMAGES_KEY in promoteSelection:
        PromoteImageSelection(promoteSelection, selectionToPromote)
    else:
        raise Exception('"No images provided! Only image promotion through artifactory API is supported at this time"')
    
    os.chdir(cwd)


def PromoteImageSelection(promoteSelection, selectionToPromote):
    print("selection to promote")
    print(selectionToPromote)


    for image in promoteSelection[BuildTools.IMAGES_KEY]:

        for sourceTargetTags in promoteSelection[BuildTools.SOURCE_TARGET_TAGS_KEY]:
            data = {
                 "targetRepo": promoteSelection[BuildTools.TARGET_FEED_KEY],
                 "dockerRepository":  image,
                 "tag": sourceTargetTags.get("sourceTag"),
                 "targetTag": sourceTargetTags.get("targetTag"),
                 "copy": promoteSelection[BuildTools.COPY_KEY]
             }

            if BuildTools.DRY_RUN_KEY in promoteSelection and promoteSelection[BuildTools.DRY_RUN_KEY]:
                print("Would have promoted: ")
                print(data)
            elif (BuildTools.DRY_RUN_KEY not in promoteSelection) or \
                     (not promoteSelection[BuildTools.DRY_RUN_KEY] or promoteSelection[BuildTools.DRY_RUN_KEY] is None):

                try:

                    if(BuildTools.CERT_FILE_PATH_KEY in promoteSelection):
                        headers={'Content-type':'application/json'}
                        response = requests.post(promoteSelection[BuildTools.PROMOTE_URI_KEY], 
                        json=data, 
                        auth=(promoteSelection[BuildTools.USER_KEY], promoteSelection[BuildTools.PASSWORD_KEY]), 
                        verify=promoteSelection[BuildTools.CERT_FILE_PATH_KEY])

                        response.raise_for_status()
                    else:
                        raise Exception('No certificate provided for communication with artifactory')

                except HTTPError as http_err:
                    print(f'HTTP error occurred during promotion: {http_err}')
                except Exception as err:
                    print(f'An error occurred during promotion: {err}')

                else:
                     print("Successfully promoted " + sourceTargetTags.get("sourceTag") + " as " + sourceTargetTags.get("targetTag"))


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
