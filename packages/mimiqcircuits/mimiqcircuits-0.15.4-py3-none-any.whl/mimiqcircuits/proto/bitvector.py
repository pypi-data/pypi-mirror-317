#
# Copyright © 2022-2024 University of Strasbourg. All Rights Reserved.
# Copyright © 2032-2024 QPerfect. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from mimiqcircuits.proto import bitvector_pb2
from mimiqcircuits.proto.qcsrproto import bitvec_to_bytes, bytes_to_bitvec


def toproto_bitvector(bv):
    return bitvector_pb2.BitVector(len=len(bv), data=bytes(bitvec_to_bytes(bv)))


def fromproto_bitvector(bv):
    return bytes_to_bitvec(bv.data, bv.len)
