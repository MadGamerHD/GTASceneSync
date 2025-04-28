bl_info = {
    "name": "GTASceneSync IPL-IDE",
    "blender": (4, 0, 0),
    "category": "Object",
    "version": (2, 0, 0),
    "author": "MadGamer HD",
    "support": "COMMUNITY",
}

import bpy
from .Export.SyncIDE_Export import ExportAsIDE
from .Export.SyncIPL_Export_SA import ExportAsIPL
from .Export.SyncIPL_Export_III import ExportAsIPLIII
from .Export.SyncIPL_Export_VC import ExportAsIPLVC
from .Menu.ide_flags_panel import GTASceneSyncPanel, IDEFlagsProperties
from .Menu.Tools import (
    OBJECT_OT_batch_rename,
    OBJECT_OT_reset_position,
    OBJECT_OT_remove_materials,
    OBJECT_OT_convert_to_collision,
    VIEW3D_PT_batch_rename_panel,
)
from .Menu.ToolsPanelTwo import (
    ToolsPanelTwo,
    OBJECT_OT_set_texture_name,
)
from .Export.Sync2DFX_Export import register as register_2dfx, unregister as unregister_2dfx

class GTASceneSyncMenu(bpy.types.Menu):
    """Create a custom menu in the Blender UI"""

    bl_idname = "OBJECT_MT_gtascenesync"
    bl_label = "GTASceneSync"

    def draw(self, context):
        layout = self.layout
        layout.operator(ExportAsIPL.bl_idname, text="Export Selected as IPL (SA)")
        layout.operator(
            ExportAsIPLIII.bl_idname, text="Export Selected as IPL (GTA III)"
        )
        layout.operator(ExportAsIPLVC.bl_idname, text="Export Selected as IPL (VC)")
        layout.operator(ExportAsIDE.bl_idname, text="Export Selected as IDE")

def menu_func(self, context):
    self.layout.menu(GTASceneSyncMenu.bl_idname)

def register():
    bpy.utils.register_class(GTASceneSyncMenu)
    bpy.utils.register_class(ExportAsIPL)
    bpy.utils.register_class(ExportAsIPLIII)
    bpy.utils.register_class(ExportAsIPLVC)
    bpy.utils.register_class(ExportAsIDE)
    bpy.utils.register_class(IDEFlagsProperties)
    bpy.utils.register_class(GTASceneSyncPanel)
    bpy.utils.register_class(OBJECT_OT_batch_rename)
    bpy.utils.register_class(OBJECT_OT_reset_position)
    bpy.utils.register_class(OBJECT_OT_remove_materials)
    bpy.utils.register_class(OBJECT_OT_convert_to_collision)
    bpy.utils.register_class(VIEW3D_PT_batch_rename_panel)
    bpy.utils.register_class(ToolsPanelTwo)
    bpy.utils.register_class(OBJECT_OT_set_texture_name)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)
    bpy.types.Object.ide_flags = bpy.props.PointerProperty(type=IDEFlagsProperties)

    # Registering the new 2DFX export functionality
    register_2dfx()

def unregister():
    bpy.utils.unregister_class(GTASceneSyncMenu)
    bpy.utils.unregister_class(ExportAsIPL)
    bpy.utils.unregister_class(ExportAsIPLIII)
    bpy.utils.unregister_class(ExportAsIPLVC)
    bpy.utils.unregister_class(ExportAsIDE)
    bpy.utils.unregister_class(IDEFlagsProperties)
    bpy.utils.unregister_class(GTASceneSyncPanel)
    bpy.utils.unregister_class(OBJECT_OT_batch_rename)
    bpy.utils.unregister_class(OBJECT_OT_reset_position)
    bpy.utils.unregister_class(OBJECT_OT_remove_materials)
    bpy.utils.unregister_class(OBJECT_OT_convert_to_collision)
    bpy.utils.unregister_class(VIEW3D_PT_batch_rename_panel)
    bpy.utils.unregister_class(ToolsPanelTwo)
    bpy.utils.unregister_class(OBJECT_OT_set_texture_name)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)
    del bpy.types.Object.ide_flags

    # Unregistering the 2DFX export functionality
    unregister_2dfx()

if __name__ == "__main__":
    register()