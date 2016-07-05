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

import urllib

class Base(object):
    __endpoint__ = None

    def __init__(self, client):
        self._client = client
        self._initialized = False

    @property
    def initialized(self):
        return self._initialized

    @property
    def endpoint(self):
        return urllib.parse.urljoin(self._client.url, self.__endpoint__.format(self))

    @property
    def session(self):
        return self._client.session
