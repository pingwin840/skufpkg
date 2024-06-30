import argparse
from skufpkg.repository import add_repository, list_repositories, search_packages
from skufpkg.package import install_package, remove_package, list_installed_packages, create_package
from skufpkg.server import start_server

def main():
    parser = argparse.ArgumentParser(description='skufpkg - A simple package manager for Linux')
    subparsers = parser.add_subparsers(dest='command')

    # Repository commands
    parser_add_repo = subparsers.add_parser('add-repo', help='Add a repository')
    parser_add_repo.add_argument('url', help='Repository URL')

    parser_list_repos = subparsers.add_parser('list-repos', help='List all repositories')

    parser_search = subparsers.add_parser('search', help='Search for packages in repositories')
    parser_search.add_argument('package', help='Package name to search for')

    # Package commands
    parser_install = subparsers.add_parser('install', help='Install a package')
    parser_install.add_argument('package', help='Package name')

    parser_remove = subparsers.add_parser('remove', help='Remove a package')
    parser_remove.add_argument('package', help='Package name')

    parser_list_installed = subparsers.add_parser('list-installed', help='List installed packages')

    parser_create_pkg = subparsers.add_parser('create-pkg', help='Create a .skufpkg package')
    parser_create_pkg.add_argument('source', help='Source directory')
    parser_create_pkg.add_argument('name', help='Package name')
    parser_create_pkg.add_argument('version', help='Package version')

    # Server command
    parser_start_server = subparsers.add_parser('start-server', help='Start a repository server')
    parser_start_server.add_argument('--host', default='0.0.0.0', help='Server host')
    parser_start_server.add_argument('--port', type=int, default=5000, help='Server port')

    args = parser.parse_args()

    if args.command == 'add-repo':
        add_repository(args.url)
    elif args.command == 'list-repos':
        list_repositories()
    elif args.command == 'search':
        search_packages(args.package)
    elif args.command == 'install':
        install_package(args.package)
    elif args.command == 'remove':
        remove_package(args.package)
    elif args.command == 'list-installed':
        list_installed_packages()
    elif args.command == 'create-pkg':
        create_package(args.source, args.name, args.version)
    elif args.command == 'start-server':
        start_server(args.host, args.port)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

