import sys
import os.path
from DockerBuildManagement import ChangelogSelections, BuildSelections, PublishSelections, RunSelections, SwarmSelections, TestSelections, BuildTools
from SwarmManagement import SwarmTools

def GetInfoMsg():
    infoMsg = "Docker Build Management\r\n\r\n"
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

def GetNoYmlFilesFoundMsg():
    infoMsg = "\033[1;31;49mError Docker Build Management\r\n"
    infoMsg += "\033[0;37;49mCould not find any supported build management files.\r\n"
    infoMsg += "Are you in the right directory?\r\n"
    infoMsg += "Supported build files: " + str.join(', ', BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    return infoMsg

def AssertYamlFilesExists():
    buildFiles = BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES.copy()
    for buildFile in BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES:
        
        if not os.path.isfile(buildFile):
            buildFiles.remove(buildFile)
    
    if len(buildFiles) == 0:
        print(GetNoYmlFilesFoundMsg())
        exit(-1)

    BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES = buildFiles
    
def HandleManagement(arguments):
    if len(arguments) == 0:
        print(GetInfoMsg())
        return

    if '-help' in arguments and len(arguments) == 1:
        print(GetInfoMsg())
        return

    AssertYamlFilesExists()
    
    SwarmTools.LoadEnvironmentVariables(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    SwarmTools.HandleDumpYamlData(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    ChangelogSelections.HandleChangelogSelections(arguments)
    SwarmSelections.HandleSwarmSelections(arguments)
    BuildSelections.HandleBuildSelections(arguments)
    TestSelections.HandleTestSelections(arguments)
    RunSelections.HandleRunSelections(arguments)
    PublishSelections.HandlePublishSelections(arguments)

if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleManagement(arguments)
