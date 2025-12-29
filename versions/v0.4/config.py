# config.py
"""
Configuration management for MZ
"""
import yaml

def load_config(config_path="config.yaml"):
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file (default: config.yaml)
    
    Returns:
        Dictionary with configuration settings
    """
    # Try to load the config file
    try:
        # Open the file for reading
        with open(config_path, 'r') as f:
            # Parse the YAML into a Python dictionary
            config = yaml.safe_load(f)

        # If we got here, it worked!
        return config
    
    except FileNotFoundError:
        # Config file doesn't exist
        print(f"ERROR: Config file not found at {config_path}")
        exit(1)

    except yaml.YAMLError as e:
        # YAML has syntax errors
        print(f"ERROR: Invalid YAML in config file: {e}")
        exit(1)