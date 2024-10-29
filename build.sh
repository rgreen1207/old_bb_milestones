#!/usr/bin/env bash
#
# This is a simple script to create/delete a Git tag, which itself triggers
# CI/CD, ultimately pushing that build+tag to Docker Hub
#
# Usage:
#
# ./build.sh 0.0.7
#
# Will create a git tag (which will trigger a build) with the tag in the
# form v0.0.7-54477d3 -- note the "v" is prepended and the current sha
# is appended
#
# ./build.sh v0.0.7-54477d3 delete
#
# Will simply delete the tag "v0.0.7-54477d3", note that it does not remove
# the build from Docker Hub
#

TAG=$1
DELETE=$2

# show tags:
# git tag -l | sort -V

if [ -z ${TAG} ]; then
    echo "Missing TAG, usage $0 v0.2.0 [delete]"
    exit 1
fi

if [ -z ${DELETE} ]; then
    # append the v
    TAG=v${TAG}
    # append the current gitsha
    SHA=$(git rev-parse --short HEAD)
    TAG=${TAG}-${SHA}

    read -p "Tag and push as ${TAG}?  Are you sure? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag ${TAG}
        git push origin ${TAG}
    fi    
    echo "Release tag:  $TAG"
else
    read -p "Delete tag ${TAG}?  Are you sure? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d ${TAG}
        git push --delete origin ${TAG}
    fi
fi