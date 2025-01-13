import bpy


class OBJECT_OT_batch_rename(bpy.types.Operator):
    """Renames selected objects with a base name followed by numbers"""

    bl_idname = "object.batch_rename"
    bl_label = "Batch Rename Objects"
    bl_options = {"REGISTER", "UNDO"}

    base_name: bpy.props.StringProperty(
        name="Base Name",
        description="Base name for renaming objects",
        default="TypeName",
    )

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({"WARNING"}, "No objects selected!")
            return {"CANCELLED"}
        # Rename the objects with base name and numerical suffix

        for i, obj in enumerate(selected_objects, start=1):
            obj.name = f"{self.base_name}_{i}"
        return {"FINISHED"}


class OBJECT_OT_reset_position(bpy.types.Operator):
    """Sets the position of selected objects to (0, 0, 0)"""

    bl_idname = "object.reset_position"
    bl_label = "Reset Position"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({"WARNING"}, "No objects selected!")
            return {"CANCELLED"}
        # Set position of selected objects to (0, 0, 0)

        for obj in selected_objects:
            obj.location = (0, 0, 0)
        return {"FINISHED"}


class OBJECT_OT_remove_materials(bpy.types.Operator):
    """Removes all materials from selected objects"""

    bl_idname = "object.remove_materials"
    bl_label = "Remove All Materials"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({"WARNING"}, "No objects selected!")
            return {"CANCELLED"}
        # Remove all materials from selected objects

        for obj in selected_objects:
            if obj.type == "MESH":
                obj.data.materials.clear()
        self.report({"INFO"}, "Materials removed from selected objects.")
        return {"FINISHED"}


class OBJECT_OT_convert_to_collision(bpy.types.Operator):
    """Convert selected objects to Collision Object"""

    bl_idname = "object.convert_to_collision"
    bl_label = "Convert to Collision Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected_objects = context.selected_objects
        for obj in selected_objects:
            if obj.type == "MESH":  # Assuming we only want to change mesh objects
                # Example: Assuming you have a custom property to store type info

                if not hasattr(obj, "dff"):
                    obj.dff = bpy.props.PointerProperty(
                        type=bpy.types.PropertyGroup
                    )  # Create a custom property group if needed
                obj.dff.type = "COL"  # Set type to 'COL' (Collision Object)
        return {"FINISHED"}


class VIEW3D_PT_batch_rename_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""

    bl_label = "Batch Rename, Reset Position, Remove Materials, and Convert to Collision Objects"
    bl_idname = "VIEW3D_PT_batch_rename_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout

        # Create a reference to the operator's property

        layout.label(text="Rename selected objects:")
        layout.prop(
            context.scene, "batch_rename_base_name", text="Base Name"
        )  # Property input for base name
        layout.operator("object.batch_rename", text="Batch Rename")

        layout.label(text="Reset position of selected objects:")
        layout.operator("object.reset_position", text="Reset Position")

        layout.label(text="Remove materials from selected objects:")
        layout.operator("object.remove_materials", text="Remove Materials")

        layout.label(text="Convert selected objects to Collision Objects:")
        layout.operator("object.convert_to_collision", text="Convert to Collision")


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_batch_rename.bl_idname)
    self.layout.operator(OBJECT_OT_reset_position.bl_idname)
    self.layout.operator(OBJECT_OT_remove_materials.bl_idname)
    self.layout.operator(OBJECT_OT_convert_to_collision.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_batch_rename)
    bpy.utils.register_class(OBJECT_OT_reset_position)
    bpy.utils.register_class(OBJECT_OT_remove_materials)
    bpy.utils.register_class(OBJECT_OT_convert_to_collision)
    bpy.utils.register_class(VIEW3D_PT_batch_rename_panel)

    # Add a StringProperty to the Scene to store the base name input from the user

    bpy.types.Scene.batch_rename_base_name = bpy.props.StringProperty(
        name="Base Name",
        description="Base name for renaming objects",
        default="WuhuPart",
    )

    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_batch_rename)
    bpy.utils.unregister_class(OBJECT_OT_reset_position)
    bpy.utils.unregister_class(OBJECT_OT_remove_materials)
    bpy.utils.unregister_class(OBJECT_OT_convert_to_collision)
    bpy.utils.unregister_class(VIEW3D_PT_batch_rename_panel)

    del bpy.types.Scene.batch_rename_base_name  # Remove the custom property

    bpy.types.VIEW3D_MT_object.remove(menu_func)