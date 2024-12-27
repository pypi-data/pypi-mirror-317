import os
import sys


def update_warnings(value='false'):
    default_warnings = [
        'ANSIBLE_ACTION_WARNINGS',
        'ANSIBLE_SYSTEM_WARNINGS',
        'ANSIBLE_DEPRECATION_WARNINGS',
        'ANSIBLE_LOCALHOST_WARNING',
        'ANSIBLE_COMMAND_WARNINGS',
    ]
    for var_name in default_warnings:
        os.environ[var_name] = value


def main(args=sys.argv):
    """
    Main entry point for pm_ansible.cli
    Example usage:
      python -m pm_ansible reference --indent
      python -m pm_ansible ansible -m ping -i localhost, --connection local
    """
    if len(args) < 2:  # nocv
        print("Usage: pm-ansible <handler> [options]")
        sys.exit(1)

    # Reduce Ansible warnings unless needed
    update_warnings()

    if args[1] == 'reference':
        from . import reference
        reference.handler(args[2:])
    elif args[1] == 'modules':
        from . import modules
        modules.handler(args[2:])
    elif args[1] == 'inventory_parser':
        from . import inventory_parser
        inventory_parser.handler(args[2:])
    elif args[1] == 'config':
        from . import config
        config.handler(args[2:])
    else:
        from . import execute
        execute.handler(args[1:])
