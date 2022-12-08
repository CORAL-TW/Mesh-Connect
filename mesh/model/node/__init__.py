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
from mesh.model.address import Address
from mesh.model.security import Security
from mesh.model.node.features import Features
from mesh.model.node.networkTransmit import NetworkTransmit
from mesh.model.node.relayRetransmit import RelayRetransmit
from mesh.model.node.features import Features
from mesh.cdb import node as cdb


class Node(Codable):
    def __init__(self, node: Optional[dict] = None):
        self._uuid = uuid.uuid4()
        self.name = 'Node'
        self._deviceKey = None
        self.unicastAddress = Address(hex_='0')
        self.security = Security.SECURE
        self.cid = 0
        self.pid = 0
        self.vid = 0
        self.crpl = 0
        self.features = Features()
        self.elements = []
        self.configComplete = False
        self.netKeys = []
        self.appKeys = []
        self.networkTransmit = NetworkTransmit()
        self.relayTransmit = RelayRetransmit()
        self.secureNetworkBeacon = False
        self.defaultTTL = 3
        self.excluded = False
        self.heartbeatPub = None
        self.heartbeatSub = None
        if node:
            self.decode(node)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.UUID:
                self._uuid = uuid.UUID(v)

            elif k == cdb.NAME:
                self.name = v

            elif k == cdb.DEVICE_KEY:
                self._deviceKey = uuid.UUID(v)

            elif k == cdb.UNICAST_ADDRESS:
                self.unicastAddress = Address(hex_=v)

            elif k == cdb.SECURITY:
                self.security = v

            elif k == cdb.CID:
                self.cid = int(v, 16)

            elif k == cdb.PID:
                self.pid = int(v, 16)

            elif k == cdb.VID:
                self.vid = int(v, 16)

            elif k == cdb.CRPL:
                self.crpl = int(v, 16)

            elif k == cdb.FEATURES:
                self.features = Features(features=v)

            elif k == cdb.ELEMENTS:
                from mesh.model.node.element import Element
                self.elements = [Element(element=e) for e in v]

            elif k == cdb.CONFIG_COMPLETE:
                self.configComplete = v

            elif k == cdb.NET_KEYS:
                from mesh.model.node.networkKey import NetworkKey
                self.netKeys = [NetworkKey(net_key=n) for n in v]

            elif k == cdb.APP_KEYS:
                from mesh.model.node.applicationKey import ApplicationKey
                self.appKeys = [ApplicationKey(app_key=a) for a in v]

            elif k == cdb.NETWORK_TRANSMIT:
                self.networkTransmit = NetworkTransmit(transmit=v)

            elif k == cdb.RELAY_RETRANSMIT:
                self.relayTransmit = RelayRetransmit(transmit=v)

            elif k == cdb.SECURE_NETWORK_BEACON:
                self.secureNetworkBeacon = v

            elif k == cdb.DEFAULT_TTL:
                self.defaultTTL = v

            elif k == cdb.EXCLUDED:
                self.excluded = v

            elif k == cdb.HEARTBEAT_PUB:
                from mesh.model.node.heartbeatPub import HeartbeatPublication
                self.heartbeatPub = HeartbeatPublication(publish=v)

            elif k == cdb.HEARTBEAT_SUB:
                from mesh.model.node.heartbeatSub import HeartbeatSubscription
                self.heartbeatSub = HeartbeatSubscription(subscribe=v)

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.UUID] = str(self._uuid).upper()
        data[cdb.NAME] = self.name
        data[cdb.DEVICE_KEY] = self._deviceKey.hex.upper() if self._deviceKey else ''
        data[cdb.UNICAST_ADDRESS] = self.unicastAddress.hex
        data[cdb.SECURITY] = self.security
        data[cdb.CID] = '%04X' % self.cid
        data[cdb.PID] = '%04X' % self.pid
        data[cdb.VID] = '%04X' % self.vid
        data[cdb.CRPL] = '%04X' % self.crpl
        data[cdb.FEATURES] = self.features.encode()
        data[cdb.ELEMENTS] = [element.encode() for element in self.elements]
        data[cdb.CONFIG_COMPLETE] = self.configComplete
        data[cdb.NET_KEYS] = [netKey.encode() for netKey in self.netKeys]
        data[cdb.APP_KEYS] = [appKey.encode() for appKey in self.appKeys]
        data[cdb.NETWORK_TRANSMIT] = self.networkTransmit.encode()
        data[cdb.RELAY_RETRANSMIT] = self.relayTransmit.encode()
        data[cdb.SECURE_NETWORK_BEACON] = self.secureNetworkBeacon
        data[cdb.DEFAULT_TTL] = self.defaultTTL
        data[cdb.EXCLUDED] = self.excluded
        if self.heartbeatPub:
            data[cdb.HEARTBEAT_PUB] = self.heartbeatPub.encode()
        if self.heartbeatSub:
            data[cdb.HEARTBEAT_SUB] = self.heartbeatSub.encode()
        return data

    @property
    def uuid(self):
        return self._uuid

    @property
    def deviceKey(self):
        return self._deviceKey
