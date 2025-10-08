from typing import Pattern, Callable
import re

ROUTES: dict[Pattern, Callable] = {}


def route(pattern: str):
    def decorator(func: Callable) -> Callable:
        ROUTES[re.compile(pattern)] = func
        return func
    return decorator


@route(r"/api/v1/users/?")
def user_list():
    user_detail("fulano")
    user_detail("cicrano")
    user_detail("beltrano")

@route(r"/api/v1/users/(?P<username>\w+)/?")
def user_detail(username: str):
    print(f"User: {username}")

@route(r"/auth/login/?")
def login_page():
    print("Login page")

@route(r"/actions/add/(\d+)\+(\d+)/?")
def add(x, y):
    result = int(x) + int(y)
    print("add:", result)

@route(r"/(?P<username>\w+)/(?P<repo>\w+)/?")
def repo_page(username, repo):
    print(f"Repo: {username}/{repo}")


def router(url: str):
    for regex, func in ROUTES.items():
        m = regex.fullmatch(url)
        if m is None:
            continue

        kwargs = m.groupdict()
        if not kwargs:
            args = m.groups()
            return func(*args)

        return func(**kwargs)

    print("Error 404: url nao encontrada")

if  __name__ == "__main__":
    while True:
        try:
            url = input("url: ")
        except (SystemExit, EOFError):
            break
        router(url)