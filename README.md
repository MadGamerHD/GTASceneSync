# GTASceneSync (SA Only)

> Export GTA San Andreas IDE & IPL files directly from Blender—batch settings, per‑object flags, draw distances, and texture dictionaries, all in one panel.

---

## ✨ Features

- **IDE Export**  
  - Generates a single `.ide` listing of unique model entries  
  - Customizable starting model ID  
  - Includes TXD name, render distance & flag for each object  

- **IPL Export**  
  - ASCII (`.ipl`) or binary (`.ipl`) export  
  - Optional global rotation offset (Euler angles)  
  - World‑space placement using Blender’s transforms → GTA quaternions

- **Batch TXD Assignment**  
  - Assign one TXD to multiple selected meshes in one click

- **Per‑Object Overrides**  
  - In‑viewport UI for each selected mesh:  
    - Texture Dictionary (TXD)  
    - IDE flag (wet, night, alpha‑1/2, day)  
    - Render distance (0–1200)

---

## Preview
![Screenshot 2025-05-27 191149](https://github.com/user-attachments/assets/ea20b4e6-6562-4e0b-9f98-8fbc6920900d)


## 🛠️ Installation

1. Copy the `GTASceneSync/` folder into Blender’s addon path:  
   - **Windows:** `%AppData%\Blender\4.0\scripts\addons\`  
   - **macOS/Linux:** `~/.config/blender/4.0/scripts/addons/`
2. In Blender: **Edit ▶ Preferences ▶ Add-ons**, search **GTASceneSync**, enable it, then **Save Preferences**.

---

## ⚙️ Usage

Open the **N‑panel** in the 3D Viewport and click the **GTASceneSync** tab.

1. **Batch TXD**  
   - Enter a texture dictionary name ➔ **Set TXD**  
2. **Per‑Object Settings**  
   - Adjust TXD, flag, and draw distance for each selected mesh  
3. **Export IDE**  
   - Click **Export IDE**, choose save path & starting ID, then **Export**  
4. **Export IPL**  
   - Click **Export IPL**, configure rotation/format, choose path, then **Export**

---

## 🧩 How It Works

- **Naming**: `clean_name()` strips `.001`‑style suffixes.  
- **Model IDs**: Deduplicates base names, assigns sequential IDs starting from user value.  
- **Quaternion Conversion**: Blender’s rotation → GTA format `(X, Y, Z, W)` with optional Euler offset.  
- **Binary IPL**: Packs 7 floats + 3 ints via `struct.pack('<7f3i', …)`.

---

## 🔧 Properties

- **Scene**
  - `batch_txd_name` (String): default TXD for batch assign
- **Object.ide_flags** (PropertyGroup)
  - `texture_name` (String)  
  - `ide_flag` (Enum: 0,1,2,4,8,16) + 
  - `render_distance` (Int, 0–1200)

---

## 🐞 Troubleshooting

- **“No mesh objects selected.”**  
  Ensure at least one mesh is selected before exporting.
- **Missing extension**  
  `.ide` or `.ipl` is auto‑appended if omitted.
- **Binary write errors**  
  Check file permissions, free disk space.

---

## ⚖️ License & Credits

- **License:** MIT  
- **Author:** MadGamerHD
- Special thanks to the GTA modding community. and WIKI

```text
MIT License
Copyright (c) 2025 MadGamerHD
