from typing import Dict, List, Tuple

import requests

from config import *
from priorities import priorities, Priority

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


def get_addons(addons: List[str]) -> Tuple[Dict[str, int], Dict[str, Dict]]:
    ids = {}
    configs = {}
    for addon in addons:
        r = s.get(addon)
        data = r.json()
        ids[data["name"]] = data["id"]
        configs[data["name"]] = data["configuration"]
    return ids, configs


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
non_core_repo_components = diff_dicts(non_core_repo_components, community_components)

for slug, comp in phpcomponents.items():
    print(slug, comp["name"])
    addon_ids, addon_configs = get_addons(comp["addons"])
    license = comp["license"]
    if license != "GPL-3.0-or-later":
        print(license)
    if slug in priorities:
        priority = priorities[slug]
    else:
        priority = Priority.medium
    update_setting(comp, {
        "check_flags": "php-format,safe-html,ignore-optional-plural",
        # "license": "proprietary",
        "manage_units": False,  # Manage strings
        "edit_template": True,
        "enforced_checks": [
            "php_format"
        ],
        "priority": priority.value,
        "language_code_style": "bcp",
        "new_lang": "contact",
        "push_on_commit": True,
    })
    if "weblate.cleanup.blank" not in addon_ids.keys():
        create_addon(comp, name="weblate.cleanup.blank", configuration={})
    if "weblate.cleanup.generic" not in addon_ids.keys():
        create_addon(comp, name="weblate.cleanup.generic", configuration={})
    if "weblate.json.customize" not in addon_ids.keys():
        create_addon(comp, name="weblate.json.customize", configuration={
            "sort_keys": True,
            "indent": 4,
            "style": "spaces"
        })
    if "weblate.git.squash" not in addon_ids.keys():
        print("add addon")
        create_addon(comp, name="weblate.git.squash", configuration={
            "squash": "language",
            "append_trailers": True,
            "commit_message": ""
        })
    # input("done\n")
    # lock_component(comp, unlock=True)
    # print("locked")
    # exit()
