import os


def env_to_bool(env_var_name):
    env_var = os.environ.get(env_var_name, True)
    return env_var in ('true', 'y', '1', 'True')


WAIT_FOR_HOST = env_to_bool('WAIT_FOR_HOST')
