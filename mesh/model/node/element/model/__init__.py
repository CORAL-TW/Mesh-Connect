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


from typing import Optional
from mesh.model import Codable
from mesh.cdb.node.element import model as cdb
from mesh.model.meshAddress import MeshAddress


class Model(Codable):

    def __init__(self, model: Optional[dict] = None):
        self._modelId = 0
        self.publish = None
        self.bind = []
        self.subscribe = []
        if model:
            self.decode(model)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return

        for k, v in data.items():
            if k == cdb.MODEL_ID:
                self._modelId = int(v, 16)

            elif k == cdb.PUBLISH:
                from mesh.model.node.element.model.publish import Publication
                self.publish = Publication(publish=v)

            elif k == cdb.BIND:
                self.bind = [index for index in v]

            elif k == cdb.SUBSCRIBE:
                self.subscribe = [MeshAddress(hex_=address) for address in v]

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        """
        Remember to add news
        """
        data = dict()
        data[cdb.MODEL_ID] = '%04X' % self._modelId if self._modelId <= 65535 else '%08X' % self._modelId
        if self.publish:
            data[cdb.PUBLISH] = self.publish.encode()
        data[cdb.BIND] = [index for index in self.bind]
        data[cdb.SUBSCRIBE] = [address.hex for address in self.subscribe]
        return data

    @property
    def modelId(self):
        return self._modelId
