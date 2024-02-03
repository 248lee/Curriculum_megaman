import os
import sys

def is_executed_locally():
    """
    Checks if the script is being executed locally or via SSH.
    Returns True if local, False if via SSH.
    """
    return os.name == 'posix' and 'SSH_CLIENT' not in os.environ

def main():
    if is_executed_locally():
        print("Script executed locally.")
    else:
        print("Script executed via SSH.")

if __name__ == '__main__':
    main()