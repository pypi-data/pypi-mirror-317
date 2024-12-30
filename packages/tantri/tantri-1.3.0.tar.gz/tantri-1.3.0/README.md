# tantri - generating telegraph noise and other Dipole TLS calculations

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg?style=flat-square)](https://conventionalcommits.org)
[![PyPI](https://img.shields.io/pypi/v/tantri?style=flat-square)](https://pypi.org/project/tantri/)
[![Jenkins](https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins.deepak.science%2Fjob%2Fgitea-physics%2Fjob%2Ftantri%2Fjob%2Fmaster&style=flat-square)](https://jenkins.deepak.science/job/gitea-physics/job/tantri/job/master/)
![Jenkins tests](https://img.shields.io/jenkins/tests?compact_message&jobUrl=https%3A%2F%2Fjenkins.deepak.science%2Fjob%2Fgitea-physics%2Fjob%2Ftantri%2Fjob%2Fmaster%2F&style=flat-square)
![Jenkins Coverage](https://img.shields.io/jenkins/coverage/cobertura?jobUrl=https%3A%2F%2Fjenkins.deepak.science%2Fjob%2Fgitea-physics%2Fjob%2Ftantri%2Fjob%2Fmaster%2F&style=flat-square)
![Maintenance](https://img.shields.io/maintenance/yes/2024?style=flat-square)


Named as an oblique half-pun on both tantri as a form of generating, and tantri as a telegraph or wire.

## dev

Build with `just`, preferred over `do.sh` I think.

## CLI

The json files for dots and dipoles have a specific format that ignores extraneous data but is sad about missing fields.
