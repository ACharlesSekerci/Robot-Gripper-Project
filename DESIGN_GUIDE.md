# 3D Gripper Design Guide

> Step-by-step guide for modifying and preparing the RobotGeek 9G Servo Gripper for 3D printing.

---

## 1. Selected Design

| Detail | Value |
|---|---|
| Name | **RobotGeek 9G Servo Gripper** |
| Source | [Thingiverse thing:2083312](https://www.thingiverse.com/thing:2083312) |
| Servo | 9g Micro Servo (SG90 / Fitec) |
| Original format | STL + DXF + STEP |
| License | Creative Commons — Attribution |

---

## 2. Parts List (33 parts total)

*Quantities verified from STEP assembly file (Gripper-Assembly.stp)*

| # | File | Description | Qty |
|---|---|---|---|
| 1 | `BottomPlate.stl` | Base frame plate | 1 |
| 2 | `TopPlate.stl` | Top frame plate | 1 |
| 3 | `BackPlate.stl` | Rear structural support | 1 |
| 4 | `BackPlateSpacer.stl` | Rear spacer | 1 |
| 5 | `Gear.stl` | Central gear — servo-driven, hidden between plates | 1 |
| 6 | `LeftFinger.stl` | Left gripper arm (has integrated gear teeth) | **2** |
| 7 | `RightFinger.stl` | Right gripper arm (has integrated gear teeth) | **2** |
| 8 | `FingerTip.stl` | Grip contact tip (attach foam/rubber) | **2** |
| 9 | `FingerTip-Plate.stl` | Tip mounting plate | **4** |
| 10 | `9GSpacer.stl` | Servo mount spacer | 1 |
| 11 | `9GSpacer-3mm.stl` | 3mm variant servo spacer | 1 |
| 12 | `3mmSpacer.stl` | General spacer (between plates) | **8** |
| 13 | `15mmStandoff.stl` | Standoff (plate separation) | **8** |
| — | `Fitec-9g.stl` | Servo reference model — **do NOT print** | — |
| — | `GripperASM.stl` | Assembly reference — **do NOT print** | — |

---

## 3. Modification Requirements

### 3.1 Hole Size — Change to 2.8 mm

All screw holes must be **2.8 mm diameter**.

**What to modify:**
- [ ] `BottomPlate.stl` — mounting holes
- [ ] `TopPlate.stl` — mounting holes
- [ ] `BackPlate.stl` — mounting holes
- [ ] `BackPlateSpacer.stl` — pass-through holes
- [ ] `LeftFinger.stl` — pivot hole
- [ ] `RightFinger.stl` — pivot hole
- [ ] `FingerTip-Plate.stl` — attachment holes
- [ ] `Gear.stl` — center and mounting holes (check if already correct)

**How to modify (Tinkercad):**
1. Import the STL into Tinkercad
2. Create a cylinder set as a **Hole** with diameter **2.8 mm**
3. Align the hole cylinder with the existing hole position
4. Group to cut the new hole
5. Repeat for every screw hole in the part
6. Export as STL

**How to modify (Fusion 360):**
1. Import STL → Convert to BRep (if small enough)
2. Select the hole face → Edit → Change diameter to **2.8 mm**
3. Export as STL

### 3.2 Screw Length Compatibility — 18–24 mm

The assembled gripper must work with screws **18 mm to 24 mm** long.

**What to check:**
- [ ] Measure the total stack-up thickness (plates + spacers) at each screw location
- [ ] Ensure the stack-up is **≤ 24 mm** (max screw length)
- [ ] Ensure the stack-up is **≥ 18 mm** or use spacers/washers to fill the gap
- [ ] If the stack is too thin, increase spacer height in the 3D model
- [ ] If the stack is too thick, reduce spacer height or use the 3mm variants

**Stack-up example:**
```
TopPlate (thickness) + Spacer + BottomPlate (thickness) = total
→ Must be between 18 mm and 24 mm for the screw to fit
```

### 3.3 Servo Attachment Screws — No Changes

The two small screws that attach the servo motor to the mounting plate use the servo's **original mounting holes**. These are standard and **do not need modification**.

---

## 4. Modification Workflow

```
Step 1: Download STL files              ✅ Done
     ↓
Step 2: Open each part in Tinkercad
     ↓
Step 3: Measure existing hole sizes
     ↓
Step 4: Modify holes → 2.8 mm
     ↓
Step 5: Check screw stack-up (18–24 mm range)
     ↓
Step 6: Adjust spacer heights if needed
     ↓
Step 7: Export modified STL files
     ↓
Step 8: Rename files (S<section>G<group>_PartName.stl)
     ↓
Step 9: Test print a small part first (e.g. spacer)
     ↓
Step 10: Print all parts
     ↓
Step 11: Assemble and test fit with servo + screws
```

---

## 5. File Naming Convention

When exporting final STL files, use this format:

```
S<section>G<group>_<PartName>.stl
```

**Example (Section 1, Group 1):**
- `S1G1_BottomPlate.stl`
- `S1G1_TopPlate.stl`
- `S1G1_BackPlate.stl`
- `S1G1_Gear.stl`
- `S1G1_LeftFinger.stl`
- `S1G1_RightFinger.stl`
- ... etc.

---

## 6. Print Settings (Recommended)

| Setting | Value |
|---|---|
| Material | PLA or PETG |
| Layer height | 0.2 mm |
| Infill | 20–30% |
| Supports | Yes (for overhangs on fingers/gear) |
| Bed adhesion | Brim recommended for small parts |
| Nozzle | 0.4 mm standard |

---

## 7. Assembly Order

1. Mount the **9g servo** into the `BottomPlate` using the servo's own screws
2. Place the `9GSpacer` around the servo
3. Attach the `Gear` to the servo horn
4. Insert the `LeftFinger` and `RightFinger` — they mesh with the gear
5. Attach `FingerTip-Plate` + `FingerTip` to each finger end
6. Add `BackPlate` + `BackPlateSpacer` to the rear
7. Close with `TopPlate`
8. Secure with **M3 screws (18–24 mm)** through all plate layers
9. Use `3mmSpacer` / `15mmStandoff` as needed for correct stack height

---

## 8. Design Checklist

- [ ] All STL files downloaded
- [ ] Each part opened in Tinkercad / editor
- [ ] All screw holes modified to **2.8 mm**
- [ ] Stack-up measured and fits **18–24 mm** screws
- [ ] Servo mount holes left unchanged
- [ ] Modified STL files exported
- [ ] Files renamed with section/group convention
- [ ] Test print completed (spacer or small part)
- [ ] Full print completed
- [ ] Assembly tested with servo + screws
- [ ] Gripper opens and closes smoothly

---

## 9. Progress Log

| Date | Update | Status |
|---|---|---|
| | STL files downloaded from Thingiverse | ✅ Done |
| | Hole modifications started | ⬜ Pending |
| | Screw stack-up verified | ⬜ Pending |
| | Modified files exported | ⬜ Pending |
| | Test print | ⬜ Pending |
| | Full print | ⬜ Pending |
| | Assembly complete | ⬜ Pending |
| | Servo test (open/close) | ⬜ Pending |

---

*This guide covers the 3D design portion only. See [ROADMAP.md](ROADMAP.md) for the full project (Python, Arduino, etc.).*
