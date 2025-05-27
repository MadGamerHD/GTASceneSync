bl_info = {
    "name": "GTASceneSync (SA Only)",
    "author": "Your Name",
    "version": (2, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > UI > GTASceneSync",
    "description": "Export GTA San Andreas IDE and IPL from Blender with batch and per-object settings",
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
# Operators
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
                flag = props.ide_flag
                dist = props.render_distance
                txd  = props.texture_name
                if base not in unique:
                    unique[base] = (cur, txd, dist, flag)
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
                nm  = clean_name(obj.name) or 'Unnamed'
                f.write(f"{mid}, {nm}, {inter}, {fmt(pos.x)}, {fmt(pos.y)}, {fmt(pos.z)}, {fmt(rx)}, {fmt(ry)}, {fmt(rz)}, {fmt(rw)}, {lod}\n")
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
# PropertyGroup
# ----------------------------
IDE_FLAGS = [
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

        # Batch TXD
        layout.label(text="Batch assign TXD for selected:")
        layout.prop(scene, 'batch_txd_name', text='TXD Name')
        layout.operator(BatchSetTXD.bl_idname, text='Set TXD')
        layout.separator()

        # Per-object settings
        layout.label(text="Selected Object Settings:")
        for obj in context.selected_objects:
            if obj.type != 'MESH': continue
            box = layout.box()
            row = box.row()
            row.label(text=obj.name)
            box.prop(obj.ide_flags, 'texture_name', text='TXD')
            box.prop(obj.ide_flags, 'ide_flag', text='Flag')
            box.prop(obj.ide_flags, 'render_distance', text='Draw Dist')
        layout.separator()

        # Export buttons
        layout.label(text="Exports:")
        layout.operator(ExportAsIDE.bl_idname, text="Export IDE")
        layout.operator(ExportAsIPL.bl_idname, text="Export IPL")

# ----------------------------
# Registration
# ----------------------------
classes = [ExportAsIDE, ExportAsIPL, BatchSetTXD, IDEFlagsProperties, GTASceneSyncUIPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.ide_flags = bpy.props.PointerProperty(type=IDEFlagsProperties)
    bpy.types.Scene.batch_txd_name = bpy.props.StringProperty(name="Batch TXD Name", default="generic")


def unregister():
    del bpy.types.Object.ide_flags
    del bpy.types.Scene.batch_txd_name
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()