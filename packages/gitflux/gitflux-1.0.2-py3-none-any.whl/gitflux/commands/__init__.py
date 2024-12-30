from .list_repos import list_repos_command
from .create_repos import create_repos_command
from .delete_repos import delete_repos_command

command_group = [list_repos_command, create_repos_command, delete_repos_command]
