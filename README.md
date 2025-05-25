# GTASceneSync 2.0.0

**Thank you for using GTASceneSync!**

---

## Summary

* **GTA San Andreas**: Stable and fully supported for IPL and IDE export.
* **GTA III**: Experimental support.
* **GTA Vice City**: Experimental support.

**Note:** LOD system is *not* included—use MEd or in-game tools to configure LODs.

> **Max Models per IPL:** Allows loading up to **11,552 DFF models** in a single IPL for massive custom maps and complex scenes.

---

## Common Questions

**Q:** Can I load or view the GTA SA map in Blender with this addon?

**A:** No. GTASceneSync is designed for creating new scenes and exporting them to GTA games; it does *not* support editing or viewing the original map.

**Q:** How do I use the exported IDE/IPL files?

**A:** Place them in your game directory (e.g., via ModLoader or custom folder structure). Use MEd, Fastman92 Processor, or other tools to preview in-game.

**Q:** My File exported but nothing shows up. What should I check?

**A:** Verify draw distances, IDE flags, TXD names, and object placement. Ensure textures and collision files are correctly referenced.

---

## Overview

**GTASceneSync** is a robust Blender addon that streamlines exporting 3D content to **Grand Theft Auto** formats. Ideal for modders and scene builders, it supports:

* **IPL** (Item Placement List)
* **IDE** (Object Definition)
* **2DFX** (Particle effects)

Compatible with **GTA San Andreas**, **GTA III**, and **GTA Vice City** (experimental for the last two).

---

## Key Features

### Export to IPL (GTA San Andreas)

* Auto-incremented model IDs to avoid conflicts.
* Quaternion-based rotations for precise orientation.
* Binary and regular IPL export (use Fastman92 Processor for binary).
* Automatic cleanup of object names (removes numeric suffixes).

### Export to IDE

* Customizable object flags for special behaviors.
* Adjustable render distances (0–1200 units) on a per-object basis.
* TXD name support for accurate texture mapping.

### Export to 2DFX

1. Select a mesh or cube and position it in Blender.
2. Choose a particle preset in the addon panel.
3. Export to `.2dfx` file and convert to `.txt` with 2DFX Tool or rw-analyze.

### Batch Operations (GTASceneSync Panel & Tools Menu)

* **Remove Materials**: Strip all materials from selected models.
* **Convert to Collisions**: Turn meshes into collision geometry (requires DragonFF).
* **Rename Objects**: Batch rename selected objects.
* **Reset Position**: Reset location to (0, 0, 0).
* **Set Render Distance**: Define per-model draw distances for optimized streaming.

---

## Installation

1. Download the latest ZIP from the [GitHub repo](https://github.com/MadGamerHD/GTAScenesync/archive/refs/heads/main.zip).
2. Install or update [DragonFF](https://github.com/Parik27/DragonFF) (use the latest version or my [DragonFF-Edit](https://github.com/MadGamerHD/DragonFF-Edit)).
3. In Blender: `Edit > Preferences > Add-ons > Install` → select the downloaded ZIP.
4. Enable **GTASceneSync IPL-IDE** in the add-on list.

---

## Usage

1. **Access Exporters**: `File > Export` → choose GTA format.
2. **Configure Objects** via the **GTASceneSync Panel**:

   * Set per-object render distances.
   * Assign TXD names and IDE flags.
3. **Batch Tools** in the **GTASceneSync Tools** menu:

   * Remove materials, rename, convert collisions, etc.
4. **Export** to IPL, IDE, or 2DFX as needed.

---

## What's New in 2.0.0

* **Max IPL Models:** Support for up to 11,552 DFFs in a single IPL. SA
* Added GTA Vice City IPL export (quaternion-based rotation).
* Batch tools: remove materials, convert to collisions, rename objects, reset positions.
* Fixed crash in GTA SA IPL export.
* 2DFX export workflow integrated.

---

## Screenshots

![GTASceneSync Panel](https://github.com/MadGamerHD/GTAScenesync/assets/96cf2f99-d6db-4573-9a14-0c6eaaebaa42)

---

## Future Plans

* Enhanced in-game LOD integration.
* Performance optimizations based on feedback.
* Better support for GTA III & Vice City.

---

## Support & Contact

For issues or feature requests, open a GitHub issue or reach out on YouTube: **MadGamerHD** ([bradzandmaxplays](https://www.youtube.com/@bradzandmaxplays)).
