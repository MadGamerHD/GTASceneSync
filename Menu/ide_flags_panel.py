import bpy

# Predefined IDE flags for better readability and maintainability
IDE_FLAGS_ITEMS = [
    ("0", "(SA)Default", "No special flags"),
    ("1", "(SA)Render_Wet_Effects", "Object is rendered with wet effects"),
    ("2", "(SA)TOBJ_Night_Flag", "Object texture is used for night time"),
    ("16", "(SA)TOBJ_Day_Flag", "Object texture is used for day time"),
    ("4", "(SA)Alpha_Transparency_1", "Object has first type of transparency"),
    ("8", "(SA)Alpha_Transparency_2", "Object has second type of transparency"),
    ("32", "(SA)Interior_Object", "Object is an interior object"),
    ("64", "(SA)Disable_Shadow_Culling", "Object's shadow culling is disabled"),
    ("128", "(SA)Exclude_Surface_From_Culling", "Excludes object from surface culling"),
    ("256", "(SA)Disable_Draw_Distance", "Disables the object's draw distance"),
    ("512", "(SA)Breakable_Window", "Object is a breakable window"),
    ("1024", "(SA)Breakable_Window_With_Cracks", "Breakable window with cracks"),
    ("2048", "(SA)Garage_door", "Object is a garage door"),
    ("4096", "(SA)2-Clump-Object", "Object belongs to a clump"),
    ("8192", "(SA)Small-Vegetation-Strong-wind-Effect", "Small vegetation affected by strong wind"),
    ("16384", "(SA)Standard-Vegetation", "Standard vegetation object"),
    ("32768", "(SA)Timecycle-PoleShadow-Flag", "Used in timecycle pole shadows"),
    ("65536", "(SA)Explosive", "Explosive object"),
    ("131072", "(SA)UNKNOWN-(Seems to be an SCM Flag)", "Uncertain flag, possibly an SCM flag"),
    ("262144", "(SA)UNKNOWN-(1 Object in Jizzy`s Club)", "Uncertain flag related to Jizzy's Club"),
    ("524288", "(SA)(SA)UNKNOWN-(?)", "Uncertain or unused flag"),
    ("1048576", "(SA)Graffiti", "Object is graffiti"),
    ("2097152", "(SA)Disable-backface-culling", "Disables backface culling"),
    ("4194304", "(SA)UNKNOWN-Unused-(Parts of a statue in Atrium)", "Unused flag related to a statue"),
    ("1073741824", "(SA)Unknown", "An unknown flag"),
]

class IDEFlagsProperties(bpy.types.PropertyGroup):
    """Property group for IDE flags used by GTASceneSync."""
    ide_flag: bpy.props.EnumProperty(
        name="IDE Flag",
        description="Select the IDE flag for the object",
        items=IDE_FLAGS_ITEMS,
        default="0",
    )
    render_distance: bpy.props.IntProperty(
        name="Render Distance",
        description="Set the render distance for the object",
        default=299,
        min=0,
        max=1200,
        step=1,
    )
    texture_name: bpy.props.StringProperty(
        name="Texture Name",
        description="Specify the texture or TXD name for the object",
        default="generic",
    )

class GTASceneSyncPanel(bpy.types.Panel):
    """Panel for GTASceneSync settings on an object."""
    bl_label = "GTASceneSync"
    bl_idname = "OBJECT_PT_gtascenesync"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_category = "Item"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj:
            # Directly access the pointer property (assigned during registration)
            layout.prop(obj.ide_flags, "ide_flag")
            layout.prop(obj.ide_flags, "render_distance")
            layout.prop(obj.ide_flags, "texture_name")
        else:
            layout.label(text="No active object selected")

# List of classes for simplified registration/unregistration
classes = (
    IDEFlagsProperties,
    GTASceneSyncPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.ide_flags = bpy.props.PointerProperty(type=IDEFlagsProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.ide_flags

if __name__ == "__main__":
    register()