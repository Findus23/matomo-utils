import argparse

import requests

from config import token, url

s = requests.Session()
s.headers.update({"Authorization": "Token " + token})

actions = {
    # see https://github.com/WeblateOrg/weblate/blob/9033a37fd4df0ffa9d7f5160d9647cb84a872330/weblate/trans/models/change.py#L173
    # for all strings
    2: "Changed Translations",
    3: "Comments",
    4: "Suggestion",
    7: "Accepted Suggestions",
    36: "Approve",
}


def print_count(project, year, month, csv=False):
    for action, action_name in actions.items():
        params = {
            "action": action,
            "timestamp_after": f"{year}-{month}-01T00:00:00+00:00",
            "timestamp_before": f"{year}-{month + 1}-01T00:00:00+00:00"
        }

        r = s.get(url + f"projects/{project}/changes/", params=params)

        data = r.json()
        count = data["count"]
        if csv:
            print(count)
        else:
            print(action_name, count)


def main():
    parser = argparse.ArgumentParser(description="fetch weblate statistics")
    parser.add_argument("year", type=int, help="select year for reports")
    parser.add_argument("month", type=int, help="select month for reports")
    parser.add_argument("--premium-plugins", action='store_true', help="get reports for premium plugins")
    parser.add_argument("--csv", action='store_true', help="only output numbers and put every value in a new line")
    args = parser.parse_args()
    project = "matomo-premium-plugins" if args.premium_plugins else "matomo"
    print(f'fetching data for project "{project}"')
    print_count(project, args.year, args.month, args.csv)


if __name__ == '__main__':
    main()
