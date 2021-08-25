from dataclasses import dataclass
from typing import Dict


@dataclass
class User:
    username: str
    num_contributions: int

    @property
    def deleted(self):
        return len(self.username) in [32, 40]


language_codes = set()
language_names = {}

data: Dict[str, list[User]] = {}

with open("matomo_multiple-teams_20100901_20210824_by-language.csv") as f:
    next(f)
    for line in f:
        columns = line.split(",")
        username = columns[0]
        language = columns[1]
        print(language)
        splits = language.split(" ")

        lang_name = " ".join(splits[:-1]).strip()
        lang_code = splits[-1][1:-1].strip()
        if username == "sgiehl" and lang_code != "de":
            continue
        language_codes.add(lang_code)
        language_names[lang_code] = lang_name
        num_new = int(columns[12])
        num_edit = int(columns[13])
        num_review = int(columns[14])
        num_contributions = num_new + num_edit + num_review
        user = User(username=username, num_contributions=num_contributions)
        if lang_code in data:
            data[lang_code].append(user)
        else:
            data[lang_code] = [user]

language_codes = sorted(list(language_codes))
for lang_code in language_codes:
    users = data[lang_code]
    lang_name = language_names[lang_code]
    users.sort(key=lambda u: -u.num_contributions)
    usernames = [user.username + str(user.num_contributions) for user in users if not user.deleted]
    deleted_users = [u for u in users if u.deleted]
    if len(deleted_users) > 1:
        usernames.append(f"{len(deleted_users)} deleted users")
    elif len(deleted_users) == 1:
        usernames.append(f"{len(deleted_users)} deleted user")

    print(f"{lang_name} ({lang_code})")
    print(", ".join(usernames))
