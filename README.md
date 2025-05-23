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
* Login to [AWS Account eruser315account](https://eruser315account.signin.aws.amazon.com/console) using username eruser315 and password ***
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
* Visually verify in output: arn:aws:iam::***:user/eruser315

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
### In this section you will the Dockerfiles, build the images, and push them to the Amazon Elastic Container Registry (ECR) repositories
* For this section, you will need to have cloned the repository to your local machine.  You can do this by running the following command in your terminal:
```sh
gh repo clone cattlepoint/cattlepoint-aer3-week2
```
* For this section, make sure you are in the repository directory:
```sh
cd cattlepoint-aer3-week2
```
* Verify AWS credentials are working:
```sh
export AWS_PROFILE=eruser315
aws sts get-caller-identity
```
* Visually verify in output: arn:aws:iam::***:user/eruser315

#### This section shows a quick-start method for the below sections
* This step is _unneccessary_ and is simply a quick-start method:
```sh
aws ecr delete-repository --repository-name cattlepoint-database; aws ecr create-repository --repository-name cattlepoint-database --query 'repository.repositoryUri' --output text && podman login -u AWS -p $(aws ecr get-login-password) $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text) && podman rm -f cattlepoint-database && podman build -t $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text):latest database/. && podman push $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text):latest && podman image rm $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text):latest && podman run -d --name cattlepoint-database -p 3306:3306 $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text):latest

aws ecr delete-repository --repository-name cattlepoint-backend; aws ecr create-repository --repository-name cattlepoint-backend --query 'repository.repositoryUri' --output text && podman login -u AWS -p $(aws ecr get-login-password) $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text) && podman rm -f cattlepoint-backend && podman build -t $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text):latest backend/. && podman push $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text):latest &&  podman image rm $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text):latest && podman run -d --name cattlepoint-backend -p 8000:8000 $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text):latest &&  sleep 3 && curl 'http://localhost:8000/healthcheck'

aws ecr delete-repository --repository-name cattlepoint-frontend; aws ecr create-repository --repository-name cattlepoint-frontend --query 'repository.repositoryUri' --output text && podman login -u AWS -p $(aws ecr get-login-password) $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text) && podman rm -f cattlepoint-frontend && podman build -t $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text):latest frontend/. &&  podman push $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text):latest && podman image rm $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text):latest && podman run -d --name cattlepoint-frontend -p 8080:80 $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text):latest &&  sleep 3 && curl -s http://localhost:8080 |grep Bulletin

podman build -t seed:latest seed/. && podman run --rm --name cattlepoint-seed seed:latest && curl -s http://localhost:8000/bulletins
```

#### This section creates the database container, pushes it to the ECR repository, and runs the container
* Create the ECR repository for the database container:
```sh
aws ecr create-repository --repository-name cattlepoint-database --query 'repository.repositoryUri' --output text
```
* Expected output:
```sh
***.dkr.ecr.us-east-1.amazonaws.com/cattlepoint-database
```
* Log podman into the new database container ECR repository:
```sh
podman login -u AWS -p $(aws ecr get-login-password) $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text)
```
* Expected output:
```sh
Login Succeeded!
```
* Create the Docker container for the database container using the supplied database Dockerfile:
```sh
podman build -t $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text):latest database/.
```
* Push the database container to the ECR repository:
```sh
podman push $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text):latest
```
* Delete the local copy of the database container image:
```sh
podman image rm $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text):latest
```
* Start the database container using the ECR repository:
```sh
podman run -d --name cattlepoint-database -p 3306:3306 $(aws ecr describe-repositories --repository-names cattlepoint-database --query 'repositories[0].repositoryUri' --output text):latest
```
* Check if the container is running:
```sh
podman ps --noheading --format '{{.ID}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}'
```
* Expected output (container id and date will vary):
```sh
7446dd07b960    mariadbd        2025-05-22 11:42:40.094091818 -0500 CDT Up About a minute       0.0.0.0:3306->3306/tcp  cattlepoint-database
```
* Connect to the database and confirm it is running:
```sh
podman run --rm -it --network container:cattlepoint-database mariadb \
  mariadb -h127.0.0.1 -P3306 -uroot -prootpassword
show databases;
exit;
```
* Expected output:
```sh
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 5
Server version: 11.7.2-MariaDB-ubu2404 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| appdb              |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.002 sec)

MariaDB [(none)]> ^DBye
```

#### This section creates the backend container, pushes it to the ECR repository, and runs the container
* Create the ECR repository for the api container:
```sh
aws ecr create-repository --repository-name cattlepoint-backend --query 'repository.repositoryUri' --output text
```
* Expected output:
```sh
***.dkr.ecr.us-east-1.amazonaws.com/cattlepoint-backend
```
* Log podman into the new backend container ECR repository:
```sh
podman login -u AWS -p $(aws ecr get-login-password) $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text)
```
* Expected output:
```sh
Login Succeeded!
```
* Create the Docker container for the backend container using the supplied backend Dockerfile:
```sh
podman build -t $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text):latest backend/.
```
* Push the backend container to the ECR repository:
```sh
podman push $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text):latest
```
* Delete the local copy of the backend container image:
```sh
podman image rm $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text):latest
```
* Start the backend container using the ECR repository:
```sh
podman run -d --name cattlepoint-backend -p 8000:8000 $(aws ecr describe-repositories --repository-names cattlepoint-backend --query 'repositories[0].repositoryUri' --output text):latest
```
* Check if the container is running:
```sh
podman ps --noheading --format '{{.ID}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}'
```
* Expected output (container id and date will vary):
```sh
1f703fbcb298    python app.py   2025-05-22 12:38:48.077546127 -0500 CDT Up About an hour        0.0.0.0:8000->8000/tcp  cattlepoint-backend
```
* Connect to the backend and confirm it is running:
```sh
curl 'http://localhost:8000/healthcheck' && curl 'http://localhost:8000/bulletins'
```
* Expected output:
```sh
% curl 'http://localhost:8000/healthcheck' && curl 'http://localhost:8000/bulletins'
{"status":"ok"}
[]
```



#### This section creates the frontend container, pushes it to the ECR repository, and runs the container
* Create the ECR repository for the api container:
```sh
aws ecr create-repository --repository-name cattlepoint-frontend --query 'repository.repositoryUri' --output text
```
* Expected output:
```sh
***.dkr.ecr.us-east-1.amazonaws.com/cattlepoint-frontend
```
* Log podman into the new frontend container ECR repository:
```sh
podman login -u AWS -p $(aws ecr get-login-password) $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text)
```
* Expected output:
```sh
Login Succeeded!
```
* Create the Docker container for the frontend container using the supplied frontend Dockerfile:
```sh
podman build -t $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text):latest frontend/.
```
* Push the frontend container to the ECR repository:
```sh
podman push $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text):latest
```
* Delete the local copy of the frontend container image:
```sh
podman image rm $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text):latest
```
* Start the frontend container using the ECR repository:
```sh
podman run -d --name cattlepoint-frontend -p 8080:80 $(aws ecr describe-repositories --repository-names cattlepoint-frontend --query 'repositories[0].repositoryUri' --output text):latest
```
* Check if the container is running:
```sh
podman ps --noheading --format '{{.ID}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}'
```
* Expected output (container id and date will vary):
```sh
3291134fd3b9    nginx -g daemon o...    2025-05-22 12:14:39.778088765 -0500 CDT Up 5 seconds    0.0.0.0:8080->80/tcp    cattlepoint-frontend
```
* Connect to the frontend and confirm it is running:
```sh
curl -s http://localhost:8080 |grep Bulletin
open http://localhost:8080
```
* Expected output:
```sh
% curl -s http://localhost:8080 |grep Bulletin
        <title>Cattle Sales Bulletin</title>
            function fetchBulletins() {
                    fetchBulletins();
            fetchBulletins();
```

#### This section creates a seed container to populate the database and runs the container
* Create the Docker container for the seed container using the supplied seed Dockerfile:
```sh
podman build -t seed:latest seed/.
```
* Start the frontend container using the ECR repository:
```sh
podman run --rm --name cattlepoint-seed seed:latest
```
* Expected output (container id and date will vary):
```sh
% podman run --rm --name cattlepoint-seed seed:latest
⏳ waiting for host.containers.internal …
🚀 seeding appdb
✅ done
```
* Check if the seed container ran:
```sh
curl -s http://localhost:8000/bulletins
```
* Expected output:
```sh
% curl -s http://localhost:8000/bulletins
[{"id":10,"location":"TX","price":"1200.00","title":"Longhorn yearling"},{"id":9,"location":"TX","price":"1900.00","title":"Brangus bred heifer"},{"id":8,"location":"CO","price":"2400.00","title":"Gelbvieh bull"},{"id":7,"location":"SD","price":"3200.00","title":"Red Angus cow-calf pair"},{"id":6,"location":"MO","price":"1700.00","title":"Limousin steer"},{"id":5,"location":"NE","price":"1550.00","title":"Simmental heifer"},{"id":4,"location":"TX","price":"1600.00","title":"Brahman cow"},{"id":3,"location":"KS","price":"2500.00","title":"Charolais bull"},{"id":2,"location":"OK","price":"1500.00","title":"Hereford heifer"},{"id":1,"location":"TX","price":"1800.00","title":"Angus steer"}]
```

#### This section verifies the app works in the browser
* Open the cattlepoint website:
```sh
open 'http://localhost:8080'
```
* Visually verify that there are cattle sales listed
* Add a new cattle sale:
```text
login with user: admin
login with password: admin
click Login
Title: midnight bull
Price: 5000
Location: CA
click Add
```
* Visually verify that the new midnight bull is present in the list

## 10 points – Deploy an Amazon EKS cluster
### In this section you will create an Amazon EKS cluster using eksctl
* Verify AWS credentials are working:
```sh
export AWS_PROFILE=eruser315
aws sts get-caller-identity
```
* Visually verify in output: arn:aws:iam::***:user/eruser315
* Create the EKS cluster using eksctl:
```sh
eksctl create cluster -f cluster.yaml
```
* Wait for the cluster to be created. This may take a while.
* Expected output:
```sh
2025-05-22 11:34:03 [ℹ]  eksctl version 0.208.0-dev+bcdd6ecb0.2025-05-12T20:08:12Z
....status output here....
2025-05-22 11:34:04 [ℹ]  creating EKS cluster "cattlepoint-cluster" in "us-east-1" region with Fargate profile and managed nodes
....status output here....
2025-05-22 11:56:20 [✔]  EKS cluster "cattlepoint-cluster" in "us-east-1" region is ready
```
* Verify the cluster is created and running:
```sh
kubectl get nodes
kubectl get pods --all-namespaces
kubectl describe svc
```
* Expected output (ips and names will vary):
```sh
% kubectl get nodes
NAME                              STATUS   ROLES    AGE     VERSION
ip-192-168-108-233.ec2.internal   Ready    <none>   8m9s    v1.31.7-eks-473151a
ip-192-168-87-152.ec2.internal    Ready    <none>   8m19s   v1.31.7-eks-473151a

% kubectl get pods --all-namespaces
NAMESPACE           NAME                                                              READY   STATUS    RESTARTS   AGE
amazon-cloudwatch   amazon-cloudwatch-observability-controller-manager-779549c8n92z   1/1     Running   0          3m39s
amazon-cloudwatch   cloudwatch-agent-gxv74                                            1/1     Running   0          3m34s
amazon-cloudwatch   cloudwatch-agent-t6z4k                                            1/1     Running   0          3m33s
amazon-cloudwatch   fluent-bit-btnbb                                                  1/1     Running   0          3m39s
amazon-cloudwatch   fluent-bit-nwbj8                                                  1/1     Running   0          3m39s
kube-system         aws-node-g42n6                                                    2/2     Running   0          8m14s
kube-system         aws-node-jnccw                                                    2/2     Running   0          8m24s
kube-system         coredns-54fb474b58-fb765                                          1/1     Running   0          16m
kube-system         coredns-54fb474b58-rckwg                                          1/1     Running   0          16m
kube-system         ebs-csi-controller-5bc6c8f8b7-97cgv                               6/6     Running   0          4m45s
kube-system         ebs-csi-controller-5bc6c8f8b7-dtxkv                               6/6     Running   0          4m45s
kube-system         ebs-csi-node-pp7zr                                                3/3     Running   0          4m45s
kube-system         ebs-csi-node-v82j6                                                3/3     Running   0          4m45s
kube-system         kube-proxy-b45q5                                                  1/1     Running   0          8m24s
kube-system         kube-proxy-m5zrs                                                  1/1     Running   0          8m14s
kube-system         metrics-server-7ccfcc47f5-mbvvn                                   1/1     Running   0          16m
kube-system         metrics-server-7ccfcc47f5-z2clz                                   1/1     Running   0          16m

% kubectl describe svc
Name:                     kubernetes
Namespace:                default
Labels:                   component=apiserver
                          provider=kubernetes
Annotations:              <none>
Selector:                 <none>
Type:                     ClusterIP
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.100.0.1
IPs:                      10.100.0.1
Port:                     https  443/TCP
TargetPort:               443/TCP
Endpoints:                192.168.105.179:443,192.168.73.71:443
Session Affinity:         None
Internal Traffic Policy:  Cluster
Events:                   <none>
```
### In this section you will delete the EKS cluster and the ECR repositories
* Delete the EKS cluster:
```sh
% eksctl delete cluster -f cluster.yaml
```
* Expected output (date will vary):
```sh
2025-05-22 11:30:07 [ℹ]  deleting EKS cluster "cattlepoint-cluster"
....status output here....
2025-05-22 11:30:45 [✔]  all cluster resources were deleted
```

## 40 points – Deploy your application, including a backend database
### In this section we will deploy the previous containers in EKS
* For this section, you will need to have cloned the repository to your local machine.  You can do this by running the following command in your terminal:
```sh
gh repo clone cattlepoint/cattlepoint-aer3-week2
```
* For this section, make sure you are in the repository directory:
```sh
cd cattlepoint-aer3-week2
```
* Verify AWS credentials are working:
```sh
export AWS_PROFILE=eruser315
aws sts get-caller-identity
```
* Visually verify in output: arn:aws:iam::***:user/eruser315
* Create the EKS cluster using eksctl:
```sh
eksctl create cluster -f cluster-arm64.yaml
```
* Wait for the cluster to be created. This may take a while.
* Expected output:
```sh
% eksctl create cluster -f cluster-arm64.yaml
2025-05-22 18:06:32 [ℹ]  eksctl version 0.208.0-dev+bcdd6ecb0.2025-05-12T20:08:12Z
2025-05-22 18:06:32 [ℹ]  using region us-east-1
....status output here....
2025-05-22 18:06:32 [ℹ]  using Kubernetes version 1.32
2025-05-22 18:06:32 [ℹ]  creating EKS cluster "cattlepoint-cluster" in "us-east-1" region with managed nodes
....status output here....
2025-05-22 18:26:06 [✔]  EKS cluster "cattlepoint-cluster" in "us-east-1" region is ready
```
* Verify the cluster is created and running:
```sh
kubectl get nodes,pods,svc
```
* Expected output (ips and names will vary):
```sh
% kubectl get nodes,pods,svc
NAME                                   STATUS   ROLES    AGE     VERSION
node/ip-192-168-122-158.ec2.internal   Ready    <none>   6m35s   v1.32.3-eks-473151a
node/ip-192-168-89-237.ec2.internal    Ready    <none>   7m38s   v1.32.3-eks-473151a
node/ip-192-168-91-109.ec2.internal    Ready    <none>   7m36s   v1.32.3-eks-473151a

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   16m
```
* Create a variable with the AWS ACCOUNT_ID:
```sh
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```
* Apply the Kubernetes template cattlepoint-deployment.v1.yaml
```sh
cat cattlepoint-deployment.v1.yaml | envsubst | kubectl apply -f -
```
* Expected output:
```sh
% cat cattlepoint-deployment.v1.yaml | envsubst | kubectl apply -f -
persistentvolumeclaim/mariadb-pvc created
deployment.apps/cattlepoint-database created
service/cattlepoint-database created
deployment.apps/cattlepoint-backend created
service/cattlepoint-backend created
deployment.apps/cattlepoint-frontend created
service/cattlepoint-frontend created
```
* Check if the pods are running:
```sh
kubectl get pods
```
* Expected output (container id and date will vary):
```sh
% kubectl get pods
NAME                                    READY   STATUS    RESTARTS   AGE
cattlepoint-backend-79fd6ff5c-48564     1/1     Running   0          96s
cattlepoint-backend-79fd6ff5c-t9sg9     1/1     Running   0          96s
cattlepoint-database-859bf7f4d-jxjsj    1/1     Running   0          96s
cattlepoint-frontend-59bcfdd9dd-68lvs   1/1     Running   0          96s
cattlepoint-frontend-59bcfdd9dd-dkvpq   1/1     Running   0          96s
```
* Obtain the URL of the frontend service:
```sh
kubectl get svc cattlepoint-frontend \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```
* Expected output (container id and date will vary):
```sh
% kubectl get svc cattlepoint-frontend \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
afec1d935cd1d4c39b3ffd2d3e4755e1-1738021288.us-east-1.elb.amazonaws.com
```
* Test the cattlepoint website:
```sh
curl -s "http://$(kubectl get svc cattlepoint-frontend \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')" | grep Bulletin
```
* Expected output:
```sh
% curl -s "http://$(kubectl get svc cattlepoint-frontend \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')" | grep Bulletin
        <title>Cattle Sales Bulletin</title>
            function fetchBulletins() {
                    fetchBulletins();
            fetchBulletins();
```
* Open the cattlepoint website:
```sh
open "http://$(kubectl get svc cattlepoint-frontend \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')"
```
* Visually verify that there are cattle sales listed
* Add a new cattle sale:
```text
login with user: admin
login with password: admin
click Login
Title: midnight bull
Price: 5000
Location: CA
click Add
```
* Visually verify that the new midnight bull is present in the list


## 10 points – Test updating your application using rolling updates
