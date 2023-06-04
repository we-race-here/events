import optparse
import sys
from datetime import datetime

import git
import pytz
import tomlkit
from rich.console import Console
from rich.pretty import pprint

console = Console()

# Pass in release type ["alpha", "beta", "release"]
parser = optparse.OptionParser()
parser.add_option("-t", "--type", help="alpha, beta or release")
parser.add_option("-f", action="store_true", dest="force", help="Force tag even if checks for tag and branch fails")
parser.add_option("-p", action="store_true", dest="push", help="Push or not")
(opts, args) = parser.parse_args()
if not opts.type:
    opts.type = "alpha"
print(opts.type)
print(opts.force)
print(opts.push)
assert opts.type in ["alpha", "beta", "release"]
assert opts.force in [None, True]
assert opts.force in [None, True]

with open("__version__", mode="rt", encoding="utf-8") as ver:
    # data = tml.load(ver)
    data = tomlkit.load(ver)

# bump version
last_ver = data["version"]
console.print(f"Current version: {last_ver}")
data["type"] = opts.type
data["date"] = datetime.now(pytz.timezone("US/Mountain")).date()
if data["date"] == data["date"]:
    data["count"] = data["count"] + 1
else:
    data["count"] = 1
data["version"] = f"{data['date']}.{data['count']}.{data['type']}"
console.print(f"New version: {data['version']}")

# most recent tag
repo = git.Repo("")
origin = repo.remotes.origin
origin.fetch()
try:
    print(f"Current branch: {repo.active_branch}")
    assert repo.active_branch.name == "main"
except AssertionError as e:
    pprint(e)
    if not opts.force:
        console.print_exception()
        sys.exit()
    else:
        console.print("FORCE: Branch not MAIN", style="bold red")
last_tag = repo.tags[-1]
try:
    console.print(f"Most recent it tag: {last_tag.name}")
    assert last_tag.name == last_ver
    assert last_tag.name != data["version"]
    assert data["version"] not in [t.name for t in repo.tags]
except AssertionError:
    if not opts.force:
        console.print_exception()
        sys.exit()
    else:
        console.print("FORCE Tagging", style="bold red")

origin.pull()
new_tag = repo.create_tag(data["version"], message=f"Automatic new tag {data['version']}")
console.print(f"tag bump successfully to {new_tag.name}")

try:
    origin.push()
except Exception:
    console.print("[bold red]WARNING:[/bold red] Push failed, probably becuase git is not configures with ssh")

# Save version file
with open("__version__", mode="wt", encoding="utf-8") as ver:
    tomlkit.dump(data, ver)

console.print("Build Release successful", style="bold green")
