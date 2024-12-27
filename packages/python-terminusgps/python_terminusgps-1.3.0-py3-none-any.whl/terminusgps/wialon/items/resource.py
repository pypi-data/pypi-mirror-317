from terminusgps.wialon import flags
from terminusgps.wialon.items.base import WialonBase


class WialonResource(WialonBase):
    def create(self, **kwargs) -> int | None:
        if not kwargs.get("owner_id"):
            raise ValueError("'owner_id' is required on creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required on creation.")

        response = self.session.wialon_api.core_create_resource(
            **{
                "creatorId": kwargs["owner_id"],
                "name": kwargs["name"],
                "dataFlags": flags.DATAFLAG_UNIT_BASE,
                "skipCreatorCheck": True,
            }
        )
        return response.get("item", {}).get("id")
