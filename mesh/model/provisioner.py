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
from mesh.cdb import provisioner as cdb


class Provisioner(Codable):
    def __init__(self, provisioner: Optional[dict] = None):
        self.provisionerName = 'Provisioner'
        self._uuid = uuid.uuid4()
        self.allocatedGroupRange = []
        self.allocatedUnicastRange = []
        self.allocatedSceneRange = []
        if provisioner:
            self.decode(provisioner)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.PROVISIONER_NAME:
                self.provisionerName = v

            elif k == cdb.UUID:
                self._uuid = uuid.UUID(v)

            elif k == cdb.ALLOCATED_GROUP_RANGE:
                from mesh.model.groupRange import GroupRange
                self.allocatedGroupRange = [GroupRange(range_) for range_ in v]

            elif k == cdb.ALLOCATED_UNICAST_RANGE:
                from mesh.model.unicastRange import UnicastRange
                self.allocatedUnicastRange = [UnicastRange(range_) for range_ in v]

            elif k == cdb.ALLOCATED_SCENE_RANGE:
                from mesh.model.sceneRange import SceneRange
                self.allocatedSceneRange = [SceneRange(range_) for range_ in v]

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.PROVISIONER_NAME] = self.provisionerName
        data[cdb.UUID] = str(self._uuid).upper()
        data[cdb.ALLOCATED_GROUP_RANGE] = [range_.encode() for range_ in self.allocatedGroupRange]
        data[cdb.ALLOCATED_UNICAST_RANGE] = [range_.encode() for range_ in self.allocatedUnicastRange]
        data[cdb.ALLOCATED_SCENE_RANGE] = [range_.encode() for range_ in self.allocatedSceneRange]
        return data

    @property
    def uuid(self):
        return self._uuid
