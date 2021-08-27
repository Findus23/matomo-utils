from typing import Dict

import requests

from config import *

s = requests.Session()
s.headers.update({"Authorization": "Token " + token})

PROJECT = "matomo"  # "matomo-premium-plugins"


def diff_dicts(dict1, dict2):
    return {key: dict1[key] for key in set(dict1) - set(dict2)}


def lock_component(component, unlock=False):
    lock = not unlock
    lock_url = component["lock_url"]
    r = s.post(lock_url, data={"lock": lock})
    print(r.json())
    r.raise_for_status()


def update_setting(component, settings: Dict):
    component_url = component["url"]
    r = s.patch(component_url, json=settings)
    if r.status_code > 200:
        print(r.json())
        r.raise_for_status()


def create_addon(component, name, configuration: Dict):
    component_url = component["url"]
    r = s.post(component_url + "addons/", json={"name": name, "configuration": configuration})
    if r.status_code > 200:
        print(r.json())
        r.raise_for_status()


components = {}

r = s.get(url + f"projects/{PROJECT}/components/")

data = r.json()
count = data["count"]
for comp in data["results"]:
    components[comp["slug"]] = comp

while data["next"]:
    r = s.get(data["next"])
    data = r.json()
    for comp in data["results"]:
        components[comp["slug"]] = comp

assert len(components) == count

phpcomponents = {slug: comp for slug, comp in components.items() if not comp["is_glossary"]}

community_components = {slug: comp for slug, comp in components.items() if "Community" in comp["name"]}

official_components = diff_dicts(phpcomponents, community_components)

core_repo_components = {slug: comp for slug, comp in components.items() if
                        "https://github.com/matomo-org/matomo/" == comp["repo"]}

non_core_repo_components = diff_dicts(phpcomponents, core_repo_components)


for slug, comp in community_components.items():
    print(slug, comp["name"])
    # print(comp["check_flags"])
    # license = comp["license"]
    # if license != "GPL-3.0-or-later":
    #     print(license)
    update_setting(comp, {
        "check_flags": "php-format,safe-html,ignore-optional-plural",
        # "license": "proprietary",
        "manage_units": False,  # Manage strings
        "enforced_checks": [
            "php_format"
        ],
    })
    if comp["addons"]:
        print("skipping")
        continue
    create_addon(comp, name="weblate.cleanup.blank", configuration={})
    create_addon(comp, name="weblate.cleanup.generic", configuration={})
    create_addon(comp, name="weblate.json.customize", configuration={
        "sort_keys": True,
        "indent": 4,
        "style": "spaces"
    })
    # lock_component(comp, unlock=True)
    # print("locked")
    # exit()
