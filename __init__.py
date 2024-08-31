bl_info = {
    "name": "GTASceneSync IPL-IDE",
    "blender": (4, 0, 0),
    "category": "Object",
    "version": (1, 9, 0),
    "author": "MadGamer HD",
    "support": "COMMUNITY",
}

import bpy
from .Export.SyncIDE_Export import ExportAsIDE
from .Export.SyncIPL_Export_SA import ExportAsIPL
from .Export.SyncIPL_Export_III import ExportAsIPLIII
from .Export.SyncIPL_Export_VC import ExportAsIPLVC
from .Menu.ide_flags_panel import GTASceneSyncPanel, IDEFlagsProperties

class GTASceneSyncMenu(bpy.types.Menu):
    """Create a custom menu in the Blender UI"""
    bl_idname = "OBJECT_MT_gtascenesync"
    bl_label = "GTASceneSync"

    def draw(self, context):
        layout = self.layout
        layout.operator(ExportAsIPL.bl_idname, text="Export Selected as IPL (SA)")
        layout.operator(ExportAsIPLIII.bl_idname, text="Export Selected as IPL (GTA III)")
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
    bpy.types.TOPBAR_MT_file_export.append(menu_func)
    bpy.types.Object.ide_flags = bpy.props.PointerProperty(type=IDEFlagsProperties)

def unregister():
    bpy.utils.unregister_class(GTASceneSyncMenu)
    bpy.utils.unregister_class(ExportAsIPL)
    bpy.utils.unregister_class(ExportAsIPLIII)
    bpy.utils.unregister_class(ExportAsIPLVC)
    bpy.utils.unregister_class(ExportAsIDE)
    bpy.utils.unregister_class(IDEFlagsProperties)
    bpy.utils.unregister_class(GTASceneSyncPanel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)
    del bpy.types.Object.ide_flags

if __name__ == "__main__":
    register()
