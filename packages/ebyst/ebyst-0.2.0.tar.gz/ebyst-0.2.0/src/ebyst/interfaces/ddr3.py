# Copyright (c) 2024 Sijmen Woutersen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from bitarray import bitarray

from ..device import Pin

class DDR3:
    def __init__(self, ctl,
                 RESETn: Pin, 
                 CK: (Pin, Pin),
                 CKE: (Pin, Pin),
                 CSn: (Pin, Pin),
                 CASn: Pin,
                 RASn: Pin,
                 WEn: Pin,
                 A: [Pin],
                 BA: [Pin],
                 DQ: [Pin],
                 DQS: [(Pin, Pin)],
                 ODT: [Pin],
                 DM: [Pin]):
        self.ctl = ctl
        self.RESETn = RESETn
        self.CK = CK
        self.CKE = CKE
        self.CSn = CSn
        self.RASn = RASn
        self.CASn = CASn
        self.WEn = WEn
        self.A = A
        self.BA = BA
        self.DQ = DQ
        self.DQS = DQS
        self.ODT = ODT
        self.DM = DM

    async def cmd_cycle(self, cycle_dqs=False, **pins):
        for name, value in pins.items():
            o = getattr(self, name)
            if isinstance(o, list) or isinstance(o, tuple):
                for i in range(len(o)):
                    o[i].set_value(int(value[i]))
            else:
                o.set_value(int(value))
        self.CK[0].set_value(0)
        self.CK[1].set_value(1)
        if cycle_dqs:
            self.DQS[0].set_value(0)
            self.DQS[1].set_value(1)
        await self.ctl.cycle()
        await self.ctl.cycle()
        self.CK[0].set_value(1)
        self.CK[1].set_value(0)
        if cycle_dqs:
            self.DQS[0].set_value(1)
            self.DQS[1].set_value(0)
        await self.ctl.cycle()
        await self.ctl.cycle()
        self.CK[0].set_value(0)
        self.CK[1].set_value(1)
        if cycle_dqs:
            self.DQS[0].set_value(0)
            self.DQS[1].set_value(1)
        self.RASn.set_value(1)
        self.CASn.set_value(1)
        self.WEn.set_value(1)
        for CSn in self.CSn:
            CSn.set_value(1)

    async def init(self):
        self.RESETn.output_enable(True)
        self.RESETn.set_value(0)
        self.CK[0].output_enable(True)
        self.CK[1].output_enable(True)
        self.CK[0].set_value(1)
        self.CK[1].set_value(0)
        for CKE in self.CKE:
            CKE.output_enable(True)
            CKE.set_value(0)
        for CSn in self.CSn:
            CSn.output_enable(True)
            CSn.set_value(1)
        for DQ in self.DQ:
            DQ.output_enable(False)
        for DQS in self.DQS:
            DQS.output_enable(False)
        for A in self.A:
            A.output_enable(True)
        for BA in self.BA:
            BA.output_enable(True)
        self.RASn.output_enable(True)
        self.RASn.set_value(1)
        self.CASn.output_enable(True)
        self.CASn.set_value(1)
        self.WEn.output_enable(True)
        self.WEn.set_value(1)
        for ODT in self.ODT:
            ODT.output_enable(True)
            ODT.set_value(0)
        await self.cmd_cycle()
        self.RESETn.set_value(1)
        await self.cmd_cycle()
        await self.cmd_cycle()
        await self.cmd_cycle()
        await self.cmd_cycle()
        await self.cmd_cycle()
        for CKE in self.CKE:
            CKE.set_value(1)
        await self.cmd_cycle()

        # mr2
        mr2 = bitarray("0" * len(self.A))
        mr2[3:6] = bitarray("100") # CWL = 6
        await self.cmd_cycle(CSn="00", RASn=0, CASn=0, WEn=0, BA="010"[::-1], A=mr2)
        for i in range(4): await self.cmd_cycle()
        # mr3
        mr3 = bitarray("0" * len(self.A))
        await self.cmd_cycle(CSn="00", RASn=0, CASn=0, WEn=0, BA="011"[::-1], A=mr3)
        for i in range(4): await self.cmd_cycle()
        # mr1
        mr1 = bitarray("0" * len(self.A))
        mr1[0] = 1 # DLL = Disable
        mr1[3:5] = bitarray("00") # AL = 0
        await self.cmd_cycle(CSn="00", RASn=0, CASn=0, WEn=0, BA="001"[::-1], A=mr1)
        for i in range(4): await self.cmd_cycle()
        # mr0
        mr0 = bitarray("0" * len(self.A))
        mr0[0:2] = bitarray("00") # BL = Fixed BL8
        mr0[3] = 0 # BT = Sequential
        mr0[4:7] = bitarray("010") # CL = 6
        mr0[8] = 0 # DLL
        mr0[9:12] = bitarray("010") # WR = 6
        mr0[12] = 0 # PD
        await self.cmd_cycle(CSn="00", RASn=0, CASn=0, WEn=0, BA="000"[::-1], A=mr0)
        for i in range(12): await self.cmd_cycle()



    async def read(self, ba="000"):
        await self.cmd_cycle(CSn="00", RASn=0, BA=ba[::-1], A="0000010000000000"[::-1])
        await self.cmd_cycle(CSn="00", CASn=0, BA=ba[::-1], A="0000010000000000"[::-1])
        
        for i in range(10):
            await self.cmd_cycle()
        await self.cmd_cycle(CSn="00", RASn=0, WEn=0, BA="000"[::-1], A="0000010000000000"[::-1])

    async def write(self):
        await self.cmd_cycle(CSn="00", RASn=0, BA="000"[::-1], A="0000010000000000"[::-1])
        await self.cmd_cycle(CSn="00", CASn=0, WEn=0, BA="000"[::-1], A="0000010000000000"[::-1])
        for i in range(4):
            await self.cmd_cycle()
            
        for i, DQ in enumerate(self.DQ):
            DQ.output_enable(True)
            DQ.set_value(i & 1)
        for DQS in self.DQS:
            DQS.output_enable(True)

        for i in range(5):
            await self.cmd_cycle(cycle_dqs=True)

        for DQ in self.DQ:
            DQ.output_enable(False)
        for DQS in self.DQS:
            DQS.output_enable(False)
        
        await self.cmd_cycle()
        await self.cmd_cycle(CSn="00", RASn=0, WEn=0, BA="000"[::-1], A="0000010000000000"[::-1])
        await self.cmd_cycle()

    async def stuff(self):
        await self.read("000")
        for i in range(10): await self.cmd_cycle()
        await self.read("001")
        for i in range(10): await self.cmd_cycle()
        await self.read("010")
        for i in range(10): await self.cmd_cycle()
        await self.read("011")
        for i in range(10): await self.cmd_cycle()
        await self.read("100")
        for i in range(10): await self.cmd_cycle()
        # await self.write("001")
        # for i in range(10): await self.cmd_cycle()
        # await self.read()
        # for i in range(10): await self.cmd_cycle()
