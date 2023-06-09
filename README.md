# Terraform Deployer

Terraform Deployer is a tool designed to simplify the deployment of infrastructure using Terraform. It provides an easy way to configure and manage the deployment process, allowing you to automate and streamline your infrastructure provisioning.

## Prerequisites

Before using Terraform Deployer, ensure that you have the following dependencies installed:

- Docker
- Docker Compose
- Make

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

## `The basic project structure`
```
my-project
|- app
    |--"Whatever additional files your project needs"
|- infra
    |--...
    |--main.tf
    |--...
|- docker-compose.yaml 
|- .envfile.json
|- .envsecrets.json
|- .artifacts.json (optional)
```

## `Configuration files`
The configuration is done through JSON files: 
- `.envfile.json`
    -  This file allows the user to specify configurations regarding the deployment process.
- `.envsecrets.json`
    -  This file allows the user to specify sensitive information to the deployment process.
- `.artifacts.json`
    - This file allows the user to specify options as to create 'artifacts' (packages) to be pre-built.

### `Configuring the .envfile.json`

The `.envfile.json` file contains the configuration parameters for the Terraform Deployer tool. The following parameters are supported:

- `PIPELINE_NAME`: The name of the deployment pipeline.
- `SKIP_APPLY`: A boolean value indicating whether to skip the `terraform apply` step. Set it to `true` to skip the apply step.
- `EXPECT_SECRETS_FOR`: An array of provider names for which secrets are expected. Supported providers are "AWS".
- `TF_STATE_LOCATION`: The location of the Terraform state file. Use the format `s3://{bucket}/` to specify an S3 bucket location.
- `TF_STATE_LOADER`: The loader type for the Terraform state. Supported loader types are "AWS_S3".
- `TERRAFORM_VARS_FILE`: The path to the Terraform variables file. 
    -   (defaults to /opt/deployer/vars.tfvars)
- `TERRAFORM_CHDIR`: The working directory for Terraform commands. 
    -   (defaults to /opt/deployer/infra)

Here is an example `.envfile.json`:

``` json
{
"PIPELINE_NAME": "my-pipeline",
"SKIP_APPLY": true,
"EXPECT_SECRETS_FOR": ["AWS"],
"TF_STATE_LOCATION": "s3://{bucket}/",
"TF_STATE_LOADER": "AWS_S3",
"AWS_REGION": "sa-east-1"
}
```
### `Configuring the .envsecrets.json`

The `.envsecrets.json` file contains the secrets required by the Terraform Deployer tool. The following secrets are expected for both the "AWS" provider and the "AWS_S3" state loader:

- `ACCESS_KEY`: The access key for the AWS account.
- `SECRET_ACCESS_KEY`: The secret access key for the AWS account.

**Note:** AWS support on machine level (AWS CLI) configuration is still in development.

### `Configuring the .artifacts.json`

The `.envsecrets.json` file contains the instructions to create/build artifact files, they may be a zip folder or other build/test sub-module in your deploy pipeline.

(Currently supporting .zip artifacts only.)

The following parameters are supported at the moment:

- `ZIP_ARTIFACTS`: A list of defined folder/target to be created before the terraforming process begin.
    - Example: 
    ``` json
    {
        "ZIP_ARTIFACTS":[
            {
                "source": "/opt/deployer/artifacts/my-app",
                "target": "/opt/deployer/infra/dist/my-app.zip",
                "include_root": false
            }
        ]
    }
    ```

- `GIT_ARTIFACTS`: A list of defined folder/target to be created before the terraforming process begin.
    - Example: 
    ``` json
    {
        "GIT_ARTIFACTS":[
            {
                "source": "https://github.com/your-user/repo/",
                "branch": "main",
                "target": "/opt/deployer/infra/dist/my-repo.zip",
                "include_root": false
            },
            {
                "source": "user@github.com:your-user/repo-2.git",
                "branch": "main",
                "target": "/opt/deployer/infra/dist/my-repo-2-no-zip",
            },
        ]
    }
    ```
**Note:** When using SSH, make sure to map the keys to the running container's root user (/root/.ssh).

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

The Terraform Deployer tool will read the configuration files and initiate the deployment process based on the provided parameters.

# License
This project is licensed under the MIT License.

# Contributions
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please create an issue or submit a pull request on the GitHub repository.