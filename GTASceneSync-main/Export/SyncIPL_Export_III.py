import bpy
import re
import mathutils
from pathlib import Path

def clean_name(name: str) -> str:
    """Remove numeric suffixes from the model name."""
    return re.sub(r"\.\d+$", "", name)

class ExportAsIPLIII(bpy.types.Operator):
    """Export Selected Objects as IPL for GTA III with a single model ID."""
    bl_idname = "export_scene.ipl_iii"
    bl_label = "Export Selected as IPL (GTA III)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(name="Model ID", default=3153)
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
        selected_objects = [obj for obj in context.selected_objects if obj.type == "MESH"]
        if not selected_objects:
            self.report({"WARNING"}, "No mesh objects selected for export.")
            return {"CANCELLED"}

        # Ensure the filepath has a .ipl extension using pathlib
        path = Path(self.filepath)
        if path.suffix.lower() != ".ipl":
            path = path.with_suffix(".ipl")
        self.filepath = str(path)

        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                file.write("inst\n")

                for obj in selected_objects:
                    loc = obj.location

                    # Determine rotation: use default rotation if enabled, otherwise the object's rotation.
                    if self.apply_default_rotation:
                        # Convert the tuple to an Euler, then to a quaternion.
                        rot = mathutils.Euler(self.default_rotation).to_quaternion()
                    else:
                        rot = obj.rotation_euler.to_quaternion()

                    model_name = clean_name(obj.name) if obj.name else "Unnamed"
                    obj_id = self.model_id

                    # Round the position values
                    pos_x = round(loc.x, 3)
                    pos_y = round(loc.y, 3)
                    pos_z = round(loc.z, 3)

                    # Use default scale (1,1,1) and the computed quaternion for rotation.
                    scale_x = scale_y = scale_z = 1
                    rot_x = round(rot.x, 3)
                    rot_y = round(rot.y, 3)
                    rot_z = round(rot.z, 3)
                    rot_w = round(rot.w, 3)

                    # Format the line according to the IPL format.
                    line = (
                        f"{obj_id}, {model_name}, {pos_x:.3f}, {pos_y:.3f}, {pos_z:.3f}, "
                        f"{scale_x}, {scale_y}, {scale_z}, {rot_x}, {rot_y}, {rot_z}, {rot_w}\n"
                    )
                    file.write(line)

                file.write("end\n")
        except Exception as e:
            self.report({"ERROR"}, f"Failed to export IPL: {e}")
            return {"CANCELLED"}

        self.report({"INFO"}, "Export complete as IPL for GTA III!")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}