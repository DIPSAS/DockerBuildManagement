import sys
import os
from DockerBuildManagement import ChangelogSelections, BuildSelections, PublishSelections, RunSelections, SwarmSelections, TestSelections, BuildTools, PromoteSelections
from SwarmManagement import SwarmTools

def GetInfoMsg():
    infoMsg = "Docker Build Management\r\n\r\n"
    infoMsg += "Run:\r\n"
    infoMsg += RunSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Build:\r\n"
    infoMsg += BuildSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Publish:\r\n"
    infoMsg += PublishSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Promote:\r\n"
    infoMsg += PromoteSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Test:\r\n"
    infoMsg += TestSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Swarm Deployment of Domain Services:\r\n"
    infoMsg += SwarmSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Export Version From Changelog:\r\n"
    infoMsg += ChangelogSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Additional Info:\r\n"
    infoMsg += BuildTools.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Add '-help' to arguments to print this info again.\r\n\r\n"
    return infoMsg


def GetPositionalActionArguments(arguments, index):
    actionArgs = []
    newIndex = index + 1
    if arguments[index].startswith('-'):
        actionArgs.append(arguments[index])

    if SwarmSelections.CheckSwarmInArguments(actionArgs) \
            and index + 1 < len(arguments) \
            and SwarmSelections.CheckSwarmCommandInArguments([arguments[index + 1]]):
        actionArgs.append(arguments[index + 1])
        newIndex += 1

    if len(actionArgs) > 0:
        selections = SwarmTools.GetArgumentValues(arguments[index:], actionArgs[-1])
        actionArgs += selections

    return actionArgs, newIndex


def SetDefaultCommonEnvVariables():
    if 'PWD' not in os.environ:
        os.environ['PWD'] = os.getcwd().replace('\\', '/')
    
    
def HandleManagement(arguments):
    if len(arguments) == 0:
        print(GetInfoMsg())
        return

    if '-help' in arguments and len(arguments) == 1:
        print(GetInfoMsg())
        return
    
    SwarmTools.LoadEnvironmentVariables(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    SetDefaultCommonEnvVariables()
    SwarmTools.HandleDumpYamlData(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    ChangelogSelections.HandleChangelogSelections(arguments)

    index = 0
    while index < len(arguments):
        actionArgs, index = GetPositionalActionArguments(arguments, index)
        SwarmSelections.HandleSwarmSelections(actionArgs)
        BuildSelections.HandleBuildSelections(actionArgs)
        TestSelections.HandleTestSelections(actionArgs)
        RunSelections.HandleRunSelections(actionArgs)
        PublishSelections.HandlePublishSelections(actionArgs)
        PromoteSelections.HandlePromoteSelections(actionArgs)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleManagement(arguments)
