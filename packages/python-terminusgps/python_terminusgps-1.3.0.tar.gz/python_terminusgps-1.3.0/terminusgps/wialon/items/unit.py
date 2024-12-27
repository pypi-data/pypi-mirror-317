from urllib.parse import quote_plus

from terminusgps.wialon import flags
from terminusgps.wialon.items.base import WialonBase, repopulate


class WialonUnit(WialonBase):
    def create(self, **kwargs) -> int | None:
        if not kwargs.get("owner_id"):
            raise ValueError("'owner_id' is required on creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required on creation.")
        if not kwargs.get("hw_type"):
            raise ValueError("'hw_type' is required on creation.")

        response = self.session.wialon_api.core_create_unit(
            **{
                "creatorId": kwargs["owner_id"],
                "name": kwargs["name"],
                "hwTypeId": kwargs["hw_type"],
                "dataFlags": flags.DATAFLAG_UNIT_BASE,
            }
        )
        return response.get("item", {}).get("id")

    def populate(self) -> None:
        super().populate()
        unit_data = self.session.wialon_api.core_search_item(
            **{"id": self.id, "flags": flags.DATAFLAG_UNIT_ADVANCED_PROPERTIES}
        )
        self.uid = unit_data.get("uid", "")
        self.phone = unit_data.get("ph", "")
        self.is_active = bool(unit_data.get("act", 0))

    def execute_command(
        self,
        name: str,
        link_type: str,
        timeout: int = 5,
        flags: int = 0,
        param: dict | None = None,
    ) -> None:
        self.session.wialon_api.unit_exec_cmd(
            **{
                "itemId": self.id,
                "commandName": name,
                "linkType": link_type,
                "timeout": timeout,
                "flags": flags,
                "param": param if param else {},
            }
        )

    def set_access_password(self, password: str) -> None:
        self.session.wialon_api.unit_update_access_password(
            **{"itemId": self.id, "accessPassword": password}
        )

    @repopulate
    def activate(self) -> None:
        if self.is_active:
            return

        self.session.wialon_api.unit_set_active(
            **{"itemId": self.id, "active": int(True)}
        )

    @repopulate
    def deactivate(self) -> None:
        if not self.is_active:
            return

        self.session.wialon_api.unit_set_active(
            **{"itemId": self.id, "active": int(False)}
        )

    @repopulate
    def assign_phone(self, phone: str) -> None:
        self.session.wialon_api.unit_update_phone(
            **{"itemId": self.id, "phoneNumber": quote_plus(phone)}
        )

    def get_phone_numbers(self) -> list[str]:
        phones = []
        if self.phone:
            phones.append(self.phone)
        for field in self.cfields | self.afields:
            if field["n"] == "to_number":
                phones.append(field["v"])
        return phones
