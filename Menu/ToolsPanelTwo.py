import bpy


class OBJECT_OT_set_texture_name(bpy.types.Operator):
    """Set Texture Name for Selected Objects"""

    bl_idname = "object.set_texture_name"
    bl_label = "Set Texture Name"
    bl_options = {"REGISTER", "UNDO"}

    texture_name: bpy.props.StringProperty(name="Texture Name", default="generic")

    def execute(self, context):
        # Iterate over selected objects

        for obj in context.selected_objects:
            if obj.type == "MESH" and hasattr(obj, "ide_flags"):
                obj.ide_flags.texture_name = self.texture_name  # Set texture name
        return {"FINISHED"}


class ToolsPanelTwo(bpy.types.Panel):
    """Panel to Set Texture Name for Selected Models"""

    bl_label = "Tools - Set Texture Name"
    bl_idname = "OBJECT_PT_tools_set_texture_name"
    bl_space_type = "VIEW_3D"  # Change to your desired space type
    bl_region_type = "UI"  # The panel will be in the side bar
    bl_category = "Tools"  # Category name for the sidebar

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "texture_name")
        layout.operator(OBJECT_OT_set_texture_name.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_set_texture_name)
    bpy.utils.register_class(ToolsPanelTwo)

    # Create a string property on the scene to hold the texture name

    bpy.types.Scene.texture_name = bpy.props.StringProperty(
        name="Texture Name",
        description="Name of the texture to set for selected objects",
        default="generic",
    )


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_set_texture_name)
    bpy.utils.unregister_class(ToolsPanelTwo)
    del bpy.types.Scene.texture_name


if __name__ == "__main__":
    register()