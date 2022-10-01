def dict2str(d: dict) -> str:
    s = ""
    for k in d:
        s += " "
        s += f"{k}={d[k]}"
    return s


