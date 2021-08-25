import json

import requests

from config import transifex_token

s = requests.Session()
s.headers.update({"Authorization": "Bearer " + transifex_token})

r = s.get("https://rest.api.transifex.com/teams", params={"filter[organization]": "o:matomo"})
print(r.status_code)
print(json.dumps(r.json(), indent=2))

relationships = []

r = s.get("https://rest.api.transifex.com/team_memberships", params={
    "filter[organization]": "o:matomo",
    "filter[team]": "o:matomo:t:matomo-team"
})

print(r.status_code)
data = r.json()
relationships.extend(data["data"])

while data["links"]["next"]:
    print("fetching next page")
    r = s.get(data["links"]["next"])
    data = r.json()
    relationships.extend(data["data"])

print(json.dumps(relationships, indent=2))
