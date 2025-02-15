import bpy
import re


def clean_name(name):
    """Remove numeric suffixes from the model name."""
    return re.sub(r"\.\d+$", "", name)


class ExportAsIDE(bpy.types.Operator):
    """Export Selected Objects as IDE with Incremental Model IDs"""

    bl_idname = "export_scene.ide"
    bl_label = "Export Selected as IDE"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(name="Starting Model ID", default=18631)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model_id")

    def execute(self, context):
        selected_objects = [
            obj for obj in bpy.context.selected_objects if obj.type == "MESH"
        ]

        if not selected_objects:
            self.report({"WARNING"}, "No mesh objects selected for export.")
            return {"CANCELLED"}
        # Ensure the file has the .ide extension

        if not self.filepath.lower().endswith(".ide"):
            self.filepath += ".ide"
        unique_names = {}
        current_id = self.model_id

        with open(self.filepath, "w") as file:
            file.write("objs\n")

            for obj in selected_objects:
                base_name = clean_name(obj.name)

                # Get custom properties

                ide_flag = obj.ide_flags.ide_flag if hasattr(obj, "ide_flags") else "0"
                render_distance = (
                    obj.ide_flags.render_distance if hasattr(obj, "ide_flags") else 299
                )
                texture_name = (
                    obj.ide_flags.texture_name
                    if hasattr(obj, "ide_flags")
                    else "generic"
                )

                if base_name not in unique_names:
                    # Assign a unique ID to this base_name and increment for the next

                    unique_names[base_name] = (
                        current_id,
                        texture_name,
                        render_distance,
                        ide_flag,
                    )
                    current_id += 1
            for base_name, (
                obj_id,
                texture_name,
                render_distance,
                ide_flag,
            ) in unique_names.items():
                line = f"{obj_id}, {base_name}, {texture_name}, {render_distance}, {ide_flag}\n"
                file.write(line)
            file.write("end\n")
        self.report({"INFO"}, "Export complete as IDE!")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}