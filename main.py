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


"""
OUTPUT:

test_files/test.json --> ConfigDict({"users": {"name": ["John", "Smith"]}})
test_files/test.yaml --> ConfigDict({"users": {"name": ["John", "Smith"]}})
test_files/test.toml --> ConfigDict({"users": {"name": ["John", "Smith"]}})


test_files/test.json --> ConfigDict({"users": {"name": ["John", "Smith"]}})
test_files/test.yaml --> ConfigDict({"users": {"name": ["John", "Smith"]}})
test_files/test.toml --> ConfigDict({"users": {"name": ["John", "Smith"]}})


<--- --- --- json --- --- --->

...
{"users": {"name": ["Eric", "Cook"]}}
...

ConfigDict({"users": {"name": ["Eric", "Cook"]}}) 

<--- --- --- yaml --- --- --->

...

users:
    name: [Eric, Cook]

...

ConfigDict({"users": {"name": ["Eric", "Cook"]}}) 

<--- --- --- toml --- --- --->

...

[users]
name = ["Eric", "Cook"]

...

ConfigDict({"users": {"name": ["Eric", "Cook"]}}) 

GitHub ConfigDict({"current_user_url": "https://api.github.com/user", "current_user_authorizations_html_url": "https://github.com/settings/connections/applications{/client_id}", "authorizations_url": "https://api.github.com/authorizations", "code_search_url": "https://api.github.com/search/code?q={query}{&page,per_page,sort,order}", "commit_search_url": "https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}", "emails_url": "https://api.github.com/user/emails", "emojis_url": "https://api.github.com/emojis", "events_url": "https://api.github.com/events", "feeds_url": "https://api.github.com/feeds", "followers_url": "https://api.github.com/user/followers", "following_url": "https://api.github.com/user/following{/target}", "gists_url": "https://api.github.com/gists{/gist_id}", "hub_url": "https://api.github.com/hub", "issue_search_url": "https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}", "issues_url": "https://api.github.com/issues", "keys_url": "https://api.github.com/user/keys", "label_search_url": "https://api.github.com/search/labels?q={query}&repository_id={repository_id}{&page,per_page}", "notifications_url": "https://api.github.com/notifications", "organization_url": "https://api.github.com/orgs/{org}", "organization_repositories_url": "https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}", "organization_teams_url": "https://api.github.com/orgs/{org}/teams", "public_gists_url": "https://api.github.com/gists/public", "rate_limit_url": "https://api.github.com/rate_limit", "repository_url": "https://api.github.com/repos/{owner}/{repo}", "repository_search_url": "https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}", "current_user_repositories_url": "https://api.github.com/user/repos{?type,page,per_page,sort}", "starred_url": "https://api.github.com/user/starred{/owner}{/repo}", "starred_gists_url": "https://api.github.com/gists/starred", "topic_search_url": "https://api.github.com/search/topics?q={query}{&page,per_page}", "user_url": "https://api.github.com/users/{user}", "user_organizations_url": "https://api.github.com/user/orgs", "user_repositories_url": "https://api.github.com/users/{user}/repos{?type,page,per_page,sort}", "user_search_url": "https://api.github.com/search/users?q={query}{&page,per_page,sort,order}"})

Process finished with exit code 0
"""