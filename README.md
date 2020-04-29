[![CircleCI](https://circleci.com/gh/nexton-labs/flask-starter/tree/microservices.svg?style=svg)](https://circleci.com/gh/nexton-labs/flask-starter/tree/microservices)
# Flask Starter

This is a Python template developed using Flask and a Micro-services architecture.

There are 3 micro-services:
 * candidates_backend - Handles all the operations related to users candidates
 * users_backend - Handles application users
 * frontend - Application user interface

## Run the application locally

Within each micro-service you will find another readme file to run each service using python commands.
There is also another option to have the application up and running using docker compose.

### DB container build
Candidates and users micro-services are having their own DB container in this example.
To build those and have them available you can use docker compose.

    cd candidates_backend
    docker-compose build db
The same command can be applied to the Users micro-service

### Server build
Each micro-service is having a `server` docker compose service definition
    
    cd candidates_backend
    docker-compose build server

### Run
To run each service, just run

    cd candidates_backend
    docker-compose run server
    
### Local Kubernetes Cluster
Docker compose can be nice for local development of one of the micro-services.
But if you want to bring up the entire app and need to change multiple micro-services it would be better to setup the 
application in a local kubernetes cluster.

`kubernetes` directory within the project is having a `local` and `dev` directory within it. `dev` directory is being used
for `AWS` deployment.

Let's setup our local cluster using `minikube`

    brew install minikube
    
If you are not using macOS, you can check the minikube installation instructions [here](https://kubernetes.io/docs/tasks/tools/install-minikube/).
When `minikube` installation is completed, start the cluster with:

    minikube start
    
To deploy the application containers to our local cluster we need to first create a namespace.

    cd kubernetes
    kubectl apply -f namespace.yaml  

Local `kubernetes` configuration files are having the image pull configuration as never pull.
This will instruct `kuberenetes` to search for the images in the local docker registry.
`minikube` is using it's local docker daemon, so is not going to find the images we build in the previous steps.
To switch your docker daemon to use the `minikube` one do:

    eval $(minikube docker-env)

After that build the required images again on the same terminal.

Finally, to deploy the containers into the cluster run:

    cd kuberenetes/local
    kubectl apply -f . --recursive

To get the URL to access the application

    minikube service frontend-service -n flask-starter --url

## Deploy to AWS EKS from ECR via CircleCI 2.0

### Cluster creation with Terraform
To deploy the application into AWS Elastic Kubernetes Service(EKS) we first need to create the cluster.
To do that, we have some terraform scripts on `terraform_setup` directory.
To be able to use these terraform scripts you need to have `AWS CLI` installed and configured:

    $ aws configure
    AWS Access Key ID [None]: <YOUR_AWS_ACCESS_KEY_ID>
    AWS Secret Access Key [None]: <YOUR_AWS_SECRET_ACCESS_KEY>
    Default region name [None]: <YOUR_AWS_REGION>
    Default output format [None]: json

This enables Terraform access to the configuration file and performs operations on your behalf with these security credentials.

After you've done this, initialize your Terraform workspace, which will download the provider and initialize it with the values provided in the `terraform.tfvars` file.

    cd terraform_setup
    terraform init
    
Then to provide the `EKS` cluster 

    terraform plan
    terraform apply

Plan command is to verify if the resources that are going to be created is what you were expecting.
`terraform destroy` can be used to delete the created assets.

### kubectl configuration to manage the cluster

To switch your `kubectl` configuration to handle the `EKS` cluster instead of the previous `minikube` one run:

    aws eks update-kubeconfig --name flask-starter-cluster

### CircleCI configuration
The `CircleCI` script being used to deploy each micro-service in the EKS cluster is also creating the ECR repository if it's not there.
As this project is using a mono-repo strategy the build is using a script to detect to which directory a commit was done to build just the micro-service
that is receiving changes.

To add a new micro-service to the project and get it built, you need to add it to the script parameters under the section:

    # A parameter per micro-service
    candidates_backend:
        type: boolean
        default: false

Then in the `workflows` section create a new workflow for the newly created service.

Finally, the following [environment variables](https://circleci.com/docs/2.0/env-vars/#setting-an-environment-variable-in-a-project) must be set for the project on CircleCI via the project settings page, before the project can be built successfully.

| Variable                       | Description                                               |
| ------------------------------ | --------------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`            | Used by the AWS CLI                                       |
| `AWS_SECRET_ACCESS_KEY `       | Used by the AWS CLI                                       |
| `AWS_DEFAULT_REGION`           | Used by the AWS CLI. Example value: "us-east-1" (Please make sure the specified region is supported by the Fargate launch type)                          |
| `AWS_ACCOUNT_ID`               | AWS account id. This information is required for deployment.                                   |
| `AWS_ECR_ACCOUNT_URL`          | URL of your AWS Elastic Container Registry (ECR)                             |    
| `CIRCLE_TOKEN`                 | Personal [CircleCI token](https://circleci.com/docs/2.0/managing-api-tokens/)                             |
