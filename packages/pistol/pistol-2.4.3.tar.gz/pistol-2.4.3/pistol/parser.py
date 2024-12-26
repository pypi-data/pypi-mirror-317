def parse_command(parts: list[str]):
    new: list[str] = []
    string: str = ""

    for part in parts:
        if not part:
            continue
        elif string:
            if part[-1] == string:
                new[-1] += " " + part[:-1]
                string = ""
            else:
                new[-1] += " " + part
        elif part[0] in "\"'":
            if len(part) > 1 and part[-1] == part[0]:
                new.append(part[1:-1])
            else:
                new.append(part[1:])
                string = part[0]
        else:
            new.append(part)
    return new, string