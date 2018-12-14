from DockerBuildSystem import VersionTools
from SwarmManagement import SwarmTools
from DockerBuildManagement import BuildTools
import sys
import os

CHANGELOG_KEY = 'changelog'
FILE_KEY = 'file'
ENV_VERSION_KEY = 'envKey'

def GetInfoMsg():
    infoMsg = "Changelog selections is configured by adding a 'changelog' property to the .yaml file.\r\n"
    return infoMsg


def GetChangelogSelection(arguments):
    return BuildTools.GetProperties(arguments, CHANGELOG_KEY, GetInfoMsg())


def ExportChangelogSelection(changelogSelection):
    if not(FILE_KEY in changelogSelection):
        return

    VersionTools.ExportVersionFromChangelogToEnvironment(
        changelogSelection[FILE_KEY], BuildTools.TryGetFromDictionary(changelogSelection, ENV_VERSION_KEY, 'VERSION'))


def HandleChangelogSelections(arguments):
    if '-help' in arguments:
        print(GetInfoMsg())
        return

    changelogSelection = GetChangelogSelection(arguments)
    ExportChangelogSelection(changelogSelection)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleChangelogSelections(arguments)
