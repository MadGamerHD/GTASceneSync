# GTASceneSync 2.0.0

**Thank you for using GTASceneSync!**

## Overview  
**GTASceneSync** is a powerful Blender addon designed to streamline exporting 3D models and scenes into formats compatible with *Grand Theft Auto* (GTA) games, including GTA San Andreas, GTA III, and GTA Vice City. It supports exporting IPL (Item Placement List) and IDE (Object Definition) formats while providing tools to manage materials, object properties, and collisions—making it an essential utility for GTA modding and scene management.

## Key Features  

### **Export to IPL**  
- **GTA San Andreas**:  
  - Export selected mesh objects with incremental model IDs to prevent conflicts.  
  - Quaternion-based rotations for precise object orientation.  
  - Options for default rotations and automatic cleanup of object names (removes numeric suffixes).  

- **GTA III**:  
  - Export objects tailored to GTA III’s object placement system.  
  - Support for scaling and rotation requirements specific to GTA III.  

- **GTA Vice City**:  
  - Export objects with accurate quaternion-based rotations for precise in-game representation.  
  - Fully integrated with Vice City’s object system.  

### **Export to IDE**  
- Define object properties and settings for your scenes:  
  - Customizable object flags to define special behaviors.  
  - Adjustable render distances (0–1200 units) for optimized performance.  
  - TXD name support for accurate in-game texture rendering.  

### **Tool Menu for Batch Operations**  
Access tools via the **GTASceneSync Panel** in the `Object Properties` tab or the **GTASceneSync Tools** menu:  
- **Remove Materials**: Strip all materials from selected models.  
- **Convert to Collisions**: Automatically convert models into collision objects (requires DragonFF).  
- **Rename Objects**: Batch rename selected models.  
- **Reset Position**: Quickly reset object positions to (0, 0, 0).  

## Installation  
1. [Download](https://github.com/MadGamerHD/GTASceneSync/archive/refs/heads/main.zip) the latest version of the addon.  
2. Open Blender, go to `Edit > Preferences`.  
3. Navigate to the `Add-ons` tab, click `Install`, and select the downloaded `.zip` file.  
4. Enable the addon by checking **GTASceneSync IPL-IDE** in the list.  

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
- Fixed crash issue in the IPL file for GTA San Andreas.  

## Future Updates  
- Ongoing refinements and bug fixes based on user feedback.  
- Optimized performance for all supported GTA formats.  

## Contact and Support  
For feedback, inquiries, or support, reach out to **MadGamerHD** on YouTube at [bradzandmaxplays](https://www.youtube.com/@bradzandmaxplays).  

Stay tuned for updates as we continue enhancing GTASceneSync!  
