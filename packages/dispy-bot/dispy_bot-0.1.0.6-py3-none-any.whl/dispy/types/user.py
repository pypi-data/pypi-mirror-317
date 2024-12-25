# Dispy - Python Discord API library for discord bots.
# Copyright (C) 2024  James French
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from dispy.modules.dictwrapper import DictWrapper
from dispy.types.variable import Snowflake, Timestamp
from typing import List, Dict, Any

class AvatarDecorationData(DictWrapper):
    asset: str
    sku_id: Snowflake
    expires_at: int

class User(DictWrapper):
    id: Snowflake
    username: str
    discriminator: str
    display_name: str
    global_name: str
    avatar: str
    clan: Any
    bot: bool
    system: bool # This is useless x)
    mfa_enabled: bool
    verified: bool
    email: str
    locale: str
    flags: int
    banner: str
    banner_color: int
    accent_color: int
    premium_type: int
    public_flags: int
    primary_guild: str
    avatar_decoration_data: AvatarDecorationData
    _api = None