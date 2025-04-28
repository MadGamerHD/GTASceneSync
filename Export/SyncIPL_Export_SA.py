import bpy
import re
import struct
import mathutils
from pathlib import Path


def clean_name(name: str) -> str:
    """Remove numeric suffixes from the model name."""
    return re.sub(r"\.\d+$", "", name)


class ExportAsIPL(bpy.types.Operator):
    """Export Selected Objects as IPL with Incremental Model IDs"""
    bl_idname = "export_scene.ipl"
    bl_label = "Export Selected as IPL (GTA SA)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(
        name="Starting Model ID",
        default=4542,
        description="Starting ID for the models",
    )
    apply_default_rotation: bpy.props.BoolProperty(
        name="Apply Default Rotation",
        default=False,
        description="Apply a default rotation to all models before GTA conversion",
    )
    default_rotation: bpy.props.FloatVectorProperty(
        name="Default Rotation (Euler)",
        subtype="EULER",
        default=(0.0, 0.0, 0.0),
        description="Default Euler rotation (radians) applied in Blender space",
    )
    export_type: bpy.props.EnumProperty(
        name="Export Type",
        description="Choose the export format",
        items=[
            ('normal', "ASCII .ipl", "Export as human-readable .ipl"),
            ('bnry',   "Binary .ipl", "Export as raw binary .ipl"),
        ],
        default='normal',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model_id")
        layout.prop(self, "apply_default_rotation")
        if self.apply_default_rotation:
            layout.prop(self, "default_rotation")
        layout.prop(self, "export_type")

    def validate_filepath(self):
        p = Path(self.filepath)
        if p.suffix.lower() != ".ipl":
            p = p.with_suffix(".ipl")
        self.filepath = str(p)

    def generate_model_id_mapping(self, objects):
        mapping = {}
        cur_id = self.model_id
        for obj in objects:
            name = clean_name(obj.name) if obj.name else "Unnamed"
            if name not in mapping:
                mapping[name] = cur_id
                cur_id += 1
        return mapping

    def write_ipl_file(self, file, objects, mapping):
        # GTA SA IPL inst format: Id, ModelName, Flags/Interior, PosX, PosY, PosZ,
        # RotX, RotY, RotZ, RotW, LOD
        interior = 0
        lod_index = -1
        pos_fmt = lambda v: f"{v:.6f}"
        rot_fmt = lambda v: f"{v:.6f}"

        if self.export_type == 'normal':
            file.write("# Exported with GTASceneSync\n")
            file.write("inst\n")
            for obj in objects:
                # Get world-space translation and quaternion
                wm = obj.matrix_world
                pos = wm.to_translation()
                base_q = wm.to_quaternion()

                # Apply optional default rotation in Blender space
                if self.apply_default_rotation:
                    offset_q = mathutils.Euler(self.default_rotation, 'XYZ').to_quaternion()
                    base_q = offset_q @ base_q

                # Convert Blender quaternion (w,x,y,z) to GTA (RotX,RotY,RotZ,RotW) = (-x, y, -z, w)
                rot_x = -base_q.x
                rot_y =  base_q.y
                rot_z = -base_q.z
                rot_w =  base_q.w

                mid = mapping.get(clean_name(obj.name), -1)
                name = clean_name(obj.name) or "Unnamed"

                # Write fields in correct order
                line = (
                    f"{mid}, {name}, {interior}, "
                    f"{pos_fmt(pos.x)}, {pos_fmt(pos.y)}, {pos_fmt(pos.z)}, "
                    f"{rot_fmt(rot_x)}, {rot_fmt(rot_y)}, {rot_fmt(rot_z)}, {rot_fmt(rot_w)}, "
                    f"{lod_index}\n"
                )
                file.write(line)
            file.write("end\n")
        else:
            for obj in objects:
                wm = obj.matrix_world
                pos = wm.to_translation()
                base_q = wm.to_quaternion()
                if self.apply_default_rotation:
                    offset_q = mathutils.Euler(self.default_rotation, 'XYZ').to_quaternion()
                    base_q = offset_q @ base_q

                # Manual quaternion conversion
                rot_x = -base_q.x
                rot_y =  base_q.y
                rot_z = -base_q.z
                rot_w =  base_q.w
                mid = mapping.get(clean_name(obj.name), -1)

                record = struct.pack(
                    '<7f3i',
                    pos.x, pos.y, pos.z,
                    rot_x, rot_y, rot_z, rot_w,
                    mid, interior, lod_index
                )
                file.write(record)

    def execute(self, context):
        objects = [o for o in context.selected_objects if o.type == 'MESH']
        if not objects:
            self.report({'WARNING'}, "No mesh objects selected for export.")
            return {'CANCELLED'}

        self.validate_filepath()
        mapping = self.generate_model_id_mapping(objects)
        mode = 'wb' if self.export_type == 'bnry' else 'w'
        try:
            with open(self.filepath, mode) as f:
                self.write_ipl_file(f, objects, mapping)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export IPL: {e}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Export complete: {len(objects)} objects → {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_func_export(self, context):
    self.layout.operator(ExportAsIPL.bl_idname, text="Export Selected as IPL (GTA SA)")


def register():
    bpy.utils.register_class(ExportAsIPL)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportAsIPL)

if __name__ == "__main__":
    register()
