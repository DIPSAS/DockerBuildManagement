from SwarmManagement import SwarmTools
import os

SELECTIONS_KEY = 'selections'
FILES_KEY = 'files'
DIRECTORY_KEY = 'directory'
ADDITIONAL_TAG_KEY = 'additionalTag'

def GetInfoMsg():
    infoMsg = "One or more yaml files are used to configure the build.\r\n"
    infoMsg += "The yaml file 'build-management.yml' is used by default if no other files are specified.\r\n"
    infoMsg += "A yaml file may be specified by adding '-file' or '-f' to the arguments.\r\n"
    infoMsg += "Example: -f build-management-1.yml -f build-management-2.yml\r\n"
    return infoMsg


def GetDockerBuildManagementYamlData(arguments):
    yamlFiles = SwarmTools.GetArgumentValues(arguments, '-file')
    yamlFiles += SwarmTools.GetArgumentValues(arguments, '-f')
    if len(yamlFiles) == 0:
        yamlFiles.append('build-management.yml')
    yamlData = SwarmTools.GetYamlData(yamlFiles)
    return yamlData


def GetEnvironmnetVariablesFiles(arguments):
    yamlData = GetDockerBuildManagementYamlData(arguments)
    envFiles = []
    if 'env_files' in yamlData:
        envFiles += yamlData['env_files']
    envFiles += SwarmTools.GetArgumentValues(arguments, '-env')
    envFiles += SwarmTools.GetArgumentValues(arguments, '-e')
    return envFiles


def GetProperties(arguments, propertyType, errorInfoMsg):
    yamlData = GetDockerBuildManagementYamlData(arguments)
    properties = {}
    if propertyType in yamlData:
        properties = yamlData[propertyType]
    return properties


def TryChangeToDirectoryAndGetCwd(selection):
    cwd = os.getcwd()
    if DIRECTORY_KEY in selection:
        if len(selection[DIRECTORY_KEY]) > 0:
            os.chdir(selection[DIRECTORY_KEY])
    return cwd


def TryGetFromDictionary(dictionary, key, defaultValue):
    if key in dictionary:
        return dictionary[key]
    return defaultValue
