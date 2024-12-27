import os
import sys
import json
from contextlib import redirect_stderr, redirect_stdout

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager


def parse_inventory(path):
    """
    Parses inventory using Ansible's InventoryManager and prints results as JSON.
    """
    # Suppress warnings or extra logs from Ansible
    with open(os.devnull, 'w') as fd, redirect_stderr(fd), redirect_stdout(fd):
        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources=path)

    data = {
        'groups': [],
        'hosts': [],
        'vars': {},
    }

    for group in inventory.groups:
        if group == 'ungrouped':
            continue
        elif group == 'all':
            data['vars'] = inventory.groups[group].vars
            continue
        group_data = {
            'name': group,
            'hosts': [],
            'groups': [],
            'vars': inventory.groups[group].vars,
        }
        for host in inventory.groups[group].hosts:
            group_data['hosts'].append(host.name)
        for child_group in inventory.groups[group].child_groups:
            group_data['groups'].append(child_group.name)
        data['groups'].append(group_data)

    for host in inventory.hosts:
        host_data = {
            'name': host,
            'vars': dict(inventory.hosts[host].vars),
        }
        # Some keys may not exist in newer versions, so pop with default
        host_data['vars'].pop('inventory_file', None)
        host_data['vars'].pop('inventory_dir', None)
        data['hosts'].append(host_data)

    json.dump(data, sys.stdout, indent=4)
    sys.stdout.flush()


def handler(args=sys.argv[1:]):
    if not args:  # nocv
        print("Usage: pm-ansible inventory_parser <inventory_file>")
        sys.exit(1)
    return parse_inventory(args[0])
