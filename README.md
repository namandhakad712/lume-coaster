### lume-coaster
<img width="1093" height="496" alt="Screenshot 2026-10-10 232703" src="https://github.com/user-attachments/assets/cfc317d4-7369-476a-be77-5d96323c1a20" />


This project is mostly different but similar to other projects, everyone is using the the hardware suggested and the utitlities in the starter guide of [Starbie](https://github.com/SharKingStudios/Starbie) project.
But lmao people forgot that that 's [guide link](https://github.com/SharKingStudios/Starbie/blob/main/Week%201%20Guide.md), a beginner path to creativity not limit to it.

###### what is made
A carrier board (sandwitch)🥪 for the Tuya **T5AI-Core** ([Link](https://tuyaopen.ai/docs/hardware/tuya-t5/t5-ai-core/overview-t5-ai-core)) module — the kind of board, might be thinking what it is , it is a better much development board than ESP32 one's.
you design once so the module stops being a tangle of Dupont wires and starts
being an actual thing on your desk. It's a coaster-sized slab that the module
plugs into.

## See the layering system:

```
________________________________________
          tft-screen[__] | buttons (o) 
________________________________________
          Our Lume sandwitch board
__|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_
         The T5 AI Core board
________________________________________


```

Some text here , if my visual was little out of understandabe scope 🥲

It breaks the module out onto a single 85 × 40 mm PCB:

- a 44-pin socket for the module,
<img width="2160" height="3240" alt="image" src="https://github.com/user-attachments/assets/cb86fe48-e51c-4e6c-a30d-06cf99e38dbd" />

OR 

```
+-----------------------------------+
|  [::] [::] [::] [::] [::] [::]    |  <-- Pin Rows 1 to 22
|                                   |
|       ( MAIN TARGET MODULE )      |
|                                   |
|  [::] [::] [::] [::] [::] [::]    |  <-- Pin Rows 23 to 44
+-----------------------------------+
          |||||||||||||||
```
- a 9-pin header for a 2.8" **ILI9341** SPI colour LCD ,
<img width="1250" height="1250" alt="image" src="https://github.com/user-attachments/assets/a3be17cc-80e0-4c63-97f8-69e5609d9a87" />

- **Three tactile buttons** (mode / up / down),
```
     +------------+------------+
     |            |            |
     v            v            v
  +-----+      +-----+      +-----+
  |     |      |     |      |     |
  |MODE |      | UP  |      |DOWN |
  |     |      |     |      |     |
  +-----+      +-----+      +-----+
  (Tactile)    (Tactile)    (Tactile)
```
- a 3-pin header for an active chime / buzzer,
- an onboard **single-cell LiPo battery supply** with a USB-C charge path,
<img width="1000" height="1000" alt="image" src="https://github.com/user-attachments/assets/00945492-caed-4a95-ad8b-7069cf2cf855" />

- a P-MOS high-side switch for the display backlight.

It's a board, on its own, that does a job. Power it from USB-C or a LiPo,
plug in a display, and it shows whatever the module is running.

## Why this board

The T5AI-Core is a module, not a dev-kit. To use it for anything you either
hand-wire a breakout every single time, or you design one carrier board once
and never think about it again. This is the second one.

Everything on it is chosen to be unremarkable and reliable:

- **No duplicate regulators.** The module already regulates 5 V and 3.3 V on
  board. The carrier's battery supply feeds the module's own charge path —
  no second regulation stage, no ground loop.
- **Backlight is a switch, not a resistor.** P-MOS high-side, gate pulled
  high so the backlight is *off* by default during boot — no flash of white
  screen while the module is still pulling itself together.
- **Buttons are pulled high.** GPIO idles high, press is low. Three 10 kΩ
  pull-ups plus 100 nF debounce caps; no matrix, no expander, three pins is
  cheaper than an IC.
- **Chime is gated, not driven.** A 3-pin header with 5 V, ground, and a
  trigger line held low by a pull-down so no boot glitch ever rings it.

## Repo layout

```
carrier-board/      netlist, pin map, schematic notes, layout constraints
reference/          module pinout screenshots used while pinning out J1
tools/              KiCad tooling — the MCP server and the probe scripts
kicad-noob-guide.md the build procedure, block by block
BOM.md              parts list
JOURNAL.md          work log
```

`tools/kicad-mcp` is a vendored copy of
[mixelpixx/KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server)
(MIT). Not this project's code — it drives KiCad from this repo's tooling.

## Hardware one-liner

LiPo or USB-C → module's own charge path and regulators → +3V3 rail →
ILI9341 over SPI0, three buttons, one chime header, one P-MOS backlight.

Full net list, per-pin reasoning, and why each pin was picked or avoided:
[`carrier-board/netlist-pinmap.md`](carrier-board/netlist-pinmap.md).

## Status

**In progress — schematic capture.** Netlist and pinmap are locked, the KiCad
10 toolchain is set up and verified end to end (`pcbnew` import, board
create, footprint load, save/round-trip, and the MCP server booting clean
against KiCad 10.0.7). Schematic capture is next; see
[`JOURNAL.md`](JOURNAL.md).
