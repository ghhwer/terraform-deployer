import os
from .aws_loader import StateFileLoaderS3

def execute_terraform(env_opts):
    # Assuming you have the Terraform command available in the system path
    # Modify these commands as per your requirement
    var_file = env_opts['TERRAFORM_VARS_FILE']
    chdir = env_opts['TERRAFORM_CHDIR']
    destroy = env_opts.get('DESTROY', False)
    init_command = f'terraform -chdir={chdir} init'
    plan_command = f'terraform -chdir={chdir} plan -var-file="{var_file}"'
    apply_command = f'terraform -chdir={chdir} apply -var-file="{var_file}" -auto-approve'

    # Initialize Terraform
    print('Initializing Terraform...')
    exit_code = os.system(init_command)
    if exit_code != 0:
        raise RuntimeError('Terraform initialization failed.')

    # Generate Terraform plan
    print('Generating Terraform plan...')
    exit_code = os.system(plan_command)
    if exit_code != 0:
        raise RuntimeError('Terraform plan generation failed.')

    if(env_opts.get('SKIP_APPLY', False) == False or destroy == True):
        print('Executing Terraform apply...')
        # Execute Terraform apply
        exit_code = os.system(apply_command)
        if exit_code == 0:
            print('Terraform steps executed successfully.')
        else:
            raise RuntimeError('Terraform execution failed.')
    else:
        print('Terraform apply skipped...')
    if destroy == True:
        # Destroy
        print('Destroying...')
        destroy_command = f'terraform -chdir={chdir} destroy -var-file="{var_file}" -auto-approve'
        exit_code = os.system(destroy_command)
        if exit_code == 0:
            print('Terraform steps executed successfully.')
        else:
            raise RuntimeError('Terraform execution failed.')

class TfLoader():
    def __init__(self, options, credentials):
        # Options
        self.options = options
        self.credentials = credentials
        
        # Options parse
        terraform_vars_path = self.options.get('TERRAFORM_VARS_FILE', '/opt/deployer/vars.tfvars')
        terraform_ch_dir = self.options.get('TERRAFORM_CHDIR', '/opt/deployer/infra')
        self.options['TERRAFORM_VARS_FILE'] = terraform_vars_path
        self.options['TERRAFORM_CHDIR'] = terraform_ch_dir

        self.state_file_loader = self.solve_state_file_loader()
    
    def run_terraform(self,):
        print('Syncing with state file loader')
        self.state_file_loader.get_file()
        # Execute Terraform
        try:
            execute_terraform(self.options)
        except RuntimeError as e:
            print('There was an error executing terraform, syncing tf_state anyways...')
        self.state_file_loader.put_file()

    def solve_state_file_loader(self):
        tf_state_loader = self.options.get('TF_STATE_LOADER')
        if tf_state_loader  == 'AWS_S3':
            return StateFileLoaderS3(self.options, self.credentials)
        else:
            raise ValueError(f'Error while parsing "TF_STATE_LOADER": {tf_state_loader} is not supported!')