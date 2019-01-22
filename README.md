# Docker Build Management

[![PyPI version](https://badge.fury.io/py/DockerBuildManagement.svg)](https://badge.fury.io/py/DockerBuildManagement)

Build Management is a python application, installed with pip.
The application makes it easy to manage a build system based on Docker by configuring a single *.yml file describing how to build the solution.

## Install And/Or Upgrade
- pip install --no-cache-dir --upgrade DockerBuildManagement

## Example

Either of the sections (`run`, `build`, `test`, `publish`) in the yaml file is triggered with the following cli commands:
- `dbm -run`
- `dbm -build`
- `dbm -test`
- `dbm -publish`

The `swarm` section helps deploying necessary domain services needed in the development.
Start/Stop the swarm:
- `dbm -start`
- `dbm -stop`

Please refer to the [`SwarmManagement`](https://github.com/DIPSAS/SwarmManagement) project for further info on how to configure the swarm deployment.

By convention, the default yaml filename is `build-management.yml`.
It is possible to specify a separate yaml file (or multiple) with the `-f` key:
- `dbm -f my-build.yml -run`

```yml
changelog:
    file: CHANGELOG.md
    envKey: VERSION

env_files: 
    - environment.env

run:
    selections:
        firstSelection:
            directory: src
            abortOnContainerExit: true
            detached: false
            files:
                - docker-compose.proxy.yml
                - docker-compose.proxy.2.yml
        secondSelection:
            directory: src
            abortOnContainerExit: false
            detached: false
            files:
                - docker-compose.proxy.yml

build:
    selections:
        firstSelection:
            directory: src
            additionalTag: latest
            files:
                - docker-compose.proxy.yml

test:
    selections:
        firstSelection:
            directory: src
            removeContainers: true
            containerNames:
                - ssl-proxy-web-c-name
            files:
                - docker-compose.proxy.yml

publish:
    selections:
        firstSelection:
            directory: src
            additionalTag: latest
            files:
                - docker-compose.proxy.yml
        secondSelection:
            directory: src
            containerArtifact: false
            files:
                - docker-compose.proxy.yml

swarm:
    selections:
        firstSelection:
            directory: src
            properties:
                - some-property
            files:
                - swarm-management.yml
```

Please have a look at an example of use here:
- https://github.com/DIPSAS/DockerBuildManagement/tree/master/example

Or take a look at another project which takes use of this library:
- https://github.com/DIPSAS/FluentDbTools

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
