# Terraform Deployer

Terraform Deployer is a tool designed to simplify the deployment of infrastructure using Terraform. It provides an easy way to configure and manage the deployment process, allowing you to automate and streamline your infrastructure provisioning.

## Prerequisites

Before using Terraform Deployer, ensure that you have the following dependencies installed:

- Docker
- Docker Compose

## Configuration

To configure the Terraform Deployer tool, you need to create a `docker-compose.yaml` file with the following contents:

``` yaml
version: '3.8'

services:
    deploy:
        image: tf-deployer:latest
        volumes:
            - ./.envfile.json:/opt/deployer/.envfile.json
            - ./.envsecrets.json:/opt/deployer/.envsecrets.json
            - ./infra/config/env.tfvars:/opt/deployer/vars.tfvars
            - ./infra:/opt/deployer/infra
```


The configuration is done through two JSON files: `.envfile.json` and `.envsecrets.json`:

### `.envfile.json`

The `.envfile.json` file contains the configuration parameters for the Terraform Deployer tool. The following parameters are supported:

- `PIPELINE_NAME`: The name of the deployment pipeline.
- `SKIP_APPLY`: A boolean value indicating whether to skip the `terraform apply` step. Set it to `true` to skip the apply step.
- `EXPECT_SECRETS_FOR`: An array of provider names for which secrets are expected. Supported providers are "AWS".
- `TF_STATE_LOCATION`: The location of the Terraform state file. Use the format `s3://{bucket}/` to specify an S3 bucket location.
- `TF_STATE_LOADER`: The loader type for the Terraform state. Supported loader types are "AWS_S3".
- `TERRAFORM_VARS_FILE`: The path to the Terraform variables file.
- `TERRAFORM_CHDIR`: The working directory for Terraform commands.

Here is an example `.envfile.json`:

``` json
{
"PIPELINE_NAME": "my-pipeline",
"SKIP_APPLY": true,
"EXPECT_SECRETS_FOR": ["AWS"],
"TF_STATE_LOCATION": "s3://{bucket}/",
"TF_STATE_LOADER": "AWS_S3"
}
```
### `.envsecrets.json`

The `.envsecrets.json` file contains the secrets required by the Terraform Deployer tool. The following secrets are expected for both the "AWS" provider and the "AWS_S3" state loader:

- `ACCESS_KEY`: The access key for the AWS account.
- `SECRET_ACCESS_KEY`: The secret access key for the AWS account.

**Note:** AWS support on machine level configuration is still in development.

## Usage

Before using Terraform Deployer, you need to build the `tf-deployer` image. Run the following command in the host machine:

```bash
make build
```

To use the Terraform Deployer tool, follow these steps:
- Create the docker-compose.yaml file with the appropriate configuration, as described above.
- Create the .envfile.json and .envsecrets.json files with the required parameters and secrets, as described above.
- Open a terminal or command prompt and navigate to the directory where the docker-compose.yaml file is located.
- Run the following command to start the deployment:
``` bash
docker-compose up
```