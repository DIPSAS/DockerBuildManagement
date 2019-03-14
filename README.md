# Docker Build Management

[![PyPI version](https://badge.fury.io/py/DockerBuildManagement.svg)](https://badge.fury.io/py/DockerBuildManagement)
[![Build Status](https://travis-ci.com/DIPSAS/DockerBuildManagement.svg?branch=master)](https://travis-ci.com/DIPSAS/DockerBuildManagement)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

Build Management is a python application, installed with pip.
The application makes it easy to manage a build system based on Docker by configuring a single *.yml file describing how to build the solution.

## Install Or Upgrade
- pip install --upgrade DockerBuildManagement

## Verify Installation
- `dbm -help`

## Example

Either of the sections (`run`, `build`, `test`, `publish`) in the yaml file is triggered with the following cli commands:
- `dbm -run`
- `dbm -build`
- `dbm -test`
- `dbm -publish`

Each of the command sections (`run`, `build`, `test`, `publish`) includes context sections, each defined by a suitable key describing that section. Each of the context sections are executed in sequence from top to bottom by default, or you may specify the sections to execute by adding the section keys to the command line:
- `dbm -run secondSelection`

It is also possible to execute multiple command sections in the same command line:
- `dbm -test -build -run secondSelection`

The `swarm` section helps deploying necessary domain services needed in the development.
Start/Stop/Restart the swarm:
- `dbm -swarm -start`
- `dbm -swarm -stop`
- `dbm -swarm -restart`

Please refer to the [SwarmManagement](https://github.com/DIPSAS/SwarmManagement) project for further info on how to configure the swarm deployment.

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
            copyFromContainer:
                pythonSnippet:
                    containerSrc: /src/
                    hostDest: output/
            cmd:
                - python ./pythonSnippet.py
            abortOnContainerExit: true
            detached: false
            files:
                - docker-compose.pythonSnippet.yml
                - docker-compose.pythonSnippet.overriden.yml
        secondSelection:
            directory: src
            files:
                - docker-compose.pythonSnippet.yml

build:
    selections:
        firstSelection:
            directory: src
            cmd:
                - python ./pythonSnippet.py
            additionalTag: latest
            additionalTags:
                - beta
                - zeta
            saveImages: ../output
            files:
                - docker-compose.pythonSnippet.yml

test:
    selections:
        firstSelection:
            directory: src
            cmd:
                - python ./pythonSnippet.py
            removeContainers: true
            containerNames:
                - pythonSnippet
            files:
                - docker-compose.pythonSnippet.yml

publish:
    selections:
        firstSelection:
            directory: src
            cmd:
                - python ./pythonSnippet.py
            additionalTag: latest
            additionalTags:
                - beta
                - zeta
            files:
                - docker-compose.pythonSnippet.yml
        secondSelection:
            directory: src
            containerArtifact: false
            files:
                - docker-compose.pythonSnippet.yml

swarm:
    selections:
        firstSelection:
            directory: src
            cmd:
                - python ./pythonSnippet.py
            properties:
                - -stack -remove proxy
            files:
                - swarm-management.yml
```

Please have a look at an example of use here:
- https://github.com/DIPSAS/DockerBuildManagement/tree/master/example

Or take a look at another project which takes use of this library:
- https://github.com/DIPSAS/FluentDbTools

## Section Features

### General features
- `directory` -> Each section has a `directory` property defining in which relative directory the section will be executed. Note that all relative position to files and command lines will be executed relative to this directory during execution of that section.
- `files` -> Each section has a `files` property listing all `docker-compose.yml` files to use when either building, testing or running the services listed in `docker-compose.yml`.
- `cmd` -> Executes a list of command lines before initiating the main job of the section.

### Run Features
The `run` section runs all listed docker-compose files with `docker-compose up`.
- `abortOnContainerExit: true/false` -> Tell docker-compose to abort when either of the containers exits. Default is `true`.
- `detached: true/false` -> Tell docker-compose to run the services in detached mode. Default is `false`.
- `copyFromContainer` -> Copy anything from a docker container to a destination on your computer. The section contains keys matching the container name, and this key has the following sub-keys:
    - `containerSrc: <folder_path/file_path>` -> Source path to copy from the container.
    -  `hostDest: <folder_path/file_path>` -> Destination path on your computer to copy the container content.

### Build Features
The `build` section builds all docker images as described by the `docker-compose.yml` files.
- `additionalTag: <additional_image_tag>` -> Include an additional tag to all built docker images.
- `additionalTags: <list_of_additional_image_tags>` -> Include a list of additional tags to all built docker images.
- `saveImages: <output_folder>` -> Save all built docker images from the compose file as tar files. The files will be saved in the given output folder.

### Test Features
The `test` section runs all services listed in the `docker-compose.yml` files, and detects if either of the services exited with a non-zero exit code due to an error.
- `containerNames` -> List of container names of the services to check for the non-zero exit code.
- `removeContainers: true/false` -> Remove containers created by the services. Default is `true`.

### Publish Features
The `publish` section publishes all docker images listed in the `docker-compose.yml` files.
- `additionalTag: <additional_image_tag>` -> Include an additional tag to publish with the docker images.
- `additionalTags: <list_of_additional_image_tags>` -> Include a list of additional tags to publish with the docker images.
- `containerArtifact: true/false` -> Sometimes the solution does not publish docker images, but just something else such as nugets, pypi or gem packages. With this property set to `true`, you can make a docker container do the work of publishing the artifact. Default is `false`.

### Swarm Features
The `swarm` section helps to deploy service stacks to your local swarm. It reuses the [SwarmManagement](https://github.com/DIPSAS/SwarmManagement) deployment tool to deploy and remove services to and from the Swarm.
- `files` -> The `files` property lists all `swarm-management.yml` deployment files to use for deploying stacks on the Swarm.
- `properties` -> This property is a list of `SwarmManagement` commands to run in addition to starting or stopping the Swarm stacks.

### General Properties
- `changelog` -> The `changelog` property parses a [CHANGELOG.md](example/CHANGELOG.md) file and sets an environment variables with current version. It contains following sub-keys:
    - `file` -> Path to the `CHANGELOG.md` file.
    - `envKey` -> On which environment variable to expose the version value. Default is `VERSION`.
- `env_files` -> List of `.env` files listing environment variables to expose. By convention, a present `.env` file will automatically be used to expose environment variables. Additionally, any yaml file may contain the `${*}` sequence anywhere in the file. The matching environment variable (`ENV_KEY` of `${ENV_KEY}`) will replace this sequence with the value of the environment variable.

## Prerequisites
- Docker:
    - https://www.docker.com/get-docker
- Install Dependencies:
    - pip install -r requirements.txt

## Additional Info
- The pip package may be located at:
    - https://pypi.org/project/DockerBuildManagement

## Publish New Version
1. Configure setup.py with new version.
2. Build: python setup.py bdist_wheel
3. Publish: twine upload dist/*

## Run Unit Tests
- python -m unittest
