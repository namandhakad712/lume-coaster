# lume-coaster — KiCad Netlist & Pin Map

**Board:** 2-layer baseboard, 85 × 40 mm, for the Tuya T5AI-Core (T5-E1 module)
**Scope:** display + buttons + chime trigger + a single-cell LiPo battery
supply that feeds the module's own onboard charge path. The T5AI-Core already
provides USB-C in, LiPo charging, and 5 V / 3.3 V regulation; this board adds
a battery and a software-visible power path, and does **not** re-regulate.

> **READ FIRST — two things you must verify before routing.**
> 1. The T5-E1 module has 70 pins; the T5AI-Core board maps a subset onto a 44-pin header. The netlist below is written against **module pin names (P-numbers)**, which are certain. The **header position** (which P-number sits at position 1…44) is NOT — fill it in from the official T5AI-Core pinout PDF, then update the "Header pos" column.
> 2. Every signal pin below must be confirmed as *actually broken out* on the 44-pin header. The docs say the header exposes GPIO/UART/SPI/I2C, so these should all be present, but verify each one. If a pin is missing, use the fallback column.

---

## 1. Reference designators & BOM

| Ref | Value / Part | Footprint | Purpose |
|---|---|---|---|
| J1 | 2×22 female header socket, 2.54 mm | 2.54mm 2×22 SMT/TH | T5AI-Core seats here (the brain) |
| J2 | 9-pin male header, 2.54 mm | 2.54mm 1×9 | Display ribbon / Dupont to ILI9341 |
| J3 | 3-pin male header, 2.54 mm | 2.54mm 1×3 | Chime trigger: 5 V, TRIG, GND |
| J4 | JST-PH 2-pin, 2.0 mm | SMD, right-angle | **LiPo battery input** |
| J5 | USB-C 16-pin, 2.0 mm | SMD | **USB-C charge / 5 V input** |
| SW1 | Tactile button 6×6 mm | 6x6x4.3 SMD | MODE |
| SW2 | Tactile button 6×6 mm | 6x6x4.3 SMD | UP (+) |
| SW3 | Tactile button 6×6 mm | 6x6x4.3 SMD | DOWN (−) |
| Q1 | AO3401 or SI2301 P-MOS | SOT-23 | Backlight high-side switch |
| Q2 | SI2301 / AO3401 P-MOS | SOT-23 | **Battery → load switch (V Batt power path)** |
| D1 | SS14 or similar Schottky, 40 V/1 A | SMA | **USB-C 5 V → rail, reverse-block** |
| R1 | 10 kΩ | 0805 | Q1 gate pull-up → +3V3 (default OFF, boot-safe) |
| R2 | 100 Ω | 0805 | Q1 gate series resistor from GPIO |
| R3 | 10 kΩ | 0805 | SW1 pull-up |
| R4 | 10 kΩ | 0805 | SW2 pull-up |
| R5 | 10 kΩ | 0805 | SW3 pull-up |
| R6 | 1 kΩ | 0805 | Chime trigger series resistor |
| R7 | 4.7 kΩ | 0805 | Chime trigger pull-down (boot glitch suppression) |
| R8 | 100 kΩ | 0805 | **Q2 gate pull-up (default OFF — battery ships safe)** |
| R9 | 100 kΩ | 0805 | **Battery voltage divider, top** |
| R10 | 100 kΩ | 0805 | **Battery voltage divider, bottom (→ ADC)** |
| C1 | 100 µF, 6.3 V | Electrolytic SMD | Bulk decoupling at J2 |
| C2 | 100 nF | 0805 | Local decoupling at J2 |
| C3 | 100 nF | 0805 | SW1 debounce |
| C4 | 100 nF | 0805 | SW2 debounce |
| C5 | 100 nF | 0805 | SW3 debounce |
| C6 | 10 µF, 10 V | 0805 | **Decoupling at the battery input** |
| C7 | 4.7 µF, 10 V | 0805 | **Decoupling on the USB-C 5 V input** |

All 0805 resistors/caps + SOT-23 + 2.54 mm headers are JLCPCB assembly-friendly and cheap. Total BOM ≈ $4–6.

---

## 2. Pin map — T5AI-Core (T5-E1) → carrier nets

| Net | Module pin | Alt functions (why it's safe) | Header pos | Fallback if not broken out |
|---|---|---|---|---|
| `SPI0_CS` | **P15** | SPI0_CSN (matches Tuya LCD example) | TBD | SPI1_CS = P3 |
| `SPI0_SCK` | **P14** | SPI0_SCK (matches example) | TBD | SPI1_SCK = P2 |
| `SPI0_MOSI` | **P16** | SPI0_MOSI (matches example) | TBD | SPI1_MOSI = P4 |
| `SPI0_MISO` | **P17** | SPI0_MISO (matches example) | TBD | SPI1_MISO = P5 |
| `LCD_DC` | **P12** | UART0_RTS / TOUCH0 / ADC14 → GPIO | TBD | P42, P43 |
| `LCD_RST` | **P13** | UART0_CTS / TOUCH1 / ADC15 → GPIO | TBD | P42, P43 |
| `LCD_BL_GATE` | **P24** | **PWMG0_PWM4** → PWM dimming bonus | TBD | P25 (no PWM) |
| `BTN_MODE` | **P25** | IRDA / ADC1 → GPIO input | TBD | P30, P31 |
| `BTN_UP` | **P4** | SPI1_MOSI / SDIO_DATA0 → GPIO input | TBD | P30, P31 |
| `BTN_DOWN` | **P5** | SPI1_MISO / SDIO_DATA1 → GPIO input | TBD | P30, P31 |
| `CHIME_TRIG` | **P3** | SPI1_CSN / SDIO_CMD → GPIO output | TBD | P2 |
| `BATT_EN` | **P30** | GPIO, no critical alt-fn → output | TBD | P31, P42 |
| `BATT_SENSE` | **P31** | ADC-capable → analog input | TBD | P42, P43 |

**Avoid — already used on the T5AI-Core board:** P0/P1 (UART1 serial debug to the USB-serial chip), P9 (onboard user LED / I2S0_DOUT audio), P29 (onboard user button), P6/P7/P8 (I2S0 audio to the onboard mic/speaker), RXD/TXD (UART0 download), P2 if used as fallback for SCK.

> **P30/P31 need the same verification as everything else** — confirm they're broken out on the 44-pin header and that P31 is on an ADC channel. If either is missing, fall back to P42/P43, and if those are gone too, drop `BATT_SENSE` (the divider can stay fitted, just tie the ADC end to GND via a 0 Ω) and hard-tie `BATT_EN` high instead of driving it.

**Why the backlight moved off the Tuya example's GPIO26:** the example uses GPIO28/GPIO26/GPIO9 for RST/BLK/RS. P9 is the user LED on an I2S0 audio line, and P26/P28 sit on QSPI0 — so all three are unsafe on this board. P24 buys you PWM dimming on top.

---

## 3. Netlist (by net)

### `+3V3`
| Node | Pin |
|---|---|
| J1 | 3.3 V power pins (from pinout) |
| J2 | pin 1 (VCC) |
| Q1 | source (SOT-23 pin 2) |
| R1 | one end (gate pull-up) |
| R3, R4, R5 | one end each (button pull-ups) |
| C1 | + |
| C2 | one end |

### `GND`
| Node | Pin |
|---|---|
| J1 | GND pins (from pinout) |
| J2 | pin 2 (GND) |
| J3 | pin 3 (GND) |
| SW1, SW2, SW3 | one terminal each |
| R7 | one end |
| C1 | − |
| C2, C3, C4, C5 | one end each |

### `+5V`
| Node | Pin |
|---|---|
| D1 | cathode (from USB-C) |
| J1 | 5 V power pin (from pinout) |
| J3 | pin 1 (5 V out to the chime circuit) |
| C7 | + (at the input) |

### `SPI0_CS`
| Node | Pin |
|---|---|
| J1 | P15 |
| J2 | pin 3 (CS) |

### `SPI0_SCK`
| Node | Pin |
|---|---|
| J1 | P14 |
| J2 | pin 7 (SCK) |

### `SPI0_MOSI`
| Node | Pin |
|---|---|
| J1 | P16 |
| J2 | pin 6 (SDI / MOSI) |

### `SPI0_MISO`
| Node | Pin |
|---|---|
| J1 | P17 |
| J2 | pin 9 (SDO / MISO — leave NC at the display if unused) |

### `LCD_DC`
| Node | Pin |
|---|---|
| J1 | P12 |
| J2 | pin 5 (DC / RS) |

### `LCD_RST`
| Node | Pin |
|---|---|
| J1 | P13 |
| J2 | pin 4 (RESET) |

### `LCD_BL_GATE`
| Node | Pin |
|---|---|
| J1 | P24 |
| R2 | one end |

### `LCD_BL`
| Node | Pin |
|---|---|
| Q1 | drain (SOT-23 pin 3) |
| R1 | other end → +3V3 |
| R2 | other end → Q1 gate (SOT-23 pin 1) |
| J2 | pin 8 (LED) |

> Q1 is a **high-side P-MOS switch**: source to +3V3, drain to the display's LED pin, gate pulled to +3V3 by R1. The GPIO pulls the gate low **through R2** to turn the backlight on. This makes the backlight **default OFF** during the T5-E1's ~5 ms boot glitch (datasheet warns GPIOs can float high at startup) — and PWM on P24 gives you dimming for free. If you skip dimming, depopulate Q1/R1/R2 and put a 0 Ω jumper from +3V3 to `LCD_BL`.

### `BTN_MODE`
| Node | Pin |
|---|---|
| J1 | P25 |
| R3 | other end → +3V3 |
| C3 | other end → GND |
| SW1 | other terminal → GND |

### `BTN_UP`
| Node | Pin |
|---|---|
| J1 | P4 |
| R4 | other end → +3V3 |
| C4 | other end → GND |
| SW2 | other terminal → GND |

### `BTN_DOWN`
| Node | Pin |
|---|---|
| J1 | P5 |
| R5 | other end → +3V3 |
| C5 | other end → GND |
| SW3 | other terminal → GND |

### `CHIME_TRIG`
| Node | Pin |
|---|---|
| J1 | P3 |
| R6 | one end |

### `CHIME_TRIG_OUT`
| Node | Pin |
|---|---|
| R6 | other end |
| R7 | other end → GND |
| J3 | pin 2 (TRIG) |

> R6 isolates the MCU from the chime circuit; R7 holds the line low so a boot glitch can't fire it. J3 pairs TRIG with 5 V and GND so the chime gets power + trigger from one connector.

---

## 3b. Power nets — the battery supply

The T5AI-Core already carries the ETA6003 (USB-C + LiPo charging), an LN2220PAR
5 V boost, and an RY3408 3.3 V buck. This board does **not** duplicate any of
that. It adds a battery, a power path the module can control, and a way to
read the battery.

### `VBATT` — battery input net
| Node | Pin |
|---|---|
| J4 | pin 1 (+) |
| C6 | + |
| R9 | top of divider |

### `GND`
| Node | Pin |
|---|---|
| J4 | pin 2 (−) |
| C6 | − |
| R10 | bottom of divider |

### `BATT_SENSE` — divided battery voltage → ADC
| Node | Pin |
|---|---|
| R9 | bottom of divider |
| R10 | top of divider |
| J1 | P31 |

> **R9 = R10 = 100 kΩ** halves the cell voltage: 4.2 V → 2.1 V, 3.0 V → 1.5 V.
> Well inside a 3.3 V ADC's range across the whole cell curve. Divider draw is
> ~21 µA at full charge — small enough to leave fitted, but if the module will
> sleep for days, gate the divider with the same `BATT_EN` net instead of
> leaving it across the cell.

### `BATT_EN` — battery-discharge enable → Q2 gate
| Node | Pin |
|---|---|
| J1 | P30 |
| R8 | one end |
| R8 | other end → `VBATT` |

> Q2 is a **P-MOS high-side switch between `VBATT` and the module's battery
> input pin**, gate pulled up to `VBATT` by R8 — so the battery is
> **disconnected by default**. That's the point: the module drives P30 low to
> connect the battery. A board that ships with the battery live and the
> module asleep is a board that arrives flat. It also means a stuck or
> glitching GPIO can't drain the cell during shipping — the default state is
> off.
>
> **Verify before routing:** confirm the module's battery-in pin is exposed on
> the 44-pin header. If the T5AI-Core already feeds its ETA6003 from the
> header's own `VBAT` pin, then Q2 sits in series with that pin — correct.
> If the module's charging is entirely internal with no battery pin on the
> header, then this board's battery *cannot* feed it, and the honest fix is
> to make J4 a raw `VBATT` output header for off-board loads and drop Q2.

### `VBUS_5V` — USB-C input net
| Node | Pin |
|---|---|
| J5 | VBUS pins (A4, B9, A9, B4 — tie all four) |
| D1 | anode |
| C7 | + |
| J1 | 5 V pin |

### `GND` (again)
| Node | Pin |
|---|---|
| J5 | GND pins (A1, B12, A12, B1 — tie all four) |
| C7 | − |
| D1 | cathode → `+5V` |

> **D1 is a series Schottky from USB-C into the +5V rail.** Two jobs: it stops
> the battery from trying to drive backwards out the USB port, and it drops
> ~0.3 V so a 5.0 V charger delivers ~4.7 V to the rail — still fine for the
> module's own regulators. Use a Schottky, not a silicon diode; a 1N4148 would
> drop 0.7 V and turn into a small heater at charge current.
>
> **USB-C gotcha — the most common first-board mistake here.** A USB-C
> receptacle will not source 5 V unless the host sees a pull-down on CC1/CC2.
> Fit **two 5.1 kΩ resistors, one from CC1 to GND and one from CC2 to GND**.
> Add them to the BOM as R11/R12 if you go this way. Without them you plug it
> in and nothing happens, and it takes an hour to figure out why.

---

## 4. Display connector J2 pinout (matches standard ILI9341 SPI module order)

| J2 pin | Net | ILI9341 module pin |
|---|---|---|
| 1 | +3V3 | VCC |
| 2 | GND | GND |
| 3 | SPI0_CS | CS |
| 4 | LCD_RST | RESET |
| 5 | LCD_DC | DC / RS |
| 6 | SPI0_MOSI | SDI / MOSI |
| 7 | SPI0_SCK | SCK |
| 8 | LCD_BL | LED |
| 9 | SPI0_MISO | SDO / MISO |

Get a **3.3 V** module, not a 5 V-only one. Verify the module's own pin order against its listing before you finalize the ribbon mapping — vendor orders differ, and getting VCC/GND swapped is the fastest way to kill a panel.

---

## 5. Schematic notes & gotchas

1. **No duplicate regulation.** The T5AI-Core already has the ETA6003 (USB-C + LiPo charging), the LN2220PAR 5 V boost, and the RY3408 3.3 V buck. This board's battery feeds the module's own charge path through Q2; USB-C comes in through D1 to the +5V rail. Do not add a second 3.3 V regulator — that only creates a ground loop and a second part that can be wrong.
2. **Confirm the RY3408 3.3 V rail can supply the display.** An ILI9341 with backlight is typically 20–50 mA — almost certainly fine, but the datasheet doesn't give the rail's rating, so don't assume; measure the backlight current of your specific module first.
3. **Keep SPI traces short and same-length.** SCK/MOSI/CS should be roughly equal length, < 50 mm, with a ground via nearby. At 24–40 MHz, sloppy routing gives you a blank screen and no obvious cause.
4. **MISO is optional.** Many ILI9341 breakouts leave SDO unpopulated. If you never read from the display, cut the net — but keep the pad so you can populate it for reading the ID register during bring-up.
5. **The antenna end is sacred.** The T5AI-Core's onboard antenna needs ≥ 15 mm clearance from metal. Route J2, the buttons, and all copper to the opposite end of the board. Do not put a ground pour under the antenna region. **This includes the battery** — a LiPo pouch is a metal object. Keep J4 at the far end from the antenna, and spec the battery lead long enough to reach.
6. **Pull-ups, not pull-downs, for buttons.** GPIOs idle high, press = low. The 10 kΩ pull-ups also keep the lines defined during boot.
7. **Add a silkscreen label for every net** on both ends of every jumper — you will thank yourself at bring-up.
8. **LiPo safety is not optional.** The cell must be a protected cell, or you must include protection on the board. The ETA6003 on the module handles charge; **it does not handle over-discharge of an external cell unless its protection pins are wired to your cell**. If the module's protection is internal to its own cell pad only, then the honest options are (a) use a protected single cell, or (b) add a DW01 + FS8205A protection IC on this board between J4 and Q2. Decide before routing; (b) is two tiny parts and ~$0.20 and removes the only real safety question on the board.
9. **The USB-C CC pulldowns are the whole game.** See the note in §3b — two 5.1 kΩ on CC1/CC2, no exceptions, or the port does nothing.

---

## 6. Layout constraints (2-layer)

- **Stackup:** top = components + signals, bottom = ground plane. Keep the bottom plane as unbroken as possible; if you must route on it, use short orthogonal stubs with ground vias at each end.
- **Board size target:** ~85 × 40 mm. The T5AI-Core is 73 × 29 mm; the extra width is for the connectors, and the extra length for the chime header at the far (antenna-free) end.
- **Header placement:** put J1 so the seated T5AI-Core's **antenna end overhangs the board edge** — that keeps it as far from your copper as physically possible.
- **Power path is short and wide:** J4 → Q2 → module battery pin, and J5 → D1 → +5V rail. 20 mil minimum for anything carrying battery or USB current; 6 mil is fine for signals.
- **Clearances:** 6 mil trace / 6 mil clearance minimum for JLCPCB. Don't go finer; you don't need to.
- **Vias:** 0.3 mm hole / 0.6 mm pad. Sprinkle ground vias around the SPI connector, Q1, and Q2.
- **Mounting:** 4× M3 holes at the corners of the *non-antenna* end only. On the antenna end use a plastic clip or nothing.

---

## 7. Pre-order verification checklist

- [ ] Download the official **T5AI-Core pinout PDF** and fill in the "Header pos" column
- [ ] Confirm all 13 signal pins (P3, P4, P5, P12, P13, P14, P15, P16, P17, P24, P25, P30, P31) are broken out on the 44-pin header
- [ ] Confirm **P31 is on an ADC channel** (for `BATT_SENSE`)
- [ ] Confirm the module exposes a **battery-in pin** on the header that actually reaches its ETA6003 — Q2 has to sit in series with it, or the battery supply can't feed the module at all
- [ ] Decide on LiPo protection: protected cell, or a DW01+FS8205A between J4 and Q2
- [ ] Confirm the 44-pin socket orientation matches the seated board (USB-C and switch face the right way)
- [ ] Confirm your ILI9341 module is 3.3 V and its pin order matches the J2 table
- [ ] **USB-C CC1 and CC2 each have a 5.1 kΩ to GND** (R11/R12)
- [ ] DRC passes, zero errors
- [ ] Board outline keeps all copper ≥ 15 mm from the seated antenna
- [ ] Battery connector J4 and the cell itself are at the far end from the antenna
- [ ] Silkscreen labels on every connector pin
- [ ] Run KiCad ERC and fix every warning (don't ignore "power pin not driven")

**Then order same-day from JLCPCB — transit + customs is the single biggest schedule risk.**
