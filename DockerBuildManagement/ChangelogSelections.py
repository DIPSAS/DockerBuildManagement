from DockerBuildSystem import VersionTools, YamlTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

CHANGELOG_KEY = 'changelog'
FILE_KEY = 'file'
ENV_VERSION_KEY = 'envKey'
ENV_VERSION_MAJOR_KEY = 'envMajorVersionKey'
ENV_VERSION_MINOR_KEY = 'envMinorVersionKey'

def GetInfoMsg():
    infoMsg = "A changelog is configured by adding a 'changelog' property to the .yaml file.\r\n"
    infoMsg += "Set the '{0}' property with the changelog filename (CHANGELOG.md), \r\n".format(FILE_KEY)
    infoMsg += "and set the '{0}' property with the exposed environment key (VERSION) \r\n".format(ENV_VERSION_KEY)
    infoMsg += "You may also set the '{0}' property with the exposed environment key for version major (VERSIONMAJOR) \r\n".format(ENV_VERSION_MAJOR_KEY)
    infoMsg += "and the '{0}' property with the exposed environment key for version minor (VERSIONMINOR) \r\n".format(ENV_VERSION_MINOR_KEY)
    return infoMsg


def GetChangelogSelection(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(
        arguments, BuildTools.DEFAULT_BUILD_MANAGEMENT_YAML_FILES)
    return YamlTools.GetProperties(CHANGELOG_KEY, yamlData)


def ExportChangelogSelection(changelogSelection):
    if not(FILE_KEY in changelogSelection):
        return

    VersionTools.ExportVersionFromChangelogToEnvironment(
        changelogSelection[FILE_KEY], YamlTools.TryGetFromDictionary(changelogSelection, ENV_VERSION_KEY, 'VERSION'),
        YamlTools.TryGetFromDictionary(changelogSelection, ENV_VERSION_MAJOR_KEY, None),
        YamlTools.TryGetFromDictionary(changelogSelection, ENV_VERSION_MINOR_KEY, None))


def HandleChangelogSelections(arguments):
    if '-help' in arguments:
        print(GetInfoMsg())
        return

    changelogSelection = GetChangelogSelection(arguments)
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(changelogSelection)

    BuildTools.HandleTerminalCommandsSelection(changelogSelection)
    ExportChangelogSelection(changelogSelection)

    os.chdir(cwd)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleChangelogSelections(arguments)
