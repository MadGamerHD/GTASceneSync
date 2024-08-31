# SyncIPL_Export_III.py

import bpy
import math

def clean_name(name):
    """Remove numeric suffixes from the model name."""
    import re
    return re.sub(r'\.\d+$', '', name)

class ExportAsIPLIII(bpy.types.Operator):
    bl_idname = "export_scene.ipl_iii"
    bl_label = "Export Selected as IPL (GTA III)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(name="Model ID", default=3153)
    apply_default_rotation: bpy.props.BoolProperty(name="Apply Default Rotation", default=False)
    default_rotation: bpy.props.FloatVectorProperty(name="Default Rotation (Euler)", subtype="EULER", default=(0.0, 0.0, 0.0))

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model_id")
        layout.prop(self, "apply_default_rotation")
        if self.apply_default_rotation:
            layout.prop(self, "default_rotation")

    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, "No mesh objects selected for export.")
            return {'CANCELLED'}
        
        if not self.filepath.lower().endswith(".ipl"):
            self.filepath += ".ipl"
        
        with open(self.filepath, 'w') as file:
            file.write("inst\n")
            
            for obj in selected_objects:
                loc = obj.location
                
                if self.apply_default_rotation:
                    rot = self.default_rotation.to_quaternion()
                else:
                    rot = obj.rotation_euler.to_quaternion()

                model_name = clean_name(obj.name) if obj.name else "Unnamed"
                
                obj_id = self.model_id
                
                pos_x = round(loc.x, 3)
                pos_y = round(loc.y, 3)
                pos_z = round(loc.z, 3)
                
                # Use default scale (1, 1, 1) and convert quaternion values for rotation
                scale_x = scale_y = scale_z = 1
                rot_x = 0
                rot_y = 0
                rot_z = 0
                rot_w = 1
                
                # Write to file in the correct format
                line = f"{obj_id}, {model_name}, {pos_x:.3f}, {pos_y:.3f}, {pos_z:.3f}, {scale_x}, {scale_y}, {scale_z}, {rot_x}, {rot_y}, {rot_z}, {rot_w}\n"
                file.write(line)
            
            file.write("end\n")

        self.report({'INFO'}, "Export complete as IPL for GTA III!")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
