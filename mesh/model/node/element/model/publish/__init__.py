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
from mesh.cdb.node.element.model import publish as cdb
from mesh.model.meshAddress import MeshAddress
from mesh.model.node.element.model.publish.period import Period
from mesh.model.node.element.model.publish.retransmit import Retransmit


class Publication(Codable):

    def __init__(self, publish: Optional[dict] = None):
        self.address = MeshAddress()
        self.index = 0
        self.ttl = 0
        self.period = Period()
        self.retransmit = Retransmit()
        self.credentials = 0
        if publish:
            self.decode(publish)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return

        for k, v in data.items():
            if k == cdb.ADDRESS:
                self.address = MeshAddress(hex_=v)

            elif k == cdb.INDEX:
                self.index = v

            elif k == cdb.TTL:
                self.ttl = v

            elif k == cdb.PERIOD:
                self.period = Period(period=v)

            elif k == cdb.RETRANSMIT:
                self.retransmit = Retransmit(retransmit=v)

            elif k == cdb.CREDENTIALS:
                self.credentials = v

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        """
        Remember to add news
        """
        data = dict()
        data[cdb.ADDRESS] = self.address.hex
        data[cdb.INDEX] = self.index
        data[cdb.TTL] = self.ttl
        data[cdb.PERIOD] = self.period.encode()
        data[cdb.RETRANSMIT] = self.retransmit.encode()
        data[cdb.CREDENTIALS] = self.credentials
        return data
