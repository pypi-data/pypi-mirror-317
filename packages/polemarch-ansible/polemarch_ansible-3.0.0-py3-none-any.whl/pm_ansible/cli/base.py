import argparse


def get_parser():
    """
    Base ArgumentParser for all CLI handlers in polemarch-ansible.
    """
    return argparse.ArgumentParser(
        prog='Polemarch-Ansible',
        description='%(prog)s CLI wrapper for Ansible.',
        conflict_handler='resolve',
    )
