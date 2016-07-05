# -*- coding: utf-8 -*-
#
# Copyright © 2016 Igor Gnatenko <ignatenko@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import collections

from .base import Base
from . import utils

class Chroot(Base):
    __endpoint__ = "/api_2/mock_chroots/{0.name!s}"

    def __init__(self, client, name):
        """
        :param aiocopr.client.Client: COPR client
        :param str name: Chroot name
        """
        super().__init__(client)
        self.name = name
        self.os_release = None
        self.os_version = None
        self.arch = None
        self.is_active = None

    @classmethod
    def deserialize(cls, client, **kwargs):
        chroot = cls(client, None)
        chroot._update(**kwargs) # pylint: disable=protected-access
        return chroot

    def _update(self, **kwargs):
        self.name = kwargs["name"]
        self.os_release = kwargs["os_release"]
        self.os_version = kwargs["os_version"]
        self.arch = kwargs["arch"]
        self.is_active = kwargs["is_active"]
        self._initialized = True

    async def refresh(self):
        async with self.session.get(self.endpoint) as resp:
            kwargs = await resp.json()
        self._update(**kwargs["chroot"])

    def __repr__(self):
        return "<Chroot: {0!r} ({1!s})>".format(self.name, utils.bool2str(self.is_active))

class Chroots(Base, collections.abc.Mapping):
    __endpoint__ = "/api_2/mock_chroots"

    class KeysView(collections.abc.KeysView):
        def __repr__(self):
            return "<Chroots: {}>".format(", ".join([repr(x) for x in self]))

    def __init__(self, client, active_only=True):
        """
        :param aiohttp.client.Client client: COPR client
        :param bool active_only: Show only acrive chroots
        """
        super().__init__(client)
        self.active_only = active_only
        self.chroots = None

    async def refresh(self):
        params = {"active_only": self.active_only}
        async with self.session.get(self.endpoint, params=params) as resp:
            kwargs = await resp.json()
        chroots = {}
        for raw_chroot in kwargs["chroots"]:
            chroot = Chroot.deserialize(self._client, **raw_chroot["chroot"])
            chroots[chroot.name] = chroot
        self.chroots = collections.OrderedDict(sorted(chroots.items()))
        self._initialized = True

    def __getitem__(self, key):
        return self.chroots[key]

    def __iter__(self):
        for i in self.chroots.__iter__():
            yield i

    def __len__(self):
        return len(self.chroots)

    def keys(self):
        return self.KeysView(self)
