Wrapper for Ansible cli.
========================

Compatibility
=============

- Versions 2.2.x are the last to support Ansible 2.5 - 2.9.
- Version 3.0.x supports ansible-core 2.11 to 2.17. It can also work with Ansible 2.10, but it must be installed manually.

Usage
=====

*  `pm-execute [ansible command name] [args]` - calls any ansible cli tool.
*  `pm-cli-reference [ansible command name,...] [--exclude key]` -
    output cli keys for command. Default - all. Exclude keys by names (support many).
    Now support output only 'ansible', 'ansible-playbook' and
    'ansible-galaxy'.
*  `pm-ansible [reference/ansible_command]` - run as module.
   For output reference use 'reference', or full ansible command.
*  `pm-ansible [--detail] [--get]` -
    Output modules reference. 

Contribution
============

We use `tox` for tests and deploy. Just run `tox -e py36-coverage,py37-install,flake`
for full tests with coverage output.
