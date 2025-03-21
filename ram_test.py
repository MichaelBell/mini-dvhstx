from machine import Pin
import time
import random

@rp2.asm_pio(out_shiftdir=0, autopull=True, pull_thresh=8, autopush=True, push_thresh=8, sideset_init=(rp2.PIO.OUT_LOW,), out_init=rp2.PIO.OUT_LOW)
def spi_cpha0():
    out(pins, 1)             .side(0x0)
    in_(pins, 1)             .side(0x1)

class PIOSPI:
    def __init__(self, sm_id, pin_mosi, pin_miso, pin_sck, freq=1000000):
        self._sm = rp2.StateMachine(sm_id, spi_cpha0, freq=2*freq, sideset_base=Pin(pin_sck), out_base=Pin(pin_mosi), in_base=Pin(pin_miso))
        self._sm.active(1)
        Pin(pin_miso, Pin.IN)

    @micropython.native
    def write(self, wdata):
        first = True
        for b in wdata:
            self._sm.put(b, 24)
            if not first:
                self._sm.get()
            else:
                first = False
        self._sm.get()
        
    def read(self, n):
        return self.write_read_blocking([0,]*n)

    @micropython.native
    def readinto(self, rdata):
        self._sm.put(0)
        for i in range(len(rdata)-1):
            self._sm.put(0)
            rdata[i] = self._sm.get()
        rdata[-1] = self._sm.get()

    @micropython.native
    def write_read_blocking(self, wdata):
        rdata = bytearray(len(wdata))
        i = -1
        for b in wdata:
            self._sm.put(b, 24)
            if i >= 0:
                rdata[i] = self._sm.get()
            i += 1
        rdata[i] = self._sm.get()
        return rdata


def test_psram(spi, sel):

    sel.on()

    CMD_WRITE = 0x02
    CMD_READ = 0x03

    def spi_cmd(data, sel, dummy_len=0, read_len=0):
        dummy_buf = bytearray(dummy_len)
        read_buf = bytearray(read_len)
        
        sel.off()
        spi.write(bytearray(data))
        if dummy_len > 0:
            spi.readinto(dummy_buf)
        if read_len > 0:
            spi.readinto(read_buf)
        sel.on()
        
        return read_buf

    def spi_cmd2(data, data2, sel):
        sel.off()
        spi.write(bytearray(data))
        spi.write(data2)
        sel.on()

    buf = bytearray(8)
    
    for j in range(1024):
        addr = random.randint(0, 8 * 1024 * 1024 - 8)
        for i in range(8):
            buf[i] = random.randint(0, 255)

        spi_cmd2([CMD_WRITE, addr >> 16, (addr >> 8) & 0xFF, addr & 0xFF], buf, sel)
        data = spi_cmd([CMD_READ, addr >> 16, (addr >> 8) & 0xFF, addr & 0xFF], sel, 0, 8)

        for i in range(8):
            if buf[i] != data[i]:
                raise Exception(f"Error {buf[i]} != {data[i]} at addr {addr}+{i}")
            
    print("PSRAM OK")

sel = Pin(0, Pin.OUT, value=1)
spi = PIOSPI(0, 2, 3, 1, freq=15000000)

test_psram(spi, sel)

sel = Pin(6, Pin.OUT, value=1)
spi = PIOSPI(0, 8, 9, 7, freq=15000000)

test_psram(spi, sel)
