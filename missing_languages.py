from pathlib import Path

lang_dir = Path("../../lang")

languages_in_matomo = set(str(dir.stem) for dir in lang_dir.glob("*.json"))

print(len(languages_in_matomo))

languages_in_transifex = set()
completenesses = {}
names = {}
with open("matomo_matomo.languages.csv") as f:
    next(f)
    for line in f:
        cols = line.split(",")
        name = cols[0]
        code = cols[1].replace("_", "-").lower()
        if code == "-":
            continue
        completeness = 100 - float(cols[3][:-1])
        languages_in_transifex.add(code)
        completenesses[code] = completeness
        names[code] = name

assert languages_in_matomo - languages_in_transifex == {"dev"}

for code in languages_in_transifex - languages_in_matomo:
    print(code, names[code], f"{completenesses[code]:.2f}% complete")
