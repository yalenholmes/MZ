"""
Command-line argument parsing for MZ
"""
import argparse

def parse_args():
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments object
    """
    parser = argparse.ArgumentParser(
        prog='MZ',
        description='MZ - Personal AI Task Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python monozukuri.py                    # Normal mode
  python monozukuri.py --debug            # Debug mode
  python monozukuri.py --config my.yaml  # Custom config
  
For more information, visit: https://github.com/yalenholmes/MZ
        """
    )
    
    # Add arguments
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging (overrides config file)'
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='MZ v0.3.0'
    )
    
    return parser.parse_args()