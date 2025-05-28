bl_info = {
    "name": "GTASceneSync (SA Only)",
    "author": "Your Name",
    "version": (2, 2, 0),
    "blender": (4, 0, 0),
    "location": "View3D > UI > GTASceneSync",
    "description": "Export GTA San Andreas IDE and IPL from Blender with batch and per-object settings + utility tools",
    "category": "Import-Export",
}

import bpy
import re
import struct
import mathutils
from pathlib import Path

# ----------------------------
# Helper Functions
# ----------------------------

def clean_name(name: str) -> str:
    """Remove numeric suffixes from the model name."""
    return re.sub(r"\.\d+$", "", name)

# ----------------------------
# Operators: GTASceneSync
# ----------------------------
class ExportAsIDE(bpy.types.Operator):
    bl_idname = "export_scene.ide"
    bl_label = "Export Selected as IDE"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(name="Starting Model ID", default=18631)

    def draw(self, context):
        self.layout.prop(self, "model_id")

    def execute(self, context):
        objs = [o for o in context.selected_objects if o.type == 'MESH']
        if not objs:
            self.report({'WARNING'}, "No mesh objects selected.")
            return {'CANCELLED'}
        if not self.filepath.lower().endswith('.ide'):
            self.filepath += '.ide'
        unique = {}
        cur = self.model_id
        with open(self.filepath, 'w') as f:
            f.write('objs\n')
            for obj in objs:
                base = clean_name(obj.name)
                props = obj.ide_flags
                if base not in unique:
                    unique[base] = (cur, props.texture_name, props.render_distance, props.ide_flag)
                    cur += 1
            for name, (mid, txd, dist, flag) in unique.items():
                f.write(f"{mid}, {name}, {txd}, {dist}, {flag}\n")
            f.write('end\n')
        self.report({'INFO'}, f"IDE export complete: {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class ExportAsIPL(bpy.types.Operator):
    bl_idname = "export_scene.ipl"
    bl_label = "Export Selected as IPL"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(name="Starting Model ID", default=18631)
    apply_default_rotation: bpy.props.BoolProperty(name="Apply Default Rotation", default=False)
    default_rotation: bpy.props.FloatVectorProperty(name="Default Rotation (Euler)", subtype='EULER', default=(0,0,0))
    export_type: bpy.props.EnumProperty(
        name="Export Type",
        items=[('normal','ASCII .ipl',''),('bnry','Binary .ipl','')],
        default='normal'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'model_id')
        layout.prop(self, 'apply_default_rotation')
        if self.apply_default_rotation:
            layout.prop(self, 'default_rotation')
        layout.prop(self, 'export_type')

    def validate_filepath(self):
        p = Path(self.filepath)
        if p.suffix.lower() != '.ipl':
            p = p.with_suffix('.ipl')
        self.filepath = str(p)

    def generate_mapping(self, objs):
        mapping, cur = {}, self.model_id
        for o in objs:
            n = clean_name(o.name) or 'Unnamed'
            if n not in mapping:
                mapping[n] = cur
                cur += 1
        return mapping

    def write_ipl(self, f, objs, mapping):
        inter, lod = 0, -1
        fmt = lambda v: f"{v:.6f}"
        if self.export_type == 'normal':
            f.write('# Exported with GTASceneSync\ninst\n')
            for obj in objs:
                wm = obj.matrix_world
                pos = wm.to_translation(); base = wm.to_quaternion()
                if self.apply_default_rotation:
                    off = mathutils.Euler(self.default_rotation,'XYZ').to_quaternion()
                    base = off @ base
                rx, ry, rz, rw = -base.x, base.y, -base.z, base.w
                mid = mapping.get(clean_name(obj.name), -1)
                nm = clean_name(obj.name) or 'Unnamed'
                f.write(
                    f"{mid}, {nm}, {inter}, {fmt(pos.x)}, {fmt(pos.y)}, {fmt(pos.z)}, {fmt(rx)}, {fmt(ry)}, {fmt(rz)}, {fmt(rw)}, {lod}\n"
                )
            f.write('end\n')
        else:
            for obj in objs:
                wm = obj.matrix_world
                pos = wm.to_translation(); base = wm.to_quaternion()
                if self.apply_default_rotation:
                    off = mathutils.Euler(self.default_rotation,'XYZ').to_quaternion()
                    base = off @ base
                rx, ry, rz, rw = -base.x, base.y, -base.z, base.w
                mid = mapping.get(clean_name(obj.name), -1)
                rec = struct.pack('<7f3i', pos.x, pos.y, pos.z, rx, ry, rz, rw, mid, inter, lod)
                f.write(rec)

    def execute(self, context):
        objs = [o for o in context.selected_objects if o.type == 'MESH']
        if not objs:
            self.report({'WARNING'}, "No mesh objects selected.")
            return {'CANCELLED'}
        self.validate_filepath()
        mapping = self.generate_mapping(objs)
        mode = 'wb' if self.export_type=='bnry' else 'w'
        try:
            with open(self.filepath, mode) as f:
                self.write_ipl(f, objs, mapping)
        except Exception as e:
            self.report({'ERROR'}, f"IPL export failed: {e}")
            return {'CANCELLED'}
        self.report({'INFO'}, f"IPL export complete: {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# ----------------------------
# Operators: Utilities
# ----------------------------
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
        for obj in selected_objects:
            if obj.type == "MESH":
                obj.data.materials.clear()
        self.report({'INFO'}, "Materials removed from selected objects.")
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

# ----------------------------
# PropertyGroup
# ----------------------------
IDE_FLAGS = [
    ("0", "(SA)Default", "No special flags"),
    # ... as before ...
]
class IDEFlagsProperties(bpy.types.PropertyGroup):
    ide_flag: bpy.props.EnumProperty(name="IDE Flag", items=IDE_FLAGS, default='0')
    render_distance: bpy.props.IntProperty(name="Render Distance", default=299, min=0, max=1200)
    texture_name: bpy.props.StringProperty(name="Texture Name", default='generic')

# ----------------------------
# UI Panel
# ----------------------------
class GTASceneSyncUIPanel(bpy.types.Panel):
    bl_label = "GTASceneSync"
    bl_idname = "VIEW3D_PT_gtascenesync"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GTASceneSync'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Utility Tools
        layout.label(text="Utilities:")
        row = layout.row(align=True)
        row.prop(scene, 'batch_rename_base_name', text='Rename Base')
        row.operator(OBJECT_OT_batch_rename.bl_idname, text='Rename')
        row = layout.row(align=True)
        row.operator(OBJECT_OT_reset_position.bl_idname, text='Reset Pos')
        row = layout.row(align=True)
        row.operator(OBJECT_OT_remove_materials.bl_idname, text='Remove Mats')
        row = layout.row(align=True)
        row.operator(OBJECT_OT_convert_to_collision.bl_idname, text='To Collision')
        layout.separator()

        # Batch TXD
        layout.label(text="Batch assign TXD for selected:")
        layout.prop(scene, 'batch_txd_name', text='TXD Name')
        layout.operator('gtascenesync.batch_txd', text='Set TXD')
        layout.separator()

        # Per-object settings
        layout.label(text="Selected Object Settings:")
        for obj in context.selected_objects:
            if obj.type != 'MESH': continue
            box = layout.box()
            box.label(text=obj.name)
            box.prop(obj.ide_flags, 'texture_name', text='TXD')
            box.prop(obj.ide_flags, 'ide_flag', text='Flag')
            box.prop(obj.ide_flags, 'render_distance', text='Draw Dist')
        layout.separator()

        # Export buttons
        layout.label(text="Exports:")
        layout.operator(ExportAsIDE.bl_idname, text="Export IDE")
        layout.operator(ExportAsIPL.bl_idname, text="Export IPL")

# ----------------------------
# Batch TXD Operator
# ----------------------------
class BatchSetTXD(bpy.types.Operator):
    bl_idname = "gtascenesync.batch_txd"
    bl_label = "Set TXD for Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        txd = context.scene.batch_txd_name.strip()
        if not txd:
            self.report({'WARNING'}, "TXD name is empty.")
            return {'CANCELLED'}
        count = 0
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.ide_flags.texture_name = txd
                count += 1
        self.report({'INFO'}, f"Set TXD '{txd}' for {count} objects.")
        return {'FINISHED'}

# ----------------------------
# Registration
# ----------------------------
classes = [
    ExportAsIDE, ExportAsIPL, BatchSetTXD,
    OBJECT_OT_batch_rename, OBJECT_OT_reset_position,
    OBJECT_OT_remove_materials, OBJECT_OT_convert_to_collision,
    IDEFlagsProperties, GTASceneSyncUIPanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.ide_flags = bpy.props.PointerProperty(type=IDEFlagsProperties)
    bpy.types.Scene.batch_txd_name = bpy.props.StringProperty(name="Batch TXD Name", default="generic")
    bpy.types.Scene.batch_rename_base_name = bpy.props.StringProperty(name="Base Rename Name", default="TypeName")


def unregister():
    del bpy.types.Object.ide_flags
    del bpy.types.Scene.batch_txd_name
    del bpy.types.Scene.batch_rename_base_name
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()
