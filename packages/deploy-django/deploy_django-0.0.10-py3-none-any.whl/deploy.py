import sys
from pathlib import Path
import os
import ast
import typing
from requirement import install_requirement
import argparse

def main(path :str, project: str) -> None:

    project_path :Path = Path.joinpath(Path(path), project)
    if not Path.joinpath(project_path.absolute(), 'settings.py').exists():
        project_path :Path= Path.joinpath(project_path, project)

    os.chdir(project_path)

    get_settings :Path= Path.joinpath(project_path.absolute(), 'settings.py')

    open_settings :typing.TextIO= open(get_settings, 'r')
    parse = ast.parse(open_settings.read())
    # close settings
    open_settings.close()


    env = {}

    python = 'py'
    if os.name == 'posix':
        python = 'python3'

    base_dir = Path(path)

    try:
        from scripts import create_env, create_settings, configure_gunicorn, make_migrations, collectstatic, configure_nginx
        from utils import change_settings
        
    except ImportError:
        install_requirement(path)
        from scripts import create_env, create_settings, configure_gunicorn, make_migrations, collectstatic, configure_nginx
        from utils import change_settings
        

    os.chdir(project_path)
    # create settings
    create_settings(change_settings(parse, env))
    # create env
    create_env(env)

    # make_migrations
    make_migrations(project_path, path, project, python)

    # collectstatic
    collectstatic(project_path, path, project,python)

    # configure gunicorn
    configure_gunicorn(path, project, project_path)

    # configure nginx

    configure_nginx(base_dir)
if __name__ == '__main__':
    test = False
    path = ''
    project = ''
    if not test:
        parser = argparse.ArgumentParser(description='Simple cli tool to deploy Django applications', add_help=False)

        parser.add_argument('Deploy')
        parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='                To use it just run deploy --path=folder containing your project --project= Your project name')
        parser.add_argument('--path', required=True)#, dest='             Path to the folder which your project is')
        parser.add_argument('--project', required=True)#, dest= '             The name of your project')

        input_args = parser.parse_args(sys.argv)

        path :str = input_args.path
        project :str = input_args.project
    main(path, project)