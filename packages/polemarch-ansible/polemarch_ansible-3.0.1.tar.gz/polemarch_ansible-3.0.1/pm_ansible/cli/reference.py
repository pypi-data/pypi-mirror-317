import os
import sys
import json
from contextlib import redirect_stderr, redirect_stdout, suppress
from collections import OrderedDict

from ansible import __version__ as ansible_version
from ansible.cli.adhoc import AdHocCLI
from ansible.cli.playbook import PlaybookCLI

from .base import get_parser


class AnsibleArgumentsReference:
    """
    Collects CLI argument details from Ansible's AdHocCLI, PlaybookCLI, GalaxyCLI.
    """

    def __init__(self, cli_types=(), exclude=()):
        self._exclude = exclude or []
        self._cli_filter = cli_types or []
        self.raw_dict = self._extract_from_cli()

    @property
    def clis(self):
        """
        Ansible CLI objects for:
          - 'module' => AdHocCLI
          - 'playbook' => PlaybookCLI
        """
        return {
            "module": AdHocCLI(args=["", "all"]),
            "playbook": PlaybookCLI(args=["", "none.yml"]),
        }

    def __help_text_format(self, action):
        """
        Formats the help text with any embedded '%(default)s' placeholders.
        """
        result = (action.help or '')
        with suppress(Exception):
            result = result % {'default': action.default}
        return result

    def parse_cli(self, cli):
        """
        Modern approach for Ansible >= 2.9 (including ansible-core).
        We parse the CLI quietly (redirecting stdout/stderr), then iterate over cli.parser._actions.
        """
        with suppress(BaseException):
            with open(os.devnull, 'w') as fd, redirect_stderr(fd), redirect_stdout(fd):
                cli.parse()

        cli_result = OrderedDict()
        for action in cli.parser._actions:
            # If we have --long-option in action.option_strings, let's use that for 'name'
            # otherwise fallback to action.dest
            long_opts = [opt for opt in action.option_strings if opt.startswith('--')]
            if long_opts:
                name = long_opts[0][2:]  # strip leading --
            else:
                name = action.dest

            if name in self._exclude:
                continue

            shortopts = [opt for opt in action.option_strings if opt.startswith('-') and not opt.startswith('--')]
            # Determine type
            action_type = action.type
            if not action_type:
                class_name = action.__class__.__name__
                if class_name in ['_StoreTrueAction', '_StoreFalseAction', '_StoreConstAction']:
                    action_type = 'bool'
                elif class_name in ['_CountAction', '_AppendAction']:
                    action_type = 'int'
                else:
                    action_type = 'string'
            elif hasattr(action_type, '__name__'):
                action_type = action_type.__name__
            else:
                action_type = 'string'  # nocv

            cli_result[name] = {
                'type': action_type,
                'help': self.__help_text_format(action),
                'shortopts': [s for s in shortopts if len(s) > 1],
            }
        return cli_result

    def _extract_from_cli(self):
        """
        Builds a dictionary with CLI arguments from the relevant CLI objects.
        For each CLI object (module, playbook, galaxy), we parse the CLI.
        """
        result = OrderedDict()

        for name, cli_obj in self.clis.items():
            if not self._cli_filter or (name in self._cli_filter):
                result[name] = self.parse_cli(cli_obj)

        answer = OrderedDict()
        answer['version'] = ansible_version
        answer['keywords'] = result
        return answer


def handler(args=sys.argv[1:], parser=get_parser()):
    """
    CLI handler for the 'reference' command, collecting Ansible CLI argument references.
    Example usage:
      pm-ansible reference
      pm-ansible reference module
      pm-ansible reference --exclude=inventory
    """
    parser.add_argument(
        'filter', type=str, nargs='*', action='append',
        help='Filter CLI by type (module, playbook, galaxy). Default is all.',
    )
    parser.add_argument(
        '--exclude', type=str, nargs='?', action='append',
        help='Filter out args by name (comma separated).',
    )
    parser.add_argument(
        '--indent', action='store_true',
        help='Indent for JSON output.',
    )
    _args = parser.parse_args(args)

    # _args.filter is a list of lists => e.g. [['module','playbook']]
    # so let's flatten or pick the first sub-list
    cli_filter = _args.filter[0] if _args.filter else []

    exclude_list = []
    if _args.exclude:
        # each --exclude could be "arg1,arg2"
        for ex in _args.exclude:
            if ex:
                exclude_list.extend(ex.split(','))

    reference = AnsibleArgumentsReference(cli_types=cli_filter, exclude=exclude_list)
    json.dump(reference.raw_dict, sys.stdout, indent=2 if _args.indent else None)
    sys.stdout.flush()
