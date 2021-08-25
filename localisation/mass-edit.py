from typing import Dict

import requests

from config import *

s = requests.Session()
s.headers.update({"Authorization": "Token " + token})


def lock_component(component, unlock=False):
    lock = not unlock
    lock_url = component["lock_url"]
    r = s.post(lock_url, data={"lock": lock})
    print(r.json())
    r.raise_for_status()


def update_setting(component, settings: Dict):
    component_url = component["url"]
    r = s.patch(component_url, data=settings)
    if r.status_code > 200:
        print(r.json())
        r.raise_for_status()


components = {}

r = s.get(url + "projects/matomo/components/")

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

official_components = {slug: components[slug] for slug in set(phpcomponents) - set(community_components)}

core_repo_components = {slug: comp for slug, comp in components.items() if
                        "https://github.com/matomo-org/matomo/" == comp["repo"]}

for slug, comp in phpcomponents.items():
    print(slug, comp["name"])
    print(comp["check_flags"])
    license = comp["license"]
    if license != "GPL-3.0-or-later":
        print(license)
    update_setting(comp, {
        "check_flags": "php-format,ignore-optional-plural"
    })
    # lock_component(comp)
    # print("locked")
