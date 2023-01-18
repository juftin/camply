#!/usr/bin/env bash

set -e

FORMER_PWD="${PWD}"

SCRIPT_PATH="$(dirname -- "${BASH_SOURCE[0]}")"
ABSOLUTE_PATH="$(readlink -f "${SCRIPT_PATH}")"
GITHUB_DIR="$(dirname "${ABSOLUTE_PATH}")"
REPO_DIR="$(dirname "${GITHUB_DIR}")"

cd "${REPO_DIR}"

POETRY_VERSION="$(poetry version)"
PACKAGE_NAME="$(echo "${POETRY_VERSION}" | awk '{ print $1 }')"

NEXT_VERSION="${1}"

if [ -z "${NEXT_VERSION}" ]; then exit 1; fi

NORMALIZED_SOURCE_CODE_DIRECTORY="${PACKAGE_NAME//-/_}"
SOURCE_CODE_DIRECTORY="${SOURCE_CODE_DIRECTORY:-${NORMALIZED_SOURCE_CODE_DIRECTORY}}"

poetry version "${NEXT_VERSION}"
REPLACED_VERSION_FILE_TEXT=$(grep -F -v "__version__" "${SOURCE_CODE_DIRECTORY}/_version.py")
echo "${REPLACED_VERSION_FILE_TEXT}" > "${SOURCE_CODE_DIRECTORY}/_version.py"
echo "__version__ = \"${NEXT_VERSION}\"" >> "${SOURCE_CODE_DIRECTORY}/_version.py"

cd "${FORMER_PWD}"
