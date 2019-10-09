from SwarmManagement import SwarmTools, SwarmManager
from DockerBuildManagement import BuildTools
from DockerBuildSystem import YamlTools, TerminalTools
import sys
import os

SWARM_KEY = 'swarm'
PROPERTIES_KEY = 'properties'


def GetInfoMsg():
    infoMsg = "Swarm selections is configured by adding a 'swarm' property to the .yaml file.\r\n"
    infoMsg += "The 'swarm' property is a dictionary of swarm selections.\r\n"
    infoMsg += "Add '-swarm -start' to the arguments to initiate all swarm selections, \r\n"
    infoMsg += "or add specific selection names to start those only.\r\n"
    infoMsg += "Add '-swarm -stop' to the arguments to stop all swarm selections, \r\n"
    infoMsg += "or add specific selection names to stop those only.\r\n"
    infoMsg += "Add '-swarm -restart' to the arguments to restart all swarm selections, \r\n"
    infoMsg += "or add specific selection names to restart those only.\r\n"
    infoMsg += "Example: 'dbm -swarm -start mySwarmSelection'.\r\n"
    infoMsg += "Example: 'dbm -swarm -stop mySwarmSelection'.\r\n"
    infoMsg += "Example: 'dbm -swarm -restart mySwarmSelection'.\r\n"
    return infoMsg


def GetSwarmSelections(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    swarmProperty = YamlTools.GetProperties(SWARM_KEY, yamlData)
    if BuildTools.SELECTIONS_KEY in swarmProperty:
        return swarmProperty[BuildTools.SELECTIONS_KEY]
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
    BuildTools.HandleTerminalCommandsSelection(swarmSelection)
    TerminalTools.LoadDefaultEnvironmentVariablesFile()
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


def GetSwarmCommand(arguments):
    if '-start' in arguments:
        return '-start'
    if '-stop' in arguments:
        return '-stop'
    if '-restart' in arguments:
        return '-restart'
    return ''


def CheckSwarmCommandInArguments(arguments):
    if GetSwarmCommand(arguments) == '':
        return False
    return True


def CheckSwarmInArguments(arguments):
    if '-swarm' in arguments or '-s' in arguments:
        return True
    return False


def HandleSwarmSelections(arguments):
    if len(arguments) == 0:
        return
    if not(CheckSwarmInArguments(arguments)) and not(CheckSwarmCommandInArguments(arguments)):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    if CheckSwarmInArguments(arguments) and not(CheckSwarmCommandInArguments(arguments)):
        print(GetInfoMsg())

    swarmSelectionsToDeploy = SwarmTools.GetArgumentValues(arguments, '-swarm')
    swarmSelectionsToDeploy += SwarmTools.GetArgumentValues(arguments, '-s')

    if not(CheckSwarmInArguments(arguments)) and CheckSwarmCommandInArguments(arguments):
        swarmSelectionsToDeploy += SwarmTools.GetArgumentValues(arguments, '-start')
        swarmSelectionsToDeploy += SwarmTools.GetArgumentValues(arguments, '-stop')
        swarmSelectionsToDeploy += SwarmTools.GetArgumentValues(arguments, '-restart')

    swarmSelections = GetSwarmSelections(arguments)
    DeploySwarmSelections(swarmSelectionsToDeploy, swarmSelections, GetSwarmCommand(arguments))


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleSwarmSelections(arguments)
