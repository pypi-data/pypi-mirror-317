from wialon.api import WialonError


class WialonBaseError(Exception):
    def __init__(self, message: str, wialon_err: WialonError | None = None) -> None:
        self.wialon_err = wialon_err
        super().__init__(message)


class WialonLoginError(WialonBaseError):
    def __init__(
        self, token: str | None, wialon_err: WialonError | None = None
    ) -> None:
        message = f"Failed to login to the Wialon API using token: '{token}'"
        if wialon_err:
            message += str(wialon_err)
        super().__init__(message, wialon_err)


class WialonLogoutError(WialonBaseError):
    def __init__(self, session_id: str, wialon_err: WialonError | None = None) -> None:
        message = f"Failed to logout of the Wialon API session: '{session_id}'"
        if wialon_err:
            message += str(wialon_err)
        super().__init__(message, wialon_err)
