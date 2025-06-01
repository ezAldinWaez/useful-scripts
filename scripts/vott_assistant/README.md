# VoTT Assistant

**Language:** `AutoHotkey`
**Author:** Ez Aldin Waez
**Last updated:** 2023-04-08

## Purpose

Automates repetitive mouse clicks and key presses in Microsoft’s **Visual Object Tagging Tool (VoTT)**, dramatically speeding up manual image-annotation workflows.

## Features

-   One-key shortcuts for **New Region**, **Delete Region**, **Finalize Tag**, and more.
-   Spacebar behaves as a left-click so your hand rarely leaves the keyboard.
-   Batch loops that can delete or confirm dozens of regions until **Esc** is pressed.
-   On-screen cursor coordinate read-out for quickly adjusting hard-coded positions.
-   Clean-exit hotkey and emergency loop break.

## Usage

```text
# Option 1 – run directly
VoTT_assistant.ahk

# Option 2 – compiled
VoTT_assistant.exe
```

### Key hotkeys

| Hotkey         | Action (1080 p default layout)     |
| -------------- | ---------------------------------- |
| `Space`        | Send left-click                    |
| `W`            | New region (`l`)                   |
| `E` / `Q`      | Confirm two regions                |
| `I` or `Alt+I` | Click **Finalize Tag** button      |
| `X`            | Delete current region              |
| `Win+Alt+X`    | Delete 50 regions in a loop        |
| `H`            | Toggle region visibility           |
| `Win+Alt+P`    | Confirm region → Next frame (loop) |
| `Esc`          | Stop any running loop              |
| `Win+Alt+\\`   | Show cursor coordinates            |
| `Win+Alt+Q`    | Exit script                        |

### Example

```text
; Typical flow
1. Launch VoTT and open your project.
2. Run VoTT_assistant.ahk.
3. Press W to start drawing regions and I to finalize.
```

## Exit codes

`VoTT_assistant` runs until terminated and does not return process exit codes. Use **Win+Alt+Q** to exit gracefully.

## Dependencies

-   **AutoHotkey v1.1+** (or compile the script to an `.exe` with **Ahk2Exe**)

Install AHK from:

```text
https://www.autohotkey.com/
```

## Changelog

| Date       | Notes           |
| ---------- | --------------- |
| 2023-04-08 | Initial version |

---

> **Tip**
> If your screen resolution differs from 1920 × 1080, update the `MouseMove` coordinates inside the script. Use **Win+Alt+\\** to read live coordinates.
