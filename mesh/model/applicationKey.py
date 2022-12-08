# Copyright (c) 2022, Nordic Semiconductor
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this
#    list of conditions and the following disclaimer in the documentation and/or
#    other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import uuid

from typing import Optional
from mesh.model import Codable
from mesh.cdb import appKey as cdb


class ApplicationKey(Codable):
    def __init__(self, index: Optional[int] = 0, app_key: Optional[dict] = None):
        self.name = 'App Key'
        self.index = index
        self._key = uuid.uuid4()
        self._oldKey = None
        self.boundNetKey = 0
        if app_key:
            self.decode(app_key)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.NAME:
                self.name = v
            elif k == cdb.INDEX:
                self.index = v
            elif k == cdb.KEY:
                self._key = uuid.UUID(v)
            elif k == cdb.OLD_KEY:
                self._oldKey = uuid.UUID(v)
            elif k == cdb.BOUND_NET_KEY:
                self.boundNetKey = v
            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.NAME] = self.name
        data[cdb.INDEX] = self.index
        data[cdb.KEY] = self._key.hex.upper()
        if self._oldKey:
            data[cdb.OLD_KEY] = self._oldKey.hex.upper()
        data[cdb.BOUND_NET_KEY] = self.boundNetKey
        return data

    @property
    def key(self):
        return self._key

    @property
    def oldKey(self):
        return self._oldKey
