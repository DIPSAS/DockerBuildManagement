import sys
import time
from DockerBuildManagement import ChangelogSelections, BuildSelections, PublishSelections, RunSelections, SwarmSelections, TestSelections, BuildTools
from DockerBuildSystem import DockerSwarmTools, TerminalTools


def GetInfoMsg():
    infoMsg = "Manage Docker Swarm\r\n"
    infoMsg += "Add '-start' to arguments to start development by deploying domain services in a swarm.\r\n"
    infoMsg += "Add '-stop' to arguments to stop development by stopping domain services in the swarm.\r\n"
    infoMsg += "Add '-restart' to arguments to restart swarm.\r\n"
    infoMsg += "Otherwise:\r\n\r\n"
    infoMsg += "Run:\r\n"
    infoMsg += RunSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Build:\r\n"
    infoMsg += BuildSelections.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Publish:\r\n"
    infoMsg += PublishSelections.GetInfoMsg() + "\r\n\r\n"
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


def HandleManagement(arguments):
    if len(arguments) == 0:
        print(GetInfoMsg())

    if '-help' in arguments and len(arguments) == 1:
        print(GetInfoMsg())

    environmentFiles = BuildTools.GetEnvironmnetVariablesFiles(arguments)
    for environmentFile in environmentFiles:
        TerminalTools.LoadEnvironmentVariables(environmentFile)

    ChangelogSelections.HandleChangelogSelections(arguments)
    SwarmSelections.HandleSwarmSelections(arguments)
    BuildSelections.HandleBuildSelections(arguments)
    TestSelections.HandleTestSelections(arguments)
    RunSelections.HandleRunSelections(arguments)
    PublishSelections.HandlePublishSelections(arguments)

if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleManagement(arguments)
