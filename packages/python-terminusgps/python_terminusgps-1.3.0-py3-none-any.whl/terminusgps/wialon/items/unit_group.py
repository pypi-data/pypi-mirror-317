from terminusgps.wialon import constants, flags
from terminusgps.wialon.items.base import WialonBase


class WialonUnitGroup(WialonBase):
    def _update_items(self, new_items: list[str]) -> None:
        self.session.wialon_api.unit_group_update_units(
            **{"itemId": self.id, "units": new_items}
        )

    def create(self, **kwargs) -> int | None:
        if not kwargs.get("owner_id"):
            raise ValueError("'owner_id' is required on creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required on creation.")

        response = self.session.wialon_api.core_create_unit_group(
            **{
                "creatorId": kwargs["owner_id"],
                "name": kwargs["name"],
                "dataFlags": flags.DATAFLAG_UNIT_BASE,
            }
        )
        return response.get("item", {}).get("id")

    def is_member(self, item: WialonBase) -> bool:
        return True if str(item.id) in self.items else False

    def grant_access(self, item: WialonBase, access_mask: int | None = None) -> None:
        if not access_mask:
            access_mask = constants.ACCESSMASK_UNIT_BASIC

        self.session.wialon_api.user_update_item_access(
            **{"userId": item.id, "itemId": self.id, "accessMask": access_mask}
        )

    def revoke_access(self, item: WialonBase) -> None:
        self.session.wialon_api.user_update_item_access(
            **{"userId": item.id, "itemId": self.id, "accessMask": 0}
        )

    def add_item(self, item: WialonBase) -> None:
        new_items: list[str] = self.items + [str(item.id)]
        self._update_items(new_items)

    def rm_item(self, item: WialonBase) -> None:
        assert self.is_member(item), "Cannot remove item, it's not in the group"
        new_items: list[str] = self.items
        new_items.remove(str(item.id))
        self._update_items(new_items)

    @property
    def items(self) -> list[str]:
        """Calls the Wialon API and returns a list of group member IDs."""
        response = self.session.wialon_api.core_search_items(
            **{
                "spec": {
                    "itemsType": "avl_unit_group",
                    "propName": "sys_id",
                    "propValueMask": str(self.id),
                    "sortType": "sys_id",
                    "propType": "property",
                    "or_logic": 0,
                },
                "force": 1,
                "flags": flags.DATAFLAG_UNIT_BASE,
                "from": 0,
                "to": 0,
            }
        )
        return [str(unit_id) for unit_id in response.get("items")[0].get("u", [])]
