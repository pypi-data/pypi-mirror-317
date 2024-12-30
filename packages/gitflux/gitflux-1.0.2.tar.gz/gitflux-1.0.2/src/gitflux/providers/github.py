from __future__ import annotations
from typing import Iterable
from github import Github, AuthenticatedUser, Organization, Repository as GitHubRepository
from gitflux.typing import Repository
from gitflux.providers import GitServiceProvider


def create_provider(token: str) -> GitHubService:
    return GitHubService(token=token)


def convert_git_repo(github_repo: GitHubRepository) -> Repository:
    repo = Repository(
        name=github_repo.name,
        full_name=github_repo.full_name
    )

    return repo


def parse_repo_fullname(fullname: str, user: AuthenticatedUser, orgs: list[Organization]) -> tuple:
    if fullname.find('/') == -1:
        owner = user
        repo_name = fullname
    else:
        org_name, repo_name = fullname.split('/')

        if org_name == user.login:
            owner = user
        else:
            owner = next((x for x in orgs if x.login == org_name), None)

        if owner is None:
            raise NameError(f'Organization not found: {org_name}.')

    return owner, repo_name


class GitHubService(GitServiceProvider):
    api: Github
    user: AuthenticatedUser
    orgs: Iterable[Organization]

    def __init__(self, token: str):
        self.api = Github(login_or_token=token)
        self.user = self.api.get_user()
        self.orgs = self.user.get_orgs()

    def get_repos(self) -> Iterable[Repository]:
        return map(convert_git_repo, self.user.get_repos())

    def create_repo(self, name: str, private: bool):
        owner, repo_name = parse_repo_fullname(name, self.user, self.orgs)
        owner.create_repo(repo_name, private=private)

    def delete_repo(self, name: str):
        owner, repo_name = parse_repo_fullname(name, self.user, self.orgs)
        owner.get_repo(repo_name).delete()
