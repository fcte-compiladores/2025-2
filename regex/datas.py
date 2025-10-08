import re
import datetime

DATE_REGEX = re.compile(r"""
    # Formato padrao
    (?P<day>[0-9]{1,2})/(?P<month>[0-9]{1,2})/(?P<year>[0-9]{2,4})

    # Formato ISO
    |(?P<isoyear>[0-9]{4})-(?P<isomonth>[0-9]{2})-(?P<isoday>[0-9]{2})
""", re.VERBOSE)


def parse(text: str) -> datetime.date | None:
    m = DATE_REGEX.fullmatch(text)
    if m is None:
        return None
    groups = {k.removeprefix("iso"): v for k, v in m.groupdict().items() if v is not None}
    if len(groups["year"]) == 2:
        groups["year"] = "20" + groups["year"]

    kwargs = {k: int(v) for k, v in groups.items()}
    try:
        return datetime.date(**kwargs)
    except ValueError:
        return None


if __name__ == "__main__":
    print("Digite datas no formato YYYY-MM-DD ou dd/mm/yyyy")
    while True:
        try:
            text = input("> ")
        except (EOFError, SystemExit):
            break

        date = parse(text)
        print(date or "<error>")