from DockerBuildManagement import BuildTools


TEST_SAMPLE_FOLDER = 'example'


def ChangeToSampleFolderAndGetCwd():
    selection = {BuildTools.DIRECTORY_KEY: TEST_SAMPLE_FOLDER}
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(selection)
    return cwd