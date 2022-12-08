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
from mesh.cdb.node import element as cdb


class Element(Codable):

    def __init__(self, element: Optional[dict] = None):
        self.name = 'Element'
        self.index = 0
        self.location = 0
        self.models = []
        if element:
            self.decode(element)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return

        for k, v in data.items():
            if k == cdb.NAME:
                self.name = v

            elif k == cdb.INDEX:
                self.index = v

            elif k == cdb.LOCATION:
                self.location = int(v, 16)

            elif k == cdb.MODELS:
                from mesh.model.node.element.model import Model
                self.models = [Model(model=m) for m in v]

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        """
        Remember to add news
        """
        data = dict()
        data[cdb.NAME] = self.name
        data[cdb.INDEX] = self.index
        data[cdb.LOCATION] = '%04X' % self.location
        data[cdb.MODELS] = [model.encode() for model in self.models]
        return data
