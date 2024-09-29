# GTASceneSync Blender Addon

## Overview
**GTASceneSync** is a versatile Blender addon for exporting 3D models and scenes into formats compatible with *Grand Theft Auto* (GTA) games. It supports exporting objects in IPL (Item Placement List) and IDE (Object Definition) formats, essential for modding and scene management in GTA titles. The addon also provides tools for managing materials, object properties, and collisions. With the latest updates, additional functionalities have been added to streamline the modding process.

## Key Features
- **Export to IPL (GTA San Andreas)**: Seamlessly export selected mesh objects from Blender into the IPL format used by GTA San Andreas. Supports incremental model IDs and configurable rotations.
- **Export to IPL (GTA III)**: Effortlessly export objects to the IPL format used by GTA III, tailored to meet the specific requirements of the game's modding environment.
- **Export to IPL (GTA Vice City)**: Full support for exporting objects in the IPL format used by GTA Vice City. The export process follows Vice City’s unique format, with hardcoded scaling and rotational values based on the game’s standards.
- **Export to IDE**: Define object properties and settings for your scenes by exporting object definitions to an IDE file. Customize each object with flags, render distances, and texture names.
  
## New Features
- **Tool Menu for Batch Operations**: Access new tools under the GTASceneSync panel, located in the `Object Properties` tab or via the `GTASceneSync Tools` menu.
  - **Remove Materials**: Select models and use the option to remove all materials from the selected objects.
  - **Convert to Collisions**: Automatically convert selected models into collision objects.
  - **Rename Objects**: Rename all selected models based on their collision data or other properties.
  - **Reset Position**: Quickly reset the position of selected objects to the origin (0, 0, 0) for easier scene management.

## Installation
1. [Download](#) the latest version of the addon.
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
   - **Convert to Collisions**: Convert models into their respective collision objects.
   - **Rename Objects**: Batch rename models based on collision data.
   - **Reset Position**: Set the position of all selected models to the origin (0, 0, 0).
5. **Export**: Use the appropriate export option from the `File > Export` menu. The GTA Vice City IPL export is now available along with the existing export options.

## Future Updates
- **Continued Refinements**: Vice City support is functional, but ongoing improvements will be made based on user feedback and testing.
- **Bug Fixes and Optimizations**: Regular updates will address any issues and optimize performance across all supported formats.

## Contact and Support
For support, feedback, or inquiries, contact **MadGamerHD** on YouTube at [bradzandmaxplays](#).

Stay tuned for more updates as we continue to expand the capabilities of the GTASceneSync addon!
