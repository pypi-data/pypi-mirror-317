import secrets
import string

from .session import WialonSession
from .flags import DATAFLAG_UNIT_BASE


def repopulate(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.populate()
        return result

    return wrapper


def is_unique(value: str, session: WialonSession, items_type: str = "avl_unit") -> bool:
    """Determines if the value is unique among Wialon objects of type 'items_type'."""
    result = session.wialon_api.core_check_unique(
        **{"type": items_type, "value": value.strip()}
    ).get("result")
    return not bool(result)


def gen_wialon_password(length: int = 16) -> str:
    """Generates a Wialon compliant password."""
    if length > 64:
        raise ValueError(f"Passwords cannot be greater than 64 chars. Got '{length}'.")
    if length < 4:
        raise ValueError(f"Password cannot be less than 4 chars. Got '{length}'.")

    symbols: str = "!@#$%^*()[]-_+"
    alphabet: str = string.ascii_letters + string.digits + symbols
    password: str = "".join(secrets.choice(alphabet) for _ in range(length - 4))
    return (
        password
        + secrets.choice(string.ascii_lowercase)
        + secrets.choice(string.ascii_uppercase)
        + secrets.choice(string.digits)
        + secrets.choice(symbols)
    )


def get_id_from_iccid(iccid: str, session: WialonSession) -> str | None:
    """Takes a Wialon unit's IMEI # and returns its unit id, if it exists."""
    response = session.wialon_api.core_search_items(
        **{
            "spec": {
                "itemsType": "avl_unit",
                "propName": "sys_unique_id",
                "propValueMask": f"={iccid}",
                "sortType": "sys_unique_id",
                "propType": "property",
                "or_logic": 0,
            },
            "force": 0,
            "flags": DATAFLAG_UNIT_BASE,
            "from": 0,
            "to": 0,
        }
    )
    if response.get("totalItemsCount", 0) != 1:
        return None
    return response["items"][0].get("id")
