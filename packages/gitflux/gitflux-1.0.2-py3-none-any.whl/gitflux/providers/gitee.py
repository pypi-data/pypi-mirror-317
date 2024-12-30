from __future__ import annotations
import json
from typing import Iterable

import urllib3
from gitflux.providers import GitServiceProvider
from gitflux.typing import Repository


def create_provider(token: str) -> GiteeService:
    return GiteeService(token=token)


def convert_git_repo(gitee_repo: dict) -> Repository:
    return Repository(
        name=gitee_repo['name'],
        full_name=gitee_repo['full_name']
    )


class GiteeService(GitServiceProvider):
    token: str
    user: dict
    http: urllib3.PoolManager

    def __init__(self, token: str):
        self.token = token
        self.http = urllib3.PoolManager()
        self.user = self.get_user()

    def get_user(self):
        res = self.http.request(
            method='GET',
            url='https://gitee.com/api/v5/user',
            headers={'Content-Type': 'application/json;charset=UTF-8'},
            fields={'access_token': self.token}
        )

        return json.loads(res.data.decode('utf-8'))

    def get_repos(self) -> Iterable[Repository]:
        res = self.http.request(
            method='GET',
            url='https://gitee.com/api/v5/user/repos',
            headers={'Content-Type': 'application/json;charset=UTF-8'},
            fields={'access_token': self.token}
        )

        return [convert_git_repo(repo) for repo in json.loads(res.data.decode('utf-8'))]

    def create_repo(self, name: str, private: bool):
        res = self.http.request(
            method='POST',
            url='https://gitee.com/api/v5/user/repos',
            headers={'Content-Type': 'application/json;charset=UTF-8'},
            body=json.dumps({
                'name': name,
                'access_token': self.token,
                'private': private
            })
        )

        if res.status >= 400:
            raise RuntimeError(res.status)

    def delete_repo(self, name: str):
        if name.find('/') == -1:
            name = f'{self.user["login"]}/{name}'

        res = self.http.request(
            method='DELETE',
            url=f'https://gitee.com/api/v5/repos/{name}',
            headers={'Content-Type': 'application/json;charset=UTF-8'},
            fields={'access_token': self.token}
        )

        if res.status >= 400:
            raise RuntimeError(res.status)
