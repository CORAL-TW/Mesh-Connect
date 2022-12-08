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


import os
import json
import shutil

from typing import Optional
from mesh.storage import Storage

_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'database')

_BULLPEN_DIR = os.path.join(_DB_DIR, 'bullpen')


def _database_file():
    # the first cdb file will be the database file
    for dir_path, _, file_names in os.walk(_DB_DIR):
        f = next(iter(file_names), None)
        return os.path.join(dir_path, f)
    return None


class LocalStorage(Storage):

    def load(self) -> Optional[dict]:
        db_file = _database_file()
        if db_file:
            with open(db_file, 'r') as f:
                return json.loads(f.read())
        return None

    def swap(self, profile: str) -> Optional[dict]:
        target = os.path.join(_BULLPEN_DIR, profile)
        if not os.path.exists(target):
            raise Exception('LocalStorage: target file not found')

        # move the database file to bullpen
        db_file = _database_file()
        if db_file:
            shutil.move(db_file, os.path.join(_BULLPEN_DIR, os.path.basename(db_file)))

        # make the target profile as database
        shutil.move(target, os.path.join(_DB_DIR, profile))

        return self.load()

    def save(self, data: dict) -> bool:
        # save to the first cdb file
        db_file = _database_file()
        if db_file:
            with open(db_file, '+w') as f:
                f.write(json.dumps(data, sort_keys=False, indent=2))
                return True
        return False
