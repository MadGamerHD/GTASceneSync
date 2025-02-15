import bpy
import re
import mathutils
from pathlib import Path

def clean_name(name: str) -> str:
    """Remove numeric suffixes from the model name."""
    return re.sub(r"\.\d+$", "", name)

class ExportAsIPLVC(bpy.types.Operator):
    """Export Selected Objects as IPL with VC Format"""

    bl_idname = "export_scene.ipl_vc"
    bl_label = "Export Selected as IPL (GTA VC)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(name="Starting Model ID", default=4794)
    apply_default_rotation: bpy.props.BoolProperty(
        name="Apply Default Rotation", default=False
    )
    default_rotation: bpy.props.FloatVectorProperty(
        name="Default Rotation (Euler)",
        subtype="EULER",
        default=(0.0, 0.0, 0.0)
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model_id")
        layout.prop(self, "apply_default_rotation")
        if self.apply_default_rotation:
            layout.prop(self, "default_rotation")

    def execute(self, context):
        # Use the context passed into the operator
        selected_objects = [obj for obj in context.selected_objects if obj.type == "MESH"]

        if not selected_objects:
            self.report({"WARNING"}, "No mesh objects selected for export.")
            return {"CANCELLED"}

        # Ensure the file has the .ipl extension using pathlib
        path = Path(self.filepath)
        if path.suffix.lower() != ".ipl":
            path = path.with_suffix(".ipl")
        self.filepath = str(path)

        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                file.write("inst\n")

                for obj in selected_objects:
                    loc = obj.location

                    # Use default rotation if specified, otherwise use the object's rotation
                    if self.apply_default_rotation:
                        # Convert the default rotation tuple to an Euler, then to a quaternion
                        rot_euler = mathutils.Euler(self.default_rotation)
                    else:
                        rot_euler = obj.rotation_euler
                    rot_quat = rot_euler.to_quaternion()

                    # Clean the object name
                    model_name = clean_name(obj.name) if obj.name else "Unnamed"

                    # Round position values
                    pos_x = round(loc.x, 6)
                    pos_y = round(loc.y, 6)
                    pos_z = round(loc.z, 6)

                    # Round quaternion components for consistency
                    rot_x = round(rot_quat.x, 6)
                    rot_y = round(rot_quat.y, 6)
                    rot_z = round(rot_quat.z, 6)
                    rot_w = round(rot_quat.w, 6)

                    # Write the line in VC format (using default scale values of 1.0)
                    line = (
                        f"{self.model_id}, {model_name}, 0, {pos_x:.6f}, {pos_y:.6f}, {pos_z:.6f}, "
                        f"{rot_x}, {rot_y}, {rot_z}, 1.0, 1.0, 1.0, {rot_w}\n"
                    )
                    file.write(line)

                    # Increment model ID for the next object
                    self.model_id += 1

                file.write("end\n")
        except Exception as e:
            self.report({"ERROR"}, f"Failed to export IPL: {e}")
            return {"CANCELLED"}

        self.report({"INFO"}, "Export complete as IPL (VC)!")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


def register():
    bpy.utils.register_class(ExportAsIPLVC)


def unregister():
    bpy.utils.unregister_class(ExportAsIPLVC)


if __name__ == "__main__":
    register()