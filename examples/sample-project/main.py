"""Tiny fixture used in the RepoLens quick demo."""


def greet(name: str) -> str:
    return f"Hello, {name}!"


class Greeter:
    def run(self, name: str) -> str:
        return greet(name)
