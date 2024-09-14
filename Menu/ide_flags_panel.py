import bpy

class IDEFlagsProperties(bpy.types.PropertyGroup):
    ide_flag: bpy.props.EnumProperty(
        name="IDE Flag",
        description="Select the IDE flag for the object",
        items=[
            ("0", "Default", ""),
            ("1", "Render_Wet_Effects", ""),
            ("2", "TOBJ_Night_Flag", ""),
            ("16", "TOBJ_Day_Flag", ""),
            ("4", "Alpha_Transparency_1", ""),
            ("8", "Alpha_Transparency_2", ""),
            ("32", "Interior_Object", ""),
            ("64", "Disable_Shadow_Culling", ""),
            ("128", "Exclude_Surface_From_Culling", ""),
            ("256", "Disable_Draw_Distance", ""),
            ("512", "Breakable_Window", ""),
            ("1024", "Breakable_Window_With_Cracks", ""),
            ("2048", "Garage_door", ""),
            ("4096", "2-Clump-Object", ""),
            ("8192", "Small-Vegetation-Strong-wind-Effect", ""),
            ("16384", "Standard-Vegetation", ""),
            ("32768", "timecycle-PoleShadow-flag", ""),
            ("65536", "Explosive", ""),
            ("131072", "UNKNOWN-(Seems to be an SCM Flag)-(?)", ""),
            ("262144", "UNKNOWN-(1 Object in Jizzy`s Club)-(?)", ""),
            ("524288", "UNKNOWN-(?)", ""),
            ("1048576", "Graffiti", ""),
            ("2097152", "Disable-backface-culling", ""),
            ("4194304", "UNKNOWN-Unused-(Parts of a statue in Atrium) (?)", ""),
            ("1073741824", "Unknown", ""),
        ],
        default="0"
    )
    
    render_distance: bpy.props.IntProperty(
        name="Render Distance",
        description="Set the render distance for the object",
        default=299,
        min=0,
        max=1200,
        step=1
    )
    
    texture_name: bpy.props.StringProperty(
        name="Texture Name",
        description="Specify the texture or TXD name for the object",
        default="generic"
    )

class GTASceneSyncPanel(bpy.types.Panel):
    bl_label = "GTASceneSync"
    bl_idname = "OBJECT_PT_gtascenesync"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_category = 'Item'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj:
            if not hasattr(obj, 'ide_flags'):
                obj.ide_flags = bpy.context.scene.ide_flags
            
            layout.prop(obj.ide_flags, "ide_flag")
            layout.prop(obj.ide_flags, "render_distance")
            layout.prop(obj.ide_flags, "texture_name")

def register():
    bpy.utils.register_class(IDEFlagsProperties)
    bpy.utils.register_class(GTASceneSyncPanel)
    bpy.types.Object.ide_flags = bpy.props.PointerProperty(type=IDEFlagsProperties)

def unregister():
    bpy.utils.unregister_class(IDEFlagsProperties)
    bpy.utils.unregister_class(GTASceneSyncPanel)
    del bpy.types.Object.ide_flags

if __name__ == "__main__":
    register()
