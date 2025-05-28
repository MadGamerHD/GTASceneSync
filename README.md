**GTASceneSync (SA Only) Blender Add‑on**
*Export GTA San Andreas IDE and IPL files directly from Blender, with both batch and per-object controls, plus handy utility tools.*

---

#Preview

![Screenshot 2025-05-28 102716](https://github.com/user-attachments/assets/2a7064ec-d3da-43d9-a74a-1103325df804)

Note.. Install DragonFF for convert to col to work
## Features

* **IDE Export**
  Generate a San Andreas `.ide` file listing unique models from selected meshes, with configurable start ID and per-object flags.

* **IPL Export**
  Export placement `.ipl` files in either ASCII or binary format.

  * Optionally apply a default rotation to all instances.
  * Auto‑assign model IDs based on cleaned object names.

* **Batch Utilities**

  * **Rename**: Give selected objects a consistent base name with incremental suffixes.
  * **Reset Position**: Move objects back to the world origin (0,0,0).
  * **Remove Materials**: Strip all materials from selected meshes.
  * **Convert to Collision**: Tag selected meshes as collision objects (sets a custom `dff.type` property).

* **Batch TXD Assignment**
  Quickly set the texture dictionary (TXD) name for all selected meshes at once.

* **Per‑Object IDE Flags**
  In the UI sidebar, adjust for each selected mesh:

  * Texture name (TXD)
  * Render distance
  * Custom IDE flag

* **Intuitive UI Panel**
  All tools are grouped under *View3D → UI → GTASceneSync* for fast access.

---

## Requirements

* Blender **4.0** or newer
* Python scripting enabled (default in Blender)

---

## Installation

1. **Download** the `GTASceneSync` add‑on directory (containing this script).
2. In Blender, go to **Edit → Preferences → Add-ons → Install…**
3. Select the `.py` script or containing folder and click **Install Add-on**.
4. Enable **GTASceneSync (SA Only)** in the list.

---

## Usage

Once enabled, open the **GTASceneSync** panel in the 3D Viewport sidebar (press **N**):

### 1. Utilities

* **Batch Rename**

  1. Enter your desired base name in the **Rename Base** field.
  2. Select objects → click **Rename** → objects become `BaseName_1`, `BaseName_2`, …

* **Reset Position**

  * With objects selected, click **Reset Pos** to move them all to (0,0,0).

* **Remove All Materials**

  * Click **Remove Mats** to clear materials on selected meshes.

* **Convert to Collision Object**

  * Click **To Collision** to tag meshes as collision models in downstream exporters.

---

### 2. Batch TXD Assignment

1. Type your TXD name into **TXD Name**.
2. Select target meshes → click **Set TXD** → all get the same texture dictionary reference.

---

### 3. Per‑Object Settings

For each selected mesh, you’ll see a collapsible box showing:

* **Texture Name (TXD)**
* **IDE Flag** (e.g. default, special behaviors)
* **Draw Distance** (render cutoff)

Adjust these before exporting to fine‑tune individual entries.

---

### 4. Exporting

#### Export IDE

1. Select one or more mesh objects.
2. Click **Export IDE**.
3. In the file dialog, choose an output path (extension auto‑appended if needed).
4. Set the **Starting Model ID** in the popup if you need a custom base.
5. Confirm → generates a `.ide` file containing:

   ```text
   objs
   <ModelID>, <CleanName>, <TXD>, <RenderDist>, <Flag>
   … (one line per unique model)
   end
   ```

#### Export IPL

1. Select meshes to place in the world.
2. Click **Export IPL**.
3. Choose output path; extension is ensured to be `.ipl`.
4. In the operator panel, adjust:

   * **Starting Model ID**
   * **Apply Default Rotation** (and specify Euler angles)
   * **Export Type**: ASCII (`normal`) or binary (`bnry`)
5. Confirm → generates the `.ipl` file with instance definitions:

   * ASCII format begins with `inst` block, each line:

     ```
     ModelID, Name, 0, X, Y, Z, Rx, Ry, Rz, Rw, LOD
     ```
   * Binary writes packed floats & integers for faster loading in mod tools.

---

## Property Overview

* **`scene.batch_txd_name`**: default `"generic"`
* **`scene.batch_rename_base_name`**: default `"TypeName"`
* **`Object.ide_flags`** property group:

  * `texture_name` (String)
  * `ide_flag` (Enum)
  * `render_distance` (Int)

---

## Tips & Best Practices
* **Clean Naming**: The add‑on strips trailing numeric suffixes (e.g. `Car.001` → `Car`), so you can model copies without worrying about duplicate entries.
* **Batch First**: Assign TXDs and flags in batch, then tweak per-object settings to save time.
* **Rotation Offset**: Use **Apply Default Rotation** on IPL export if your models were authored in a different up‑axis or need a uniform orientation tweak.
