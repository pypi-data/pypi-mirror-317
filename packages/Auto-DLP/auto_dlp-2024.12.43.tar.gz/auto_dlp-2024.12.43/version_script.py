import datetime
import re
import sys
from pathlib import Path

python_version_file = Path(".") / "auto_dlp" / "version.py"
pyproject_toml_regex = re.compile("\"(?P<VERSION>[0-9]+\\.[0-9]+\\.[0-9]+)\"\\s*#\\s?version")

def get_version(increment):
    date = datetime.date.today()
    return f"{date.year}.{date.month}.{increment}"


def write_version_file(version):
    python_version_file.touch(exist_ok=True)

    with open(python_version_file, "w") as file:
        file.write(f"""program_version = \"{version}\"""")


def update_pyproject_toml(version):
    path = Path(".") / "pyproject.toml"

    string = path.read_text()
    match = pyproject_toml_regex.search(string)

    print(f"The old version is {match.groupdict()["VERSION"]}")

    path.write_text(pyproject_toml_regex.sub(f"\"{version}\" # version", string))


def update(version):
    print(f"Updating version to {version}")

    write_version_file(version)

    update_pyproject_toml(version)


def main():
    args = sys.argv

    if len(args) <= 1:
        print(f"Not enough parameters for {args[0]}")
        return

    version = get_version(int(sys.argv[1]))
    print(f"The current version is {version}")

    if len(args) <= 2 or args[2] != "update":
        return

    update(version)


main()
