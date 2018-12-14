# Docker Build Management
Build Management is a python application, installed with pip.
The application makes it easy to manage a build system based on Docker by configuring a single *.yml file describing how to build the solution.

## Example
1. Install DockerBuildManagement with pip:
    - pip install DockerBuildManagement

Please have a look at an example of use here:
- https://github.com/DIPSAS/DockerBuildManagement/tree/master/example

## Install And/Or Upgrade
- pip install --no-cache-dir --upgrade DockerBuildManagement

## Prerequisites
- Docker:
    - https://www.docker.com/get-docker

## Additional Info
- The pip package may be located at:
    - https://pypi.org/project/DockerBuildManagement

## Publish New Version.
1. Configure setup.py with new version.
2. Build: python setup.py bdist_wheel
3. Publish: twine upload dist/*