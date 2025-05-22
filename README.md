# cattlepoint-aer3-week2
Capstone Project for AWS ER - Week 2
#### Finalized May 22nd 2025

## Overview
* These instructions are intended for participants of the AWS Engagement Ready Class started in April 2025
* The goal of this week2 project is to verify minimal Kubernetes competency and to ensure that the environment is working properly
* This project assumes that you have access to the eruser315 credentials
* This project also assumes that you are running the latest MacOS and have terminal access sufficient to install local applications

## Prerequisite
### This section is to ensure you have access to the AWS account and the necessary credentials
* Request access to private repo cattlepoint/cattlepoint-aer3-week2
* Login to [AWS Account eruser315account](https://eruser315account.signin.aws.amazon.com/console) using username eruser315 and password *****
* [Download AWS Access Keys](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials/access-key-wizard) file eruser315_accessKeys.csv by selecting Command Line Interface (CLI) and I understand the above recommendation and want to proceed to create an access key -> Next

## 20 points – Create and configure your deployment environment
### This section installs the AWS CLI and configures it with the credentials from the CSV file
* If you haven't already done so, setup Homebrew on your MacOS following [these instructions](https://brew.sh/).
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
* Perform these steps in the MacOS terminal to install the AWS CLI
```sh
brew update && brew install awscli
```
* Next we need to configure the AWS CLI with the credentials from the CSV file. You can do this by running the following command in your terminal:
```sh
aws configure --profile eruser315
```
* When prompted, enter the access key and secret access key from the CSV file.  Set the default region to us-east-1 and the output format to json.  The command will look like this:
```sh
% aws configure --profile eruser315
AWS Access Key ID [****************GFJ2]:
AWS Secret Access Key [****************Ya3D]:
Default region name [us-east-1]:
Default output format [json]:
```
* Verify AWS credentials are working:
```sh
export AWS_PROFILE=eruser315
aws sts get-caller-identity
```
* Visually verify in output: arn:aws:iam::****:user/eruser315

### This section installs the latest version of the Kubernetes Command Line Tool, Amazon Elastic Kubernetes Service (Amazon EKS) Command Line Tool (eksctl), Podman (Docker), Helm, project dependencies and verifies they are working
* Perform these steps in the MacOS terminal to install podman, git, github client, kubectl, and eksctl:
```sh
brew update && brew install git gh kubectl eksctl podman helm
```
* Login to your github account following the instructions the below command provides:
```sh
gh login
```
* Verify the the github client is working:
```sh
gh auth status
```

* Expected output (contents will vary):
```sh
✓ Logged in to github.com account
```

* Verify the git tool is working:
```sh
git --version
```

* Verify the the Kubernetes CLI is working:
```sh
kubectl version --client
```

* Verify the the eksctl is working:
```sh
eksctl version
```

* Verify podman is working:
```sh
podman -v
```

* Verify helm is working:
```sh
helm version
```


## 20 points – Containerize and store your images in a repository
## 10 points – Deploy an Amazon EKS cluster
## 40 points – Deploy your application, including a backend database
## 10 points – Test updating your application using rolling updates
