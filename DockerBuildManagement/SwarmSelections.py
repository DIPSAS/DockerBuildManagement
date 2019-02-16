from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools, SwarmManager
from DockerBuildManagement import BuildTools
import sys
import os

SWARM_KEY = 'swarm'
PROPERTIES_KEY = 'properties'


def GetInfoMsg():
    infoMsg = "Test selections is configured by adding a 'swarm' property to the .yaml file.\r\n"
    infoMsg += "The 'swarm' property is a dictionary of swarm selections.\r\n"
    infoMsg += "Add '-start' to the arguments to initiate the swarms selections, or add spesific selection names to start those only.\r\n"
    infoMsg += "Example: 'dbm -start mySwarmSelection'.\r\n"
    return infoMsg


def GetSwarmSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, [BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILE])
    publishProperty = SwarmTools.GetProperties(arguments, SWARM_KEY, GetInfoMsg(), yamlData)
    if BuildTools.SELECTIONS_KEY in publishProperty:
        return publishProperty[BuildTools.SELECTIONS_KEY]
    return {}


def DeploySwarmSelections(swarmSelectionsToDeploy, swarmSelections, prefix):
    if len(swarmSelectionsToDeploy) == 0:
        for swarmSelection in swarmSelections:
            DeploySwarmSelection(swarmSelections[swarmSelection], prefix)
    else:
        for swarmSelectionToDeploy in swarmSelectionsToDeploy:
            if swarmSelectionToDeploy in swarmSelections:
                DeploySwarmSelection(swarmSelections[swarmSelectionToDeploy], prefix)


def DeploySwarmSelection(swarmSelection, prefix):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(swarmSelection)
    SwarmManager.HandleManagement(
        [prefix] + BuildSwarmManagementFilesRow(swarmSelection) + BuildSwarmManagementPropertiesRow(swarmSelection))
    os.chdir(cwd)


def BuildSwarmManagementFilesRow(swarmSelection):
    swarmManagementFiles = []
    if not(BuildTools.FILES_KEY in swarmSelection):
        return swarmManagementFiles
    for swarmManagementFile in swarmSelection[BuildTools.FILES_KEY]:
        swarmManagementFiles += ['-f', swarmManagementFile]
    return swarmManagementFiles


def BuildSwarmManagementPropertiesRow(swarmSelection):
    swarmManagementProperties = []
    if not(PROPERTIES_KEY in swarmSelection):
        return swarmManagementProperties
    for swarmManagementProperty in swarmSelection[PROPERTIES_KEY]:
        swarmManagementProperties += str.split(swarmManagementProperty)
    return swarmManagementProperties


def GetPrefix(arguments):
    if '-start' in arguments:
        return '-start'
    if '-stop' in arguments:
        return '-stop'
    if '-restart' in arguments:
        return '-restart'
    return ''


def HandleSwarmSelections(arguments):
    if len(arguments) == 0:
        return
    if not('-start' in arguments or '-stop' in arguments or '-restart' in arguments or '-swarm' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    swarmSelectionsToDeploy = SwarmTools.GetArgumentValues(arguments, '-swarm')
    swarmSelectionsToDeploy += SwarmTools.GetArgumentValues(arguments, '-s')

    swarmSelections = GetSwarmSelections(arguments)
    DeploySwarmSelections(swarmSelectionsToDeploy, swarmSelections, GetPrefix(arguments))


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleSwarmSelections(arguments)
