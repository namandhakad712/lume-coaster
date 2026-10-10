# lume-coaster — Zero-to-Gerber KiCad Guide (PURE NOOB)

> **How to use this:** open KiCad on one half of your screen, this guide on the other. Do one block at a time. Each block is 30–90 minutes of real design time; the whole run is roughly 6 hours end to end, including the mistakes.

---

## BLOCK 0 — Before you touch KiCad (15 min, do this first)

**0.1** Find your KiCad version: open KiCad → top menu **Help → About KiCad**. Remember the big number (7, 8, or 9). Everything below works on all of them, but the screenshots differ slightly.

**0.2** You need the **T5AI-Core pinout**. Go to the Tuya docs page for the T5AI-Core and download the pinout PDF/image. This is your bible for this project. Save it as `carrier-board/t5ai-pinout.pdf`.

**0.3** Look at your actual T5AI-Core board. **Do the gold pins stick OUT (male) or are there holes (female)?**
- Male pins sticking out → your carrier needs a **female socket** (this is the normal case, go with it)
- This decides the J1 footprint in Block 5. Write your answer here: `J1 gender: __________`

**0.4** Check the antenna. One short edge of the T5AI-Core has the onboard antenna (usually marked with a silkscreen antenna symbol or "ANT"). That edge must hang OFF the carrier board or stay 15mm from any copper. Note which edge it is relative to the USB-C port. Write it here: `Antenna is on the ________ end`

---

## BLOCK 1 — New project (5 min)

**1.1** Open the **KiCad** main window (the one with all the app icons in the middle).

**1.2** Top menu: **File → New Project**. Or the folder+ icon.

**1.3** A save box appears. Browse to your project folder, into `carrier-board`. Name it exactly:
```
lume-coaster
```
**1.4** Click **Save**. You'll see `lume-coaster.kicad_pro` appear.

**1.5** Back in the KiCad main window, click **"Schematic Editor"** (the icon that looks like a pencil drawing over a circuit schematic). A new window opens — this is where you draw the circuit.

> ✅ **Checkpoint:** you're looking at a mostly-empty page with a grid. Good.

---

## BLOCK 2 — Place the parts on the schematic (45-60 min)

The trick: **every part in KiCad is a "symbol". You add symbols by name.**

**2.1** Press the **A** key (or click the op-amp-looking icon on the right toolbar, tooltip "Add a symbol"). A search box pops up.

**2.2** Type this EXACTLY and hit Enter, then click once on the page:

| Search for | What it is | Where to drop it |
|---|---|---|
| `Connector_Generic:Conn_02x22_Odd_Even` | **J1** — the 44-pin socket the T5AI-Core plugs into | far left, vertical |
| `Connector_Generic:Conn_01x09` | **J2** — 9-pin display connector | top right |
| `Connector_Generic:Conn_01x03` | **J3** — 3-pin chime connector | bottom right |
| `Switch:SW_Push` | a button (place **three**: SW1, SW2, SW3) | middle, stacked |
| `Device:Q_PMOS_GDS` | **Q1** — the P-MOSFET | middle-right |
| `Device:R` | a resistor (place **seven**: R1–R7) | spread out |
| `Device:C` | a small cap (place **four**: C2, C3, C4, C5) | spread out |
| `Device:CP` | **C1** — the big electrolytic cap (polarized) | near J2 |
| `power:PWR_FLAG` | a power flag (place **three**) | top-left corner |

**2.3** After each placement, press **Esc** to stop placing.

**2.4** **MOVING:** hover over a symbol, press **M**, move, click to drop. **ROTATING:** hover, press **R** (keep pressing R to spin 90° at a time). Get them roughly spread out — tidy comes later.

**2.5** **GIVING THEM NAMES & VALUES.** Hover over R1 and press **V** (V = value). A box pops up. Type the value from the BOM below. Then hover again and press **Q** (Q = reference designator) and type `R1` if it's not already right.

**Full BOM with values — type each one in:**

| Ref | Value | Purpose |
|---|---|---|
| J1 | 2x22 socket | T5AI-Core seats here |
| J2 | 9-pin header | display ribbon |
| J3 | 3-pin header | chime: 5V, TRIG, GND |
| SW1 | 6x6 SMD tact | MODE |
| SW2 | 6x6 SMD tact | UP |
| SW3 | 6x6 SMD tact | DOWN |
| Q1 | AO3401 | backlight switch |
| R1 | 10k | Q1 gate pull-up |
| R2 | 100R | Q1 gate series |
| R3 | 10k | SW1 pull-up |
| R4 | 10k | SW2 pull-up |
| R5 | 10k | SW3 pull-up |
| R6 | 1k | chime trigger series |
| R7 | 4k7 | chime trigger pull-down |
| C1 | 100uF | bulk cap at display |
| C2 | 100nF | decoupling at display |
| C3 | 100nF | SW1 debounce |
| C4 | 100nF | SW2 debounce |
| C5 | 100nF | SW3 debounce |

> ✅ **Checkpoint:** you should see ~22 little boxes with values next to them, spread around the page. Ugly is fine. We are NOT making art yet.

---

## BLOCK 3 — Wire it up, the smart way (60-90 min)

**The noob cheat code: DO NOT draw long wires everywhere. Use NET LABELS.**

When two pins carry the same net label, KiCad considers them connected even if there's no wire between them. This is how professionals keep schematics readable.

**3.1** Draw a SHORT wire stub first: press **W** (W = wire). Click a pin, drag out a few mm, double-click to end. Press Esc.

**3.2** Now the label: find the **"Add a net label"** icon on the right toolbar (it looks like a small tag / name plate; hover the icons until the tooltip says "Add a net label"). Click it, type the net name, hit Enter, then click on the end of your wire stub. The label sticks there.

**3.3** These are all the net names you'll use — spell them EXACTLY like this:

```
+3V3   GND   +5V
SPI0_CS   SPI0_SCK   SPI0_MOSI   SPI0_MISO
LCD_DC   LCD_RST   LCD_BL_GATE   LCD_BL
BTN_MODE   BTN_UP   BTN_DOWN
CHIME_TRIG   CHIME_TRIG_OUT
```

**3.4** Here's what connects to what. For each row: put a label on the J1 pin, and the same label on the other component's pin.

### Power nets — use the special power symbols instead of labels
For `+3V3`, `+5V`, `GND`, add them with the symbol tool:
- Search `power:+3V3` → place 1 (drop it near the top-left)
- Search `power:+5V` → place 1
- Search `power:GND` → place 1
Then run a **W wire** from each power symbol to wherever it's needed. Every `+3V3` symbol anywhere on the page is automatically the same net. Same for GND. This is the cleanest part of KiCad — use it hard.

### The signal nets — J1 pin → label

> ⚠️ **THE ONE THING YOU MUST VERIFY:** which pin NUMBER on the 2x22 socket corresponds to which T5-E1 pin (P3, P4, P5, ...). Your T5AI-Core pinout PDF tells you. The module pin names below are correct; the socket position is what you're confirming. **When in doubt, ask me — do not guess.**

| Label | Goes on J1 pin... | ...and also on |
|---|---|---|
| `SPI0_CS` | the pin = module **P15** | J2 pin 3 |
| `SPI0_SCK` | the pin = module **P14** | J2 pin 7 |
| `SPI0_MOSI` | the pin = module **P16** | J2 pin 6 |
| `SPI0_MISO` | the pin = module **P17** | J2 pin 9 |
| `LCD_DC` | the pin = module **P12** | J2 pin 5 |
| `LCD_RST` | the pin = module **P13** | J2 pin 4 |
| `LCD_BL_GATE` | the pin = module **P24** | R2 (one end) |
| `BTN_MODE` | the pin = module **P25** | R3 + C3 + SW1 |
| `BTN_UP` | the pin = module **P4** | R4 + C4 + SW2 |
| `BTN_DOWN` | the pin = module **P5** | R5 + C5 + SW3 |
| `CHIME_TRIG` | the pin = module **P3** | R6 (one end) |

**J1 power pins:** wire the T5AI-Core's **3.3V pins** to a `+3V3` symbol, its **5V pin** to `+5V`, and **all its GND pins** to `GND`. (How many of each? The pinout PDF says — usually several GND.)

### Display connector J2 — label the 9 pins in order

| J2 pin | Label |
|---|---|
| 1 | `+3V3` |
| 2 | `GND` |
| 3 | `SPI0_CS` |
| 4 | `LCD_RST` |
| 5 | `LCD_DC` |
| 6 | `SPI0_MOSI` |
| 7 | `SPI0_SCK` |
| 8 | `LCD_BL` |
| 9 | `SPI0_MISO` |

### Chime connector J3

| J3 pin | Label |
|---|---|
| 1 | `+5V` |
| 2 | `CHIME_TRIG_OUT` |
| 3 | `GND` |

### The little circuits — draw these with actual wires

**Backlight switch (the only IC-ish thing here):**
- Q1 (P-MOS, SOT-23): pin **S** → `+3V3`, pin **D** → `LCD_BL`, pin **G** → R2's other end
- R1: one end to Q1's **G**, other end to `+3V3`
- So: gate is pulled HIGH = backlight OFF by default. The GPIO pulls it LOW through R2 to turn it ON. Boot-safe. 

**Each button (do this 3×):**
- One terminal → the net label (`BTN_MODE` etc.) AND a 10k resistor to `+3V3`
- Other terminal → `GND`
- 100nF cap across the same two terminals (that's the debounce)

**Chime trigger:**
- R6: one end `CHIME_TRIG`, other end `CHIME_TRIG_OUT`
- R7: one end `CHIME_TRIG_OUT`, other end `GND`
- `CHIME_TRIG_OUT` also goes to J3 pin 2

**Decoupling:**
- C1 (+) → `+3V3`, C1 (−) → `GND`
- C2: one end `+3V3`, other end `GND`

> ✅ **Checkpoint:** hover over a label — KiCad highlights everything on that net. Click J2 pin 3's `SPI0_CS` label and J1's `SPI0_CS` label should both light up. If they don't, the labels are spelled differently.

---

## BLOCK 4 — ERC: the "did you mess up" check (15-30 min)

**4.1** Top menu: **Inspect → Electrical Rules Checker**. Click **Run ERC**.

**4.2** You will probably get errors. It's fine, EVERYONE does. Fix them in this order:

- **"Power pin not driven"** on `+3V3` / `+5V` / `GND` → this is why we placed those three `PWR_FLAG` symbols in Block 2. Wire one PWR_FLAG to each of `+3V3`, `+5V`, `GND` (any spot). Re-run. This is the #1 noob error and it is NOT a real mistake in your circuit — KiCad just can't see that the T5AI-Core is the power source.
- **"Input pin not driven"** → you missed a connection. Click the error, KiCad jumps to the pin, draw the missing wire.
- **"Unconnected pin"** on a pin you don't use (like MISO if your display has no SDO pad) → right-click the pin → **Unconnect** or add a "no connect" X marker (the X icon on the right toolbar, hotkey **Q**... no — the X-looking icon, tooltip "Add a no-connection flag"). Click it on the unused pin.

**4.3** Goal: **0 errors**. Warnings are okay-ish but try to kill them all.

> ✅ **Checkpoint:** ERC says 0 errors. SCREENSHOT THIS. That's proof for your work log AND your future self.

---

## BLOCK 5 — Assign footprints: "how big is each part physically" (30 min)

**5.1** In the KiCad MAIN window (close or minimize the schematic for a sec), click **"Footprint Assignment"** — the icon that looks like a chip next to a PCB footprint. A table opens with all your parts on the left.

**5.2** For each row, click it, then in the search box (or the 3-dot browse button) find and assign:

| Ref | Footprint (search for exactly this) |
|---|---|
| J1 | `Connector_PinSocket_2.54mm:PinSocket_2x22_P2.54mm_Vertical` *(if your T5AI-Core has male pins — verify from Block 0.3!)* |
| J2 | `Connector_PinHeader_2.54mm:PinHeader_1x09_P2.54mm_Vertical` |
| J3 | `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical` |
| SW1-3 | `Button_Switch_SMD:SW_SPST_TL3305` *(then buy TL3305-style 6.2mm SMD switches)* |
| Q1 | `Package_TO_SOT_SMD:SOT-23` |
| R1-R7 | `Resistor_SMD:R_0805_2012Metric` |
| C2-C5 | `Capacitor_SMD:C_0805_2012Metric` |
| C1 | `Capacitor_SMD:CP_Elec_6.3x5.3` |

**5.3** Click **OK** / Apply. Close the window.

> ✅ **Checkpoint:** every row in that table has a footprint name next to it. None of them say "no footprint assigned".

---

## BLOCK 6 — Board outline: draw the physical board (30 min)

**6.1** Back in the KiCad MAIN window, click **"PCB Editor"** (the icon that looks like a green/black PCB). A new window opens. This is where the physical board lives.

**6.2** First, push your schematic into this board: top menu **Tools → Update PCB from Schematic** (or the icon with the double-arrow / "board gets updated from schematic" tooltip). A confirmation box appears — click **Update PCB**, then **Close**. All your parts appear in a clump near the middle.

**6.3** **Set the grid to 1 mm:** look at the top toolbar, there's a grid dropdown that probably says something like "0.2540 mm". Click it → select **1 mm**.

**6.4** **Select the board edge layer:** on the right side of the screen there's a layer list. Click **Edge.Cuts** (usually near the bottom, might be orange or grey). The name highlights.

**6.5** **Draw the outline:** on the right toolbar, click the **"Draw a rectangle"** icon (tooltip says it — if you only see "Draw a line", hold that button down and the rectangle option appears). Click once at roughly (0,0), then click again to make a rectangle about **85 mm wide × 40 mm tall**. You'll see the dimension readout as you drag.

**6.6** Doesn't have to be perfect. If you mess up: hover the line, press **Delete**, redraw.

> ✅ **Checkpoint:** there's a rectangle on the screen and all your parts are inside it (or near it). The rectangle IS your physical PCB.

---

## BLOCK 7 — Place the parts (45-60 min)

This is where it becomes a real product. Rules, in order of importance:

**7.1** **J1 goes at one LONG edge, and the antenna end hangs OFF the board.** Remember Block 0.4? The T5AI-Core's antenna end must be as far from your copper as possible. Place J1 so the seated T5AI-Core's antenna end pokes past the Edge.Cuts rectangle. If you can't overhang, keep the antenna end ≥15mm from every trace.

**7.2** **J2 (display) goes at the OPPOSITE end from the antenna**, near where the screen will physically sit.

**7.3** **J3 (chime) also at the non-antenna end.**

**7.4** **The 3 buttons** cluster at the front face where your thumb will reach — think the bottom edge of the wedge.

**7.5** **Q1, R1, R2** huddle next to J2 (short traces to the backlight pin).

**7.6** **Decoupling caps C1, C2** go as close to J2's power pins as physically possible. Like, touching-close. This actually matters for the screen to work.

**7.7** **Move:** hover a footprint, press **M**, click to drop. **Rotate:** hover, **R**. **Flip to the back of the board:** hover, **F** (you probably won't need this on a 2-layer board except maybe nothing — leave everything on the front).

**7.8** **Reference labels:** press **Ctrl+S** often. If KiCad asks about saving, yes.

> ✅ **Checkpoint:** it LOOKS like a board now. Parts are spread out, not overlapping. Take a screenshot.

---

## BLOCK 8 — Route the copper (90-120 min — this is the big one)

**8.1** **Set your design rules first.** Top menu **File → Board Setup** → left side click **Design Rules**. Set:
- **Minimum track width:** `0.15 mm`
- **Minimum clearance:** `0.15 mm`
- Click **OK**. (These are safe for JLCPCB's standard 2-layer service.)

**8.2** **Set your default track width.** Near the top toolbar there's a "Track width" dropdown — set it to `0.25 mm`. That's your signal trace. For power (`+3V3`, `+5V`, `GND`) bump it up to `0.5 mm` manually while routing those.

**8.3** **Route:** press **X** (X = route track). Click on a pad (a pin), drag to the pad it must reach, click. Press Esc when done with a net.

**8.4** Route in this order — easiest and most important first:
1. `GND` to everything — but ONLY as short stubs for now, the bottom layer will handle most of it (next block)
2. `+3V3` and `+5V` — short and fat (0.5mm)
3. The 4 SPI lines to J2: **keep them short, keep them parallel, keep them the same rough length**
4. `LCD_DC`, `LCD_RST`, `LCD_BL`
5. The 3 button nets
6. `CHIME_TRIG` / `CHIME_TRIG_OUT`

**8.5** **The rules that will save your screen from being blank forever:**
- SPI traces **under 50 mm**. If they're longer, move J2 closer.
- The 4 SPI lines should run side by side like train tracks.
- **DO NOT cross traces over each other on the same layer.** If you're stuck, use a via to jump to the other layer.
- **Add a via:** while routing, press **V** — the trace jumps to the other layer through a hole. On this board use vias sparingly.

**8.6** If a trace looks wrong: hover it, **Delete**, re-route. No penalty, do it as many times as it takes.

> ✅ **Checkpoint:** the white "ratsnest" lines (the thin lines showing missing connections) are ALL GONE. If any remain, those nets aren't connected — route them.

---

## BLOCK 9 — Ground plane: the pro move (20 min)

This is the trick that separates "hobby board" from "real board" — and it's three clicks.

**9.1** On the right layer list, click **B.Cu** (bottom copper). It highlights.

**9.2** On the right toolbar, click **"Add a filled zone"** (the icon looks like a hatched / crosshatched rectangle).

**9.3** Click at one corner of your board outline, then click each of the other three corners, then double-click to close the rectangle. A properties box pops up.

**9.4** In that box, the **Net** dropdown — select **GND**. Click OK.

**9.5** Press **B** (B = fill zones). The whole bottom layer floods with copper.

**9.6** **Do NOT put this zone under the antenna end.** If your zone covers the whole board and the antenna overhangs anyway, you're fine. If the antenna is over the board, shrink the zone away from it (delete the zone, redraw it as a smaller rectangle or an L-shape that stops 15mm short of the antenna).

> ✅ **Checkpoint:** the bottom of the board is a solid sheet of copper (usually shown purple/blue-green), and every GND pad has a path to it.

---

## BLOCK 10 — DRC and Gerbers: ship it (30 min)

**10.1** Top menu **Inspect → Design Rules Checker** → **Run DRC**.

**10.2** Fix EVERYTHING it reports. Common ones:
- **"Clearance" violations** → move the traces apart
- **"Track too narrow"** → widen that track to 0.15+
- **"Unconnected items"** → you missed a route (go back to Block 8.6)
- **"Edge.Cuts" issues** → your rectangle isn't fully closed, redraw it

**10.3** Goal: **0 errors, 0 unconnected items.**

**10.4** Add your silkscreen labels (the white text on the board): press the **"Add text"** icon (a "T"-looking icon on the right toolbar), click near J2, type `DISPLAY`. Do the same near J1 (`T5AI-CORE`), J3 (`CHIME`), each button (`MODE`, `UP`, `DN`). On the **F.Silkscreen** layer. Future-you will love this at bring-up.

**10.5** **GENERATE GERBERS** (this is the file you send to the factory):
- Top menu **File → Fabrication Outputs → Gerbers (.gbr)**
- A plot window appears. Default settings are fine for JLCPCB. Click **Plot**.
- Then in the same window click **Generate Drill Files** → **Generate**.
- KiCad puts everything in a folder next to your project. **Zip that folder.** That zip is what you upload to JLCPCB.

**10.6** SCREENSHOT THE 3D VIEW: top menu **View → 3D Viewer** (or press **Alt+3**). Spin it around, screenshot it. This is your hero shot for the submission AND your eventual viral post.

---

## THE PIN-VERIFICATION CHECKLIST — do this before you order

Print it, tick each box:

- [ ] T5AI-Core pinout PDF is open in front of me
- [ ] I know which socket pin = module pin P3, P4, P5 (buttons + chime)
- [ ] I know which socket pin = P12, P13, P14, P15, P16, P17 (LCD + SPI)
- [ ] I know which socket pin = P24, P25 (backlight + MODE)
- [ ] I know which socket pins are +3.3V, +5V, and GND
- [ ] When I hold the real T5AI-Core over the placed J1 footprint, USB-C faces the direction I want
- [ ] ERC: 0 errors
- [ ] DRC: 0 errors, 0 unconnected
- [ ] Every copper trace is ≥15mm from where the antenna sits
- [ ] Silkscreen labels on every connector
- [ ] Gerber zip is saved and I opened the 3D view to double check

**Then: order from JLCPCB same day. 5 boards of an 85×40mm 2-layer board is like $2 + shipping. Transit + customs is the one thing that can actually hurt you — so order the HOUR the DRC passes.**

---

## When you get stuck (you will, everyone does)

Stop, screenshot the screen, paste it to me. Tell me which block and step number. I will unstick you.
Do NOT sit there for 40 minutes fighting one error — that's how noobs quit.
