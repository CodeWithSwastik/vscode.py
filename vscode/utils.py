from typing import Optional

__all__ = (
    "log",
    "camel_case_to_snake_case",
    "snake_case_to_camel_case",
    "snake_case_to_title_case",
    "python_condition_to_js_condition",
)


def log(*args, **kwargs):
    kwargs["flush"] = True
    print(*args, **kwargs)


def camel_case_to_snake_case(text: str) -> str:
    return "".join("_" + i.lower() if i.isupper() else i for i in text).lstrip("_")


def snake_case_to_camel_case(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None

    temp = text.split("_")
    return temp[0] + "".join(ele.title() for ele in temp[1:])


def snake_case_to_title_case(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None

    return text.replace("_", " ").title()


def python_condition_to_js_condition(condition: Optional[str]) -> Optional[str]:
    if condition is None:
        return None

    condition = " ".join(
        i if "_" not in i else snake_case_to_camel_case(i) for i in condition.split(" ")
    )
    condition = condition.replace(" and ", " && ")
    condition = condition.replace(" or ", " || ")
    if " not " in condition:
        if "(" not in condition or ")" not in condition:
            raise SyntaxError(
                "Use parenthesis '()' while using 'not' otherwise your conditions might not work as expected!"
            )
        else:
            condition = condition.replace(" not ", " !")

    return condition
