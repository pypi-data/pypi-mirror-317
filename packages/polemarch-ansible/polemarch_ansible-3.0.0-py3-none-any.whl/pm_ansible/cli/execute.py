import os
import sys
import subprocess

from .base import get_parser

ON_POSIX = 'posix' in sys.builtin_module_names


def get_ansible_command(command):
    """
    Attempt to run an Ansible command from the same directory as sys.executable,
    otherwise fall back to PATH.
    """
    python_exec_dir = os.path.dirname(sys.executable)
    maybe_command = os.path.join(python_exec_dir, command)
    if os.path.exists(maybe_command):
        return maybe_command
    return command  # nocv


def print_output(output):
    if output:
        try:
            output = output.decode('utf-8')
        except UnicodeDecodeError:  # nocv
            return False
        print(output, end='')
        sys.stdout.flush()
    return True


def handler(args=sys.argv[1:], parser=get_parser()):
    """
    Executes ansible/ansible-playbook/... via subprocess, piping stdout/stderr to current stdout.
    """
    command, arguments = get_ansible_command(args[0]), args[1:]
    os.environ.setdefault('ANSIBLE_FORCE_COLOR', 'true')

    process = subprocess.Popen(
        [command] + arguments,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0,
        env=os.environ.copy(),
        close_fds=ON_POSIX,
    )

    rc = None
    while True:
        output = process.stdout.read(1)
        if rc is not None:
            # process ended, read remaining bytes
            output += process.stdout.read()
            print_output(output)
            break

        if not print_output(output):
            continue  # nocv

        rc = process.poll()

    process.stdout.close()
    sys.exit(rc) if rc else 0
