import bpy
import re

def clean_name(name):
    """Remove numeric suffixes from the model name."""
    return re.sub(r"\.\d+$", "", name)


class ExportAsIPL(bpy.types.Operator):
    """Export Selected Objects as IPL with Incremental Model IDs"""

    bl_idname = "export_scene.ipl"
    bl_label = "Export Selected as IPL (GTA SA)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(
        name="Starting Model ID", 
        default=19378,
        description="Starting ID for the models"
    )
    apply_default_rotation: bpy.props.BoolProperty(
        name="Apply Default Rotation",
        default=False,
        description="Apply a default rotation to all models"
    )
    default_rotation: bpy.props.FloatVectorProperty(
        name="Default Rotation (Euler)",
        subtype="EULER",
        default=(0.0, 0.0, 0.0),
        description="Default rotation values in Euler angles"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model_id")
        layout.prop(self, "apply_default_rotation")
        if self.apply_default_rotation:
            layout.prop(self, "default_rotation")

    def validate_filepath(self):
        """Ensure the filepath has a valid .ipl extension."""
        if not self.filepath.lower().endswith(".ipl"):
            self.filepath += ".ipl"

    def generate_model_id_mapping(self, selected_objects):
        """Generate a mapping of model names to unique IDs."""
        model_id_mapping = {}
        current_id = self.model_id

        for obj in selected_objects:
            model_name = clean_name(obj.name) if obj.name else "Unnamed"
            if model_name not in model_id_mapping:
                model_id_mapping[model_name] = current_id
                current_id += 1  # Increment ID for next unique name

        return model_id_mapping

    def write_ipl_file(self, file, selected_objects, model_id_mapping):
        """Write the IPL file content."""
        file.write("inst\n")
        for obj in selected_objects:
            loc = obj.location
            rot = (
                self.default_rotation.to_quaternion()
                if self.apply_default_rotation
                else obj.rotation_euler.to_quaternion()
            )

            model_name = clean_name(obj.name) if obj.name else "Unnamed"
            obj_id = model_id_mapping.get(model_name, -1)

            # Round values for IPL format
            pos_x, pos_y, pos_z = round(loc.x, 6), round(loc.y, 6), round(loc.z, 6)
            quat_x, quat_y, quat_z, quat_w = (
                round(rot.x, 6),
                round(rot.y, 6),
                round(rot.z, 6),
                round(rot.w, 6),
            )

            # Write object data
            line = (
                f"{obj_id}, {model_name}, 0, {pos_x:.6f}, {pos_y:.6f}, {pos_z:.6f}, "
                f"{quat_x:.6f}, {quat_y:.6f}, {quat_z:.6f}, {quat_w:.6f}, -1\n"
            )
            file.write(line)

        file.write("end\n")

    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]

        if not selected_objects:
            self.report({"WARNING"}, "No mesh objects selected for export.")
            return {"CANCELLED"}

        # Validate filepath and create model ID mapping
        self.validate_filepath()
        model_id_mapping = self.generate_model_id_mapping(selected_objects)

        # Write the IPL file
        try:
            with open(self.filepath, "w") as file:
                self.write_ipl_file(file, selected_objects, model_id_mapping)
        except Exception as e:
            self.report({"ERROR"}, f"Failed to export IPL: {e}")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Export complete as IPL! File saved to: {self.filepath}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


# Register the operator
def menu_func_export(self, context):
    self.layout.operator(ExportAsIPL.bl_idname, text="Export Selected as IPL (GTA SA)")


def register():
    bpy.utils.register_class(ExportAsIPL)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportAsIPL)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()