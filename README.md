# GTASceneSync 2.0.0

**Thank you for using GTASceneSync!**

Summary
GTA SA Full IPL IDE Support.
GTA III Experimental.
GTA VC Experimental.

## Overview  
**GTASceneSync** is a powerful Blender addon designed to simplify the process of exporting 3D models and scenes into formats compatible with *Grand Theft Auto* (GTA) games, including GTA San Andreas, GTA III, and GTA Vice City. It supports exporting IPL (Item Placement List) and IDE (Object Definition) files while providing tools for managing materials, object properties, and collisions—making it an indispensable utility for GTA modding and scene management.

## Key Features  

### **Export to IPL**  
- **GTA San Andreas**:  
  - Export selected mesh objects with incremental model IDs to prevent conflicts.  
  - Precise quaternion-based rotations for accurate object orientation.  
  - Options for default rotations and automatic cleanup of object names (removes numeric suffixes).  
  - Support for both regular and binary IPL exports. Use [Fastman92 Processor](https://gtaforums.com/topic/857375-fastman92-processor/) for processing the binary IPL file.

- **GTA III**:  
  - Export objects with custom-tailored properties for GTA III’s object placement system.  
  - Support for scaling and rotation adjustments specific to GTA III.  

- **GTA Vice City**:  
  - Export objects with quaternion-based rotations for accurate in-game representation.  
  - Seamlessly integrates with Vice City’s object system.  

### **Export to IDE**  
- Define object properties and settings for your scenes:  
  - Customizable object flags for defining special behaviors.  
  - Adjustable render distances (0–1200 units) for optimized performance.  
  - TXD name support for accurate in-game texture rendering.

### **Export to 2DFX**
- Export to a 2DFX file by selecting a cube or mesh, positioning it, and choosing a particle in the panel.  
- Export the 2DFX file, open it in a text editor, and save it as a `.txt` file.  
- Use [2DFX Tool](https://github.com/MadGamerHD/2DFX-Tool) to convert the file, and then use [rw-analyze](https://github.com/andrenanninga/mashed/tree/master/tools/rw-analyze) to replace or add the 2DFX data in the DFF file.

### **Tool Menu for Batch Operations**  
Access tools via the **GTASceneSync Panel** in the `Object Properties` tab or the **GTASceneSync Tools** menu:  
- **Remove Materials**: Strip all materials from selected models.  
- **Convert to Collisions**: Automatically convert models into collision objects (requires DragonFF).  
- **Rename Objects**: Batch rename selected models.  
- **Reset Position**: Quickly reset object positions to (0, 0, 0).  

## Installation  
1. [Download the latest version](https://github.com/MadGamerHD/GTASceneSync/archive/refs/heads/main.zip) of the addon.
2. Install [DragonFF](https://github.com/Parik27/DragonFF). Make sure to install the latest version or my edit below.  
3. Open Blender, go to `Edit > Preferences`.  
4. Navigate to the `Add-ons` tab, click `Install`, and select the downloaded `.zip` file.  
5. Enable the addon by checking **GTASceneSync IPL-IDE** in the list.

## Usage  
1. **Access the Addon**: Find export options under `File > Export`.  
2. **Configure Objects**: In the **GTASceneSync Panel**:  
   - Set render distances (0–1200 units).  
   - Define TXD names.  
   - Assign IDE flags from a predefined list.  
3. **Batch Operations**: Use the **GTASceneSync Tools** menu to perform actions like removing materials or resetting object positions.  
4. **Export**: Choose the appropriate format under `File > Export` (e.g., GTA Vice City IPL, GTA San Andreas IPL).

## New in 2.0.0  
- Added support for GTA Vice City IPL export with quaternion-based rotations.  
- New batch operations: Remove materials, convert to collisions, rename objects, and reset positions.  
- Fixed a crash issue in the IPL export for GTA San Andreas.  
- Support for exporting both regular and binary IPL formats. Use Fastman92 Processor to process the binary IPL file.
- Export to a 2DFX file by selecting a cube or mesh, positioning it, and choosing a particle in the panel.  

## Previews
![Screenshot 2025-04-28 162531](https://github.com/user-attachments/assets/96cf2f99-d6db-4573-9a14-0c6eaaebaa42)


## Future Updates  
- Ongoing bug fixes and optimizations based on user feedback.  
- Performance enhancements for all supported GTA formats.

## Contact and Support  
For feedback, inquiries, or support, reach out to **MadGamerHD** on YouTube at [bradzandmaxplays](https://www.youtube.com/@bradzandmaxplays).  

Stay tuned for more updates as we continue to improve GTASceneSync!

Also, if you want to mass export DFF/COL files, check out my edit of DragonFF:  
[DragonFF Edit](https://github.com/MadGamerHD/DragonFF-Edit)
