import tomllib


def load_toml_file(path: str):
    with open(path, "rb") as f:
        return tomllib.load(f)
