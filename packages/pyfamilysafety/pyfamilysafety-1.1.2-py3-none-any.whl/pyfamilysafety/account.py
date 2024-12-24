# pylint: disable=line-too-long
"""Family safety account handler."""

import asyncio
import logging
from datetime import datetime, date, time
from urllib.parse import quote_plus

from .api import FamilySafetyAPI
from .device import Device
from .application import Application
from .enum import OverrideTarget, OverrideType
from .helpers import localise_datetime, API_TIMEZONE

_LOGGER = logging.getLogger(__name__)

class Account:
    """Represents a single family safety account."""

    def __init__(self, api) -> None:
        """Init an account."""
        self.user_id = None
        self.role = None
        self.profile_picture = None
        self.first_name = None
        self.surname = None
        self.devices: list[Device] = None
        self.applications: list[Application] = []
        self.today_screentime_usage: int = None
        self.average_screentime_usage: float = None
        self.screentime_usage: dict = None
        self.application_usage: dict = None
        self.blocked_platforms: list[OverrideTarget] = None
        self.experimental: bool = False
        self._api: FamilySafetyAPI = api
        self.account_balance: float = 0.0
        self.account_currency: str = ""

    async def update(self) -> None:
        """Update all account details."""
        await self.get_screentime_usage()
        coros = [self._get_devices(), self._get_overrides(), self._get_applications(), self._get_account_balance()]
        await asyncio.gather(*coros)

    async def _get_devices(self) -> list[Device]:
        """Returns all devices on the account."""
        response = await self._api.send_request("get_user_devices", USER_ID=self.user_id)
        self.devices = Device.from_dict(response.get("json"), self.screentime_usage)
        return self.devices

    async def _get_overrides(self):
        """Collects overrides."""
        response = await self._api.send_request(
            endpoint="get_override_device_restrictions",
            USER_ID=self.user_id)
        self._update_device_blocked(response.get("json"))

    async def _get_applications(self) -> list[Application]:
        """Returns all applications on the account."""
        if self.application_usage is None:
            raise ValueError("Application usage not collected, call 'get_screentime_usage' first.")
        parsed_applications = Application.from_app_activity_report(
            self.application_usage,
            self._api,
            self.user_id)
        for app in parsed_applications:
            try:
                self.get_application(app.app_id).update(app)
            except IndexError:
                self.applications.append(app)
        return self.applications

    async def _get_account_balance(self):
        """Updates the account balance."""
        response = await self._api.send_request(
            endpoint="get_user_spending",
            USER_ID=self.user_id
        )
        response = response["json"]
        balances = response.get("balances", [])
        if len(balances) == 1:
            self.account_balance = balances[0]["balance"]
            self.account_currency = balances[0]["currency"]

    async def get_screentime_usage(self,
                                   start_time: datetime = None,
                                   end_time: datetime = None,
                                   device_count = 4,
                                   platform: str = "ALL") -> dict:
        """Returns screentime usage for the account."""
        default = False
        if start_time is None:
            default = True
            start_time = localise_datetime(datetime.combine(date.today(), time(0,0,0), tzinfo=API_TIMEZONE))
        if end_time is None:
            default = True
            end_time = localise_datetime(datetime.combine(date.today(), time(23,59,59), tzinfo=API_TIMEZONE))

        device_usage = await self._api.send_request(
                endpoint="get_user_device_screentime_usage",
                headers={
                    "Plat-Info": platform
                },
                USER_ID=self.user_id,
                BEGIN_TIME=quote_plus(start_time.strftime('%Y-%m-%dT%H:%M:%S%z')),
                END_TIME=quote_plus(end_time.strftime('%Y-%m-%dT%H:%M:%S%z')),
                DEVICE_COUNT=device_count
            )

        application_usage = await self._api.send_request(
                endpoint="get_user_app_screentime_usage",
                headers={
                    "Plat-Info": platform
                },
                USER_ID=self.user_id,
                BEGIN_TIME=quote_plus(start_time.strftime('%Y-%m-%dT%H:%M:%S%z')),
                END_TIME=quote_plus(end_time.strftime('%Y-%m-%dT%H:%M:%S%z'))
            )

        if default:
            self.screentime_usage = device_usage.get("json")
            self.today_screentime_usage = self.screentime_usage["deviceUsageAggregates"]["totalScreenTime"]
            self.average_screentime_usage = self.screentime_usage["deviceUsageAggregates"]["dailyAverage"]
            self.application_usage = application_usage.get("json")
            return self.screentime_usage
        else:
            # don't actually set a value
            return {
                "devices": device_usage.get("json"),
                "applications": application_usage.get("json")
            }

    def get_device(self, device_id) -> Device:
        """Returns a single device."""
        return [x for x in self.devices if x.device_id == device_id][0]

    def get_application(self, application_id) -> Application:
        """Returns a single application."""
        return [x for x in self.applications if x.app_id == application_id][0]

    async def override_device(self,
                              target: OverrideTarget,
                              override: OverrideType,
                              valid_until: datetime = None) -> bool:
        """Overrides a single device (block/unblock)"""
        if override == OverrideType.UNTIL and valid_until is None:
            raise ValueError("valid_until is required if using OverrideType.UNTIL")
        if override == OverrideType.CANCEL:
            valid_until = datetime.now()
        response = await self._api.send_request(
            endpoint="override_device_restriction",
            body={
                "overrideType": str(override),
                "target": str(target),
                "validUntil": valid_until.strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            USER_ID=self.user_id
        )
        self._update_device_blocked(response.get("json"))

    def _update_device_blocked(self, raw_response: dict):
        """updates device(s) blocked status from a overrides response."""
        platforms = raw_response.get("lockablePlatforms")
        blocked_platforms = []
        for platform in platforms:
            # get if locked
            state = len(platform.get("overrides"))>0
            if state:
                blocked_platforms.append(OverrideTarget.from_pretty(platform.get("appliesTo")))

            for device in platform.get("devices"):
                try:
                    self.get_device(device.get("deviceId").replace("g:", "")).update_blocked_status(state)
                finally:
                    pass
        self.blocked_platforms = blocked_platforms

    @classmethod
    async def from_dict(cls, api: FamilySafetyAPI, raw_response: dict, experimental: bool) -> list['Account']:
        """Converts a roster request response to an array."""
        response = []
        if "members" in raw_response.keys():
            members = raw_response.get("members")
            for member in members:
                if member.get("isDigitalSafetyEnabled"):
                    self = cls(api)
                    self.user_id = member.get("id")
                    self.role = member.get("role")
                    self.profile_picture = member.get("profilePicUrl")
                    self.first_name = member.get("user").get("firstName")
                    self.surname = member.get("user").get("lastName")
                    self.experimental = experimental
                    await self.update()
                    response.append(self)

        return response
