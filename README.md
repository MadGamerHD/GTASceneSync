# GTASceneSync 2.0.0

**Thank you for using GTASceneSync!**

## Summary
- **GTA San Andreas (SA)**: Full IPL and IDE support.  
- **GTA III**: Experimental.  
- **GTA Vice City**: Experimental.

## Overview
**GTASceneSync** is a robust Blender addon that streamlines the process of exporting 3D models and scenes into formats compatible with *Grand Theft Auto* (GTA) games, including GTA San Andreas, GTA III, and GTA Vice City. With powerful tools for managing object properties, materials, collisions, and object placements, it is an essential utility for GTA modders and scene managers. It supports exporting both IPL (Item Placement List) and IDE (Object Definition) files.

## Key Features

### **Export to IPL**
- **GTA San Andreas**:  
  - Export mesh objects with auto-incremented model IDs to avoid conflicts.  
  - Quaternion-based rotations for precise object orientation.  
  - Default rotations and automatic cleanup of object names (removes numeric suffixes).  
  - Support for both regular and binary IPL exports. Use [Fastman92 Processor](https://gtaforums.com/topic/857375-fastman92-processor/) to process the binary IPL file.

- **GTA III**:  
  - Experimental.

- **GTA Vice City**:  
  - Experimental.

### **Export to IDE**
- Define object properties and settings for your scenes:  
  - Customizable object flags for defining special behaviors.  
  - Adjustable render distances (0–1200 units) for optimized performance.  
  - TXD name support for accurate in-game texture rendering.

### **Export to 2DFX**
- Export a 2DFX file by selecting a mesh or cube, positioning it, and choosing a particle in the panel.  
- Open the exported 2DFX file in a text editor and save it as `.txt`.  
- Use [2DFX Tool](https://github.com/MadGamerHD/2DFX-Tool) for conversion and [rw-analyze](https://github.com/andrenanninga/mashed/tree/master/tools/rw-analyze) to replace or add 2DFX data in the DFF file.

### **Tool Menu for Batch Operations**
Access tools via the **GTASceneSync Panel** in the `Object Properties` tab or the **GTASceneSync Tools** menu:  
- **Remove Materials**: Strip all materials from selected models.  
- **Convert to Collisions**: Convert models into collision objects (requires DragonFF).  
- **Rename Objects**: Batch rename selected models.  
- **Reset Position**: Quickly reset object positions to (0, 0, 0).

## Installation
1. [Download the latest version](https://github.com/MadGamerHD/GTASceneSync/archive/refs/heads/main.zip) of the addon.  
2. Install [DragonFF](https://github.com/Parik27/DragonFF), making sure to use the latest version or my edit below.  
3. Open Blender, go to `Edit > Preferences`.  
4. Navigate to the `Add-ons` tab, click `Install`, and select the downloaded `.zip` file.  
5. Enable the addon by checking **GTASceneSync IPL-IDE** in the list.

## Usage
1. **Access the Addon**: Export options are available under `File > Export`.  
2. **Configure Objects**: In the **GTASceneSync Panel**:  
   - Set render distances (0–1200 units).  
   - Define TXD names.  
   - Assign IDE flags from a predefined list.  
3. **Batch Operations**: Use the **GTASceneSync Tools** menu for actions like removing materials, renaming objects, and resetting positions.  
4. **Export**: Choose the appropriate format under `File > Export` (e.g., GTA Vice City IPL, GTA San Andreas IPL).

## What's New in 2.0.0
- Added support for GTA Vice City IPL export with quaternion-based rotations.  
- New batch operations: Remove materials, convert to collisions, rename objects, and reset positions.  
- Fixed a crash issue in IPL export for GTA San Andreas.  
- Support for both regular and binary IPL exports. Use Fastman92 Processor to process the binary IPL files.  
- Added the ability to export to a 2DFX file. Select a cube or mesh, position it, and choose a particle to export.

## Screenshots
![Screenshot](https://github.com/user-attachments/assets/96cf2f99-d6db-4573-9a14-0c6eaaebaa42)

## Future Updates
- Ongoing bug fixes and performance optimizations based on user feedback.  
- Enhancements for all supported GTA formats.

## Contact and Support
For feedback, inquiries, or support, reach out to **MadGamerHD** on YouTube at [bradzandmaxplays](https://www.youtube.com/@bradzandmaxplays).  

Stay tuned for more updates as we continue to improve GTASceneSync!

Also, if you want to mass export DFF/COL files, check out my edit of DragonFF:  
[DragonFF Edit](https://github.com/MadGamerHD/DragonFF-Edit)
