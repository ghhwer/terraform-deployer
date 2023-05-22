from commons.parser import parse_env_file
from commons.checker import options_present

from credentials_providers import Credentials
from tf_loader import TfLoader

def main():
    # File
    env_path = '/opt/deployer/.envfile.json'
    env_secrets = '/opt/deployer/.envsecrets.json'
    # Get env opts
    env_opts = parse_env_file(env_path)
    env_secrets = parse_env_file(env_secrets)
    
    # Merge the opts
    env_opts.update(env_secrets)
    
    # Check obligatory base parameters
    options_present([
        'PIPELINE_NAME',
        'EXPECT_SECRETS_FOR',
        'TF_STATE_LOCATION',
        'TF_STATE_LOADER'
    ], env_opts)

    # Load credentials and tf loader
    credentials = Credentials(env_opts)
    tf_loader = TfLoader(env_opts, credentials)
    tf_loader.run_terraform()

if __name__ == '__main__':
    main()