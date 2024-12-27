import asyncio
import logging
from typing import List
from . import engine, messages


_LOG = logging.getLogger("pysignalapi.api")


class _BaseAPI:
    def __init__(self, engine):
        self.engine = engine

    # API

    # General

    def about(self):
        """Returns the supported API versions and the internal build nr."""
        result = self.engine.get("v1/about")
        return result.json()

    def configuration(self):
        """List the REST API configuration."""
        result = self.engine.get("v1/configuration")
        return result.json()

    def set_configuration(self, *, logging_level):
        result = self.engine.post(
            "v1/configuration",
            json={"logging": {"Level": logging_level}},
        )
        return result.text

    def get_account_settings(self, number):
        """List account specific settings."""
        result = self.engine.get(f"v1/configuration/{number}/settings")
        return result.content

    def set_account_settings(self, number, *, trust_mode: str):
        """Set account specific settings."""
        result = self.engine.post(
            f"v1/configuration/{number}/settings",
            json={"truts_mode": trust_mode},
        )
        return result.content

    # Devices

    def qrcodelink(self, device_name="PYSIGNAL_DEVICE"):
        """returns png binary image"""
        result = self.engine.get(f"v1/qrcodelink?device_name={device_name}")
        return result.content

    def register(self, number, use_voice=False):
        result = self.engine.post(
            f"v1/register/{number}",
            json={"captcha": "string", "use_voice": use_voice},
        )
        return result.content

    def unregister(self, number):
        result = self.engine.post(
            f"v1/unregister/{number}",
            json={"delete_account": False, "delete_local_data": True},
        )
        return result.content

    # accounts

    def get_accounts(self):
        result = self.engine.get("v1/accounts")
        return result.json()

    def username_remove(self, number):
        return self.engine.delete(f"v1/accounts/{number}/username")

    # groups

    def get_groups(self, number):
        result = self.engine.get(f"v1/groups/{number}")
        return result.json()

    def create_group(
        self,
        number,
        *,
        name: str,
        description: str,
        members: list[str],
    ):
        result = self.engine.post(
            f"v1/groups/{number}",
            json={
                "description": description,
                "expiration_time": 0,
                "group_link": "disabled",
                "members": members,
                "name": name,
                "permissions": {
                    "add_members": "only-admins",
                    "edit_group": "only-admins",
                },
            },
        )
        return result.json()

    def get_group(self, number, group_id: str):
        result = self.engine.get(f"v1/groups/{number}/{group_id}")
        return result.json()

    def update_group(
        self,
        number,
        group_id: str,
        *,
        base64_avatar: str,
        description: str,
        name: str,
        expiration_time: int = 0,
    ):
        result = self.engine.put(
            f"v1/groups/{number}/{group_id}",
            json={
                "base64_avatar": base64_avatar,
                "description": description,
                "expiration_time": expiration_time,
                "name": name,
            },
        )
        return result.text

    def delete_group(self, number, group_id: str):
        result = self.engine.delete(f"v1/groups/{number}/{group_id}")
        return result.text

    def quit_group(self, number, group_id: str):
        result = self.engine.post(f"v1/groups/{number}/{group_id}/quit")
        return result.text

    def get_groups_members(self, number, group_id):
        result = self.engine.get(f"v1/groups/{number}/{group_id}")
        return result.json()

    # Messages

    def send(
        self,
        number,
        *,
        msg: str,
        recipients: List[str],
        mentions: List[messages.SendMention] = [],
        styled=False,
    ):
        result = self.engine.post(
            "v2/send",
            json={
                "number": number,
                "message": msg,
                "recipients": recipients,
                "mentions": mentions,
                "text_mode": "styled" if styled else "normal",
            },
        )
        return result.json()

    # Profiles

    def update_profile(
        self,
        number,
        about,
        base64_avatar,
        name,
    ):
        result = self.engine.put(
            f"/v1/profiles/{number}",
            json={"about": about, "base64_avatar": base64_avatar, "name": name},
        )
        return result.text

    # Identities

    def get_identities(self, number):
        result = self.engine.get(f"v1/identities/{number}")
        return result.json()

    def trust_identity(
        self,
        number,
        *,
        numberToTrust: str,
        trust_all_or_safety_number: bool | str,
    ):
        data = {}
        if isinstance(trust_all_or_safety_number, bool):
            data["trust_all_known_keys"] = trust_all_or_safety_number
        elif isinstance(trust_all_or_safety_number, str):
            data["verified_safety_number"] = trust_all_or_safety_number
        else:
            raise RuntimeError("Set `trust_all_or_safety_number` as bool or string!")

        result = self.engine.put(
            f"/v1/identities/{number}/trust/{numberToTrust}",
            json=data,
        )
        return result.text


class NativeAPI(_BaseAPI):
    def __init__(self, url):
        super().__init__(engine.NativeEngine(url))

    def receive(self, number):
        result = self.engine.get(f"v1/receive/{number}")
        return result.json()


class JsonRPCAPI(_BaseAPI):
    def __init__(self, url):
        super().__init__(engine.JsonRPCEngine(url))
        self.message_handlers = []

    def handler(self, func):
        self.message_handlers.append(func)

    async def receive(self, number):
        async for message in self.engine.fetch(number):
            for handler in self.message_handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(number, message)
                    else:
                        handler(number, message)
                except Exception as e:  # noqa: E722
                    _LOG.exception(e)
                except:  # noqa: E722
                    pass
