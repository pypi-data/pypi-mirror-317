from urllib.parse import quote_plus

from terminusgps.wialon import flags
from terminusgps.wialon.items.base import WialonBase
from terminusgps.wialon import constants


class WialonUser(WialonBase):
    def create(self, **kwargs) -> int | None:
        if not kwargs.get("owner_id"):
            raise ValueError("'owner_id' is required on creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required on creation.")
        if not kwargs.get("password"):
            raise ValueError("'password' is required on creation.")

        response = self.session.wialon_api.core_create_user(
            **{
                "creatorId": kwargs["owner_id"],
                "name": kwargs["name"],
                "password": kwargs["password"],
                "dataFlags": flags.DATAFLAG_UNIT_BASE,
            }
        )
        return response.get("item", {}).get("id")

    def _get_access_response(self, hw_type: str) -> dict:
        return self.session.wialon_api.user_get_items_access(
            **{
                "userId": self.id,
                "directAccess": True,
                "itemSuperclass": hw_type,
                "flags": 0x2,
            }
        )

    @property
    def units(self) -> list[str]:
        response = self._get_access_response(hw_type="avl_unit")
        return [key for key in response.keys()]

    @property
    def groups(self) -> list[str]:
        response = self._get_access_response(hw_type="avl_unit_group")
        return [key for key in response.keys()]

    def has_access(self, other: WialonBase) -> bool:
        response: dict = self._get_access_response(hw_type=other.hw_type)
        items: list[str] = [key for key in response.keys()]
        return True if str(other.id) in items else False

    def assign_phone(self, phone: str) -> None:
        self.add_cproperty(("phone", quote_plus(phone)))

    def assign_email(self, email: str) -> None:
        """Assigns an email address to the Wialon user."""
        self.add_cproperty(("email", email))

    def grant_access(
        self, item: WialonBase, access_mask: int = constants.ACCESSMASK_UNIT_BASIC
    ) -> None:
        """Grants item access to the Wialon user according to the access mask integer."""
        self.session.wialon_api.user_update_item_access(
            **{"userId": self.id, "itemId": item.id, "accessMask": access_mask}
        )

    def set_settings_flags(self, flags: int, flags_mask: int) -> None:
        self.session.wialon_api.user_update_user_flags(
            **{"userId": self.id, "flags": flags, "flagsMask": flags_mask}
        )

    def update_password(self, old_password: str, new_password: str) -> None:
        self.session.wialon_api.user_update_password(
            **{
                "userId": self.id,
                "oldPassword": old_password,
                "newPassword": new_password,
            }
        )
