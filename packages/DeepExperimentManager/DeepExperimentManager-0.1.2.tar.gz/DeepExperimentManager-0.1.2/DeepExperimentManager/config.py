import yaml

def load_config(config_path):
    """
    Loads the configuration from a YAML file.

    Args:
        config_path (str): The path to the YAML configuration file.

    Returns:
        dict: A dictionary containing the loaded configuration.
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config
