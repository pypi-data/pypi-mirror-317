import os
from string import Template

from dotenv import find_dotenv, load_dotenv, dotenv_values


def generate_env_file(load_global=False, load_local=False):
    #lazyenv_path = os.path.join(os.path.dirname(__file__), 'dymenv.py')
    lazyenv_path = os.path.dirname(__file__)
    
    env_vars = {}

    if load_local:
        # Load environment variables specified in the .env file
        local_env_path = find_dotenv()
        load_dotenv(local_env_path)
        env_vars = dotenv_values(local_env_path)

    if load_global:
        # Load environment variables from the system
        for key in os.environ:
            env_vars[key] = os.getenv(key)

    # Generate the `env.py` file with environment variable names from template
    with open(os.path.join(lazyenv_path, 'env.template'), 'r') as templ_file:
        template = templ_file.read()

    variable_names_block = '\n'.join(f"{key} = os.getenv('{key}')"
                                for key in env_vars)
    templ_str = Template(template)
    file_content = templ_str.substitute(variable_names=variable_names_block)
    
    with open(os.path.join(lazyenv_path, 'env.py'), 'w') as env_file:
        env_file.write(file_content)