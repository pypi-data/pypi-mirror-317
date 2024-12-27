import re
import os
import sys
import warnings
import json
import importlib
import importlib.util
from contextlib import suppress
from tempfile import gettempdir
from collections import OrderedDict

from ansible import modules as ansible_modules
from ansible import __version__ as ansible_version

from .base import get_parser


def import_module_from_path(module_path, directory=None):
    """
    Imports a Python module using importlib. If 'directory' is set, we do a file-based import;
    otherwise normal import_module(module_path).
    """
    with suppress(Exception):
        if directory is None:
            return importlib.import_module(module_path)
        else:
            parts = module_path.split('.')
            file_name = parts[-1] + '.py'
            base_path = os.path.join(directory, *parts[:-1])
            full_path = os.path.join(base_path, file_name)

            if not os.path.isfile(full_path):
                return None  # nocv

            spec = importlib.util.spec_from_file_location(module_path, full_path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod

    return None


def import_class(path, directory=None):
    """
    Returns a class/object from the specified path, e.g. 'mypackage.mymodule.MyClass'.
    """
    m_len = path.rfind(".")
    class_name = path[m_len + 1:]
    module_path = path[:m_len]
    module = import_module_from_path(module_path, directory=directory)
    if not module:
        return None
    return getattr(module, class_name, None)


def find_ansible_collections_paths():
    """
    Returns a list of additional directories for 'ansible_collections/' from:
      - $ANSIBLE_COLLECTIONS_PATHS
      - The default (~/.ansible/collections, /usr/share/ansible/collections)
    """
    paths_env = os.environ.get('ANSIBLE_COLLECTIONS_PATHS')
    if paths_env:
        # e.g. "path1:path2"
        result = [p for p in paths_env.split(os.pathsep) if p.strip()]
    else:
        # Default per Ansible docs
        home = os.path.expanduser("~")
        result = [
            os.path.join(home, ".ansible", "collections"),
            "/usr/share/ansible/collections",
        ]
    return result


class Modules:
    """
    Manages the discovery of modules from:
      - Built-in modules (ansible.builtin.*)
      - Ansible collections (namespace.collection.*)
      - A custom path (treated like 'library'), i.e. the user-defined modules

    If the user specifies at least one --path, we skip built-in & collections
    and only scan those paths. The discovered modules in a custom path
    reflect the subfolder structure (like 'test_pack.test_packed_module').
    """
    __slots__ = (
        'search_paths',
        '_modules_list',
        '_key_filter',
        '_modules_map',
        '_scanned',
    )

    def __init__(self, search_paths=None):
        """
        :param search_paths: A list of directories to scan.
            If it's empty or None => we do built-in + collections.
            If it's non-empty => we treat them as user-defined library paths only.
        """
        self.search_paths = search_paths or []
        self.clean()

    def clean(self):
        self._modules_list = []
        self._key_filter = None
        self._modules_map = {}
        self._scanned = False

    def _record_module(self, public_name, real_import_path):
        """Store the module in both _modules_list and _modules_map."""
        self._modules_list.append(public_name)
        self._modules_map[public_name] = real_import_path

    def _scan_builtin_modules(self):
        """
        Enumerate built-in Ansible modules => 'ansible.builtin.<mod>'.
        """
        builtin_path = ansible_modules.__path__[0]
        for _, dirs, files in os.walk(builtin_path):
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")

            for f in files:
                if not f.endswith(".py"):
                    continue  # nocv
                mod_name = f[:-3]
                if mod_name == "__init__" or mod_name.startswith('_'):
                    continue  # nocv

                public = f"ansible.builtin.{mod_name}"
                real = "ansible.modules"
                real += f".{mod_name}"
                self._record_module(public, real)

    def _scan_collections_in_site_packages(self):  # nocv
        """
        Walk ansible_collections package if installed via pip or ansible>=2.10.
        """
        try:
            import ansible_collections
        except ImportError:
            return  # not installed as a python package

        for base_path in ansible_collections.__path__:
            for root, dirs, files in os.walk(base_path):
                if "__pycache__" in dirs:
                    dirs.remove("__pycache__")
                if "plugins/modules" not in root.replace('\\', '/'):
                    continue

                rel = os.path.relpath(root, base_path)
                parts = rel.split(os.path.sep)
                if len(parts) < 4:
                    # must have at least ["namespace", "collection", "plugins", "modules"]
                    continue
                namespace, collection = parts[0], parts[1]
                subfolders = parts[4:] if len(parts) > 4 else []

                for f in files:
                    if not f.endswith(".py"):
                        continue
                    mod_name = f[:-3]
                    if mod_name == "__init__" or mod_name.startswith('_'):
                        continue

                    if subfolders:
                        public_mod = "_".join(subfolders + [mod_name])
                    else:
                        public_mod = mod_name

                    public = f"{namespace}.{collection}.{public_mod}"
                    real = f"ansible_collections.{namespace}.{collection}.plugins.modules"
                    if subfolders:
                        real += f".{'.'.join(subfolders)}"
                    real += f".{mod_name}"
                    self._record_module(public, real)

    def _scan_collections_in_env_paths(self):
        """
        Also walk ~/.ansible/collections or /usr/share/ansible/collections, etc.
        """
        for base_collections_path in find_ansible_collections_paths():
            collections_root = os.path.join(base_collections_path, "ansible_collections")
            if not os.path.isdir(collections_root):
                continue

            for root, dirs, files in os.walk(collections_root):
                if "__pycache__" in dirs:
                    dirs.remove("__pycache__")  # nocv
                if "plugins/modules" not in root.replace('\\', '/'):
                    continue

                rel = os.path.relpath(root, collections_root)
                parts = rel.split(os.path.sep)
                if len(parts) < 2:
                    continue  # nocv
                namespace, collection = parts[0], parts[1]

                # find where 'plugins' / 'modules' occur
                try:
                    modules_idx = parts.index("modules")
                    subfolders = parts[modules_idx+1:]  # everything after 'modules'
                except ValueError:  # nocv
                    # didn't find them
                    continue

                for f in files:  # nocv
                    if not f.endswith(".py"):
                        continue
                    mod_name = f[:-3]
                    if mod_name == "__init__" or mod_name.startswith('_'):
                        continue

                    if subfolders:
                        public_mod = "_".join(subfolders + [mod_name])
                    else:
                        public_mod = mod_name

                    public = f"{namespace}.{collection}.{public_mod}"
                    real = f"ansible_collections.{namespace}.{collection}.plugins.modules"
                    if subfolders:
                        real += f".{'.'.join(subfolders)}"
                    real += f".{mod_name}"
                    self._record_module(public, real)

    def _scan_custom_path(self, custom_dir):
        """
        Enumerate modules in 'custom_dir'.
        The discovered module name is <subfolder>.<filename> (minus .py),
        ignoring the top-level directory name itself.
        Example: custom_dir=./test_modules
          If we have ./test_modules/test_pack/test_packed_module.py,
          we produce 'test_pack.test_packed_module'.
        """
        base_path = os.path.abspath(custom_dir)
        for root, dirs, files in os.walk(base_path):
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")

            rel = os.path.relpath(root, base_path)  # e.g. "test_pack"
            if rel == ".":
                rel = ""

            # Replace path separators with dots => "test_pack"
            rel = rel.replace(os.path.sep, '.')

            for f in files:
                if not f.endswith(".py"):
                    continue
                mod_name = f[:-3]
                if mod_name == "__init__" or mod_name.startswith('_'):
                    continue

                if rel:
                    public = f"{rel}.{mod_name}"
                else:
                    public = mod_name
                # For file-based import, the real path is also 'public'
                # We'll do the import via spec_from_file_location.
                self._record_module(public, public)

    def _scan_all(self):
        """
        If user specified --path => scan only those directories.
        Otherwise => scan built-in + collections from site-packages + env paths.
        """
        if self.search_paths:
            # user library mode
            for p in self.search_paths:
                self._scan_custom_path(p)
        else:
            # built-in + collections
            self._scan_builtin_modules()
            self._scan_collections_in_site_packages()
            self._scan_collections_in_env_paths()

    def get(self, regex=""):
        """
        Return all public module names, or only those matching a regex.
        """
        self._scan_all()
        if not regex:
            return list(self._modules_list)

        pattern = re.compile(regex, re.IGNORECASE)
        return [m for m in self._modules_list if pattern.search(m)]

    def get_mod_info(self, public_name, sub="DOCUMENTATION"):
        """
        If it's from a custom path => real_import_path == public_name => file-based import.
        If it's built-in or from a collection => real_import_path is a Python package path.
        """
        real_path = self._modules_map.get(public_name)
        if not real_path:
            return None  # nocv

        directory = None
        # If real_path is exactly the 'public_name' and user provided a path => file-based import
        if real_path == public_name and self.search_paths:
            # we don't know which custom dir it belongs to if multiple
            # but typically it should be found in one of them
            # We'll guess the first that actually has that file
            for custom_dir in self.search_paths:
                # Build a hypothetical .py path
                parts = public_name.split('.')
                file_name = parts[-1] + '.py'
                base_path = os.path.join(custom_dir, *parts[:-1])
                test_full = os.path.join(base_path, file_name)
                if os.path.isfile(test_full):
                    directory = custom_dir
                    break

        return import_class(f"{real_path}.{sub}", directory=directory)


class AnsibleModules(Modules):
    """
    Wraps the Modules class to optionally provide detailed info (DOCUMENTATION).
    """
    __slots__ = ('detailed',)

    def __init__(self, detailed=False, search_paths=None):
        super(AnsibleModules, self).__init__(search_paths=search_paths)
        self.detailed = detailed

    def _get_detail_info(self, public_name, doc_data):
        return OrderedDict([
            ('path', public_name),
            ('doc_data', doc_data),
        ])

    def _get_info(self, public_name):
        doc = self.get_mod_info(public_name, sub="DOCUMENTATION")
        if isinstance(doc, BaseException) or doc is None:
            return None
        return self._get_detail_info(public_name, doc)

    def get(self, regex=""):
        names = super(AnsibleModules, self).get(regex)
        if not self.detailed:
            return names

        results = []
        for n in names:
            detail = self._get_info(n)
            if detail:
                results.append(detail)
        return results


def get_data(args):
    """
    Collects a list (or detail) of modules given CLI args.
    If no paths => we scan built-in + collections
    If user supplies --path => we only scan those directories, ignoring built-ins/collections.
    """
    # user might pass multiple --path => we gather them
    paths = [p for p in args.path if p is not None]

    # If zero explicit paths => normal (built-in + collections)
    search_paths = paths or []

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
        mod = AnsibleModules(detailed=args.detail, search_paths=search_paths)
        return mod.get(args.get)


def get_from_cache(args):
    """
    Simple file-based cache unless --cachedir=NoCache or multiple --path used.
    """
    # if user passed multiple --path => skip caching
    if len(args.path) > 1:
        return get_data(args)

    cache_dir = args.cachedir
    try:
        if cache_dir == 'NoCache':
            return get_data(args)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    except Exception:  # nocv
        return get_data(args)

    suffix = 'detail' if args.detail else 'list'
    cache_name = os.path.join(cache_dir, f"{args.get or 'all'}_{suffix}")

    try:
        with open(cache_name, 'r') as fd:
            return json.load(fd)
    except Exception:
        data = get_data(args)
        with suppress(Exception):
            with open(cache_name, 'w') as fd:
                json.dump(data, fd)
        return data


def handler(args=sys.argv[1:], parser=get_parser()):
    """
    Handler for the 'modules' command.
    Usage:
      pm-ansible modules
      pm-ansible modules --path ./test_modules --get test_pack.test_packed_module --detail
      pm-ansible modules --detail --get '^community\.general\.'
    """
    default_cache_dir = os.path.join(gettempdir(), f"pm_cache_ansible_{ansible_version}")
    parser.add_argument(
        '--detail', action='store_true',
        help='Get detailed info (module doc strings).',
    )
    parser.add_argument(
        '--get', type=str, default='',
        help='Regex to filter modules by name. Default: all.',
    )
    parser.add_argument(
        '--cachedir', type=str, default=default_cache_dir,
        help=f'Use file-based cache. Default [{default_cache_dir}] or "NoCache".',
    )
    parser.add_argument(
        '--path', type=str, default=[None], action='append',
        help='Library path(s) to scan. If set, built-in & collections are ignored.',
    )
    parser.add_argument(
        '--indent', type=int, default=None,
        help='Indent level for JSON output.',
    )
    _args = parser.parse_args(args)

    result = get_from_cache(_args)
    json.dump(result, sys.stdout, indent=_args.indent)
    sys.stdout.flush()
