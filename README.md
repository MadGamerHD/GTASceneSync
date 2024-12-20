# GTASceneSync 2.0.0 Blender Addon

Notice Regarding Updates for GTASceneSync 2.0.0 Blender Addon

I want to inform users that there may not be many updates for the GTASceneSync 2.0.0 Blender Addon in the near future. Due to ongoing considerations and potential changes to the development direction, there's a possibility that the addon may be remade from scratch. We appreciate your patience and understanding during this time, and we'll keep you updated on any major changes or progress.

Thank you for using GTASceneSync!

## Overview
**GTASceneSync** is a versatile Blender addon for exporting 3D models and scenes into formats compatible with *Grand Theft Auto* (GTA) games. It supports exporting objects in IPL (Item Placement List) and IDE (Object Definition) formats, essential for modding and scene management in GTA titles. The addon also provides tools for managing materials, object properties, and collisions. With the latest updates, additional functionalities have been added to streamline the modding process.

## Key Features

- **Export to IPL (GTA San Andreas)**: Seamlessly export selected mesh objects from Blender into the IPL format used by GTA San Andreas. Key features include:
  - Incremental model IDs to avoid ID conflicts.
  - Configurable quaternion-based rotations for precise object placement, allowing for accurate orientation.
  - Option to apply default rotations across all objects for consistent placement.
  - Automatic cleanup of object names by removing numeric suffixes to prevent naming issues.

- **Export to IPL (GTA III)**: Effortlessly export objects to the IPL format used by GTA III, tailored to meet the specific requirements of the game's modding environment. Key features include:
  - Compatibility with GTA III’s object placement system.
  - Support for game-specific scaling and rotation requirements.

- **Export to IPL (GTA Vice City)**: Full support for exporting objects in the IPL format used by GTA Vice City. The export process follows Vice City’s unique format, now utilizing quaternion-based rotations for accuracy. Key features include:
  - Accurate representation of objects in Vice City with precise orientation.
  - Seamless integration with Vice City’s object system.

- **Export to IDE **: Define object properties and settings for your scenes by exporting object definitions to an IDE file. Key features include:
  - Customizable object flags to control special behaviors.
  - Adjustable render distances for optimizing performance.
  - Support for defining texture names (TXDs) to ensure proper in-game rendering.
  
## New Features
- **Tool Menu for Batch Operations**: Access new tools under the GTASceneSync panel, located in the `Object Properties` tab or via the `GTASceneSync Tools` menu.
  - **Remove Materials**: Select models and use the option to remove all materials from the selected objects.
  - **Convert to Collisions**: Automatically convert selected models into collision objects Requires DragonFF.
  - **Rename Objects**: Rename all selected models.
  - **Reset Position**: Quickly reset the position of selected objects to the origin (0, 0, 0) for easier scene management.

## Installation
1. [Download](https://github.com/MadGamerHD/GTASceneSync/archive/refs/heads/main.zip) the latest version of the addon.
2. Open Blender and navigate to `Edit > Preferences`.
3. In the `Add-ons` tab, click on `Install`.
4. Select the downloaded `.zip` file and click `Install Add-on`.
5. Enable the addon by checking the box next to **GTASceneSync IPL-IDE** in the list.

## Usage
1. **Access the Addon**: New export options are available under `File > Export`, including the ability to export objects to GTA IPL and IDE formats.
2. **Select Objects**: Choose the objects in Blender that you want to export.
3. **GTASceneSync Panel**: In the `Object Properties` tab, configure each object:
   - **Render Distance**: Set the render distance (299 to 1200 units) with step increments of 1.
   - **Texture Name**: Enter the texture or TXD name for each object.
   - **IDE Flags**: Assign specific flags to each object from a predefined list.
4. **Tool Menu Operations**: Open the **GTASceneSync Tools** menu for batch operations:
   - **Remove Materials**: Strip materials from all selected models.
   - **Convert to Collisions**: Convert models into their respective collision objects Requires DragonFF.
   - **Rename Objects**: Batch rename models.
   - **Reset Position**: Set the position of all selected models to the origin (0, 0, 0).
5. **Export**: Use the appropriate export option from the `File > Export` menu. The GTA Vice City IPL export is now available along with the existing export options.
6. 
## Future Updates
- **Continued Refinements**: Support for GTA San Andreas, GTA III, and GTA Vice City is functional, but ongoing improvements will be made based on user feedback and testing for all three formats.
- **Bug Fixes and Optimizations**: Regular updates will address any issues and optimize performance across all supported formats to ensure a smooth modding experience.

## Contact and Support
For support, feedback, or inquiries, contact **MadGamerHD** on YouTube at [bradzandmaxplays](https://www.youtube.com/@bradzandmaxplays).

Stay tuned for more updates as we continue to expand the capabilities of the GTASceneSync addon!
