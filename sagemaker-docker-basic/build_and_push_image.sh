#!/usr/bin/env bash

# Fail on errors
set -o errexit

# call prepare.sh in the same directory
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sh ${__dir}/prepare.sh

# The name of our algorithm
# TODO: change me
repo_name=REPO_NAME

account=$(aws sts get-caller-identity --query Account --output text)

# Get the region defined in the current configuration (default to us-west-1 if none defined)
region=$(aws configure get region)

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${repo_name}:latest"

# If the repository doesn't exist in ECR, create it.

aws ecr describe-repositories --repository-names "${repo_name}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${repo_name}" > /dev/null
fi

# Get the login command from ECR and login
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${account}.dkr.ecr.${region}.amazonaws.com

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build  -t ${repo_name} -f ${__dir}/Dockerfile .
docker tag ${repo_name} ${fullname}

docker push ${fullname}