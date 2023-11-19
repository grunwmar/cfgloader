from cfgload import ConfigDict
import cfgload

cfgload.TO_STRING_INDENT = None


FILE_LST = ["test_files/test.json", "test_files/test.yaml", "test_files/test.toml"]

for fn in FILE_LST:
    config = ConfigDict.file_load(fn)
    print(fn, "-->", config)

print("\n")

for fn in FILE_LST:
    with open(fn, "r") as fp:
        config = ConfigDict.file_load(fp)
        print(fn, "-->", config)

print("\n")

STRINGS = {
    "json": """{"users": {"name": ["Eric", "Cook"]}}""",
    "yaml": """
users:
    name: [Eric, Cook]
""",
    "toml": """
[users]
name = ["Eric", "Cook"]
"""
}

for sft, st in STRINGS.items():
    config = ConfigDict.string_load(string=st, sformat=sft)
    print("<--- --- ---", sft, "--- --- --->")
    print("\n...")
    print(st)
    print("...\n")
    print(config, "\n")

# GIT HUB api test

config = ConfigDict.http_load("https://api.github.com/", sformat=cfgload.FORMAT_JSON)
print("GitHub", config)