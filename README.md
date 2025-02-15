# Mini RP2350 board for Digital Video

The RP2350's HSTX peripheral supports TMDS encoding, as needed for HDMI/DVI video.

The idea of this board is to provide a minimal board in a similar form factor to the Pico 2, but with an HDMI connector on it, to allow experimenting with HSTX and digital video.

![image_720](https://github.com/user-attachments/assets/a6ff67bf-fb8c-44f8-9487-60a8524ab704)

My [DVI for HSTX](https://github.com/MichaelBell/dvhstx) library should be ideal for use with this board.

## Pinout

The left side is the same as the Pico, the right side is different (but somewhat related).

| Left Side | Right Side |
| --------- | ---------- |
| GPIO 0    | VBUS       |
| GPIO 1    | HDMI 5V    |
| Ground    | Ground     |
| GPIO 2    | Not connected |
| GPIO 3    | +3V3       |
| GPIO 4    | GPIO 29 (ADC) |
| GPIO 5    | GPIO 28 (ADC) |
| Ground    | Ground     |
| GPIO 6    | GPIO 23    |
| GPIO 7    | GPIO 22    |
| GPIO 8    | SWD        |
| GPIO 9    | SWCLK      |
| Ground    | Ground     |
| GPIO 10   |            |
| GPIO 11   |            |
| HDMI HPD  |            |
