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

import asyncio
import configparser
import os

import aiohttp

from .chroot import Chroot, Chroots

DEFAULT_COPR_URL = "https://copr.fedorainfracloud.org/"

class Client(object):
    def __init__(self, login, token, url=DEFAULT_COPR_URL, loop=None):
        self.url = url
        self._loop = loop or asyncio.get_event_loop()
        self.__auth = aiohttp.BasicAuth(login, token)
        self._session = aiohttp.ClientSession(auth=self.__auth, loop=self._loop)

    @classmethod
    def from_config_file(cls, conf_file=None, loop=None):
        if conf_file is None:
            conf_file = os.path.join(os.path.expanduser("~"), ".config", "copr")
        config = configparser.ConfigParser()
        config.read(conf_file)
        return cls(config["copr-cli"]["login"], config["copr-cli"]["token"], loop=loop)

    def __del__(self):
        if not self._session.closed:
            self._session.close()

    @property
    def session(self):
        return self._session

    async def get_chroots(self, *args, **kwargs):
        chroots = Chroots(self, *args, **kwargs)
        await chroots.refresh()
        return chroots

    async def get_chroot(self, *args, **kwargs):
        chroot = Chroot(self, *args, **kwargs)
        await chroot.refresh()
        return chroot
