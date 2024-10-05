import bpy
import re

def clean_name(name):
    """Remove numeric suffixes from the model name."""
    return re.sub(r'\.\d+$', '', name)

class ExportAsIPL(bpy.types.Operator):
    """Export Selected Objects as IPL with Incremental Model IDs"""
    bl_idname = "export_scene.ipl"
    bl_label = "Export Selected as IPL (GTA SA)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(name="Starting Model ID", default=19378)
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
        
        # Ensure the file has the .ipl extension
        if not self.filepath.lower().endswith(".ipl"):
            self.filepath += ".ipl"
        
        model_id_mapping = {}
        current_id = self.model_id
        
        with open(self.filepath, 'w') as file:
            file.write("inst\n")
            
            for obj in selected_objects:
                loc = obj.location
                
                # Apply the default rotation or use the object's own rotation
                if self.apply_default_rotation:
                    rot = self.default_rotation.to_quaternion()
                else:
                    rot = obj.rotation_euler.to_quaternion()
                
                # Clean the name to remove any numeric suffixes
                model_name = clean_name(obj.name) if obj.name else "Unnamed"
                
                # Assign ID based on model name
                if model_name not in model_id_mapping:
                    model_id_mapping[model_name] = current_id
                    current_id += 1  # Increment ID for next unique name
                
                obj_id = model_id_mapping[model_name]
                
                pos_x = round(loc.x, 6)
                pos_y = round(loc.y, 6)
                pos_z = round(loc.z, 6)
                
                # Use quaternion values without converting to integers
                quat_x = round(rot.x, 6)
                quat_y = round(rot.y, 6)
                quat_z = round(rot.z, 6)
                quat_w = round(rot.w, 6)
                
                # Write to file in the correct format with quaternion rotations
                line = f"{obj_id}, {model_name}, 0, {pos_x:.6f}, {pos_y:.6f}, {pos_z:.6f}, {quat_x:.6f}, {quat_y:.6f}, {quat_z:.6f}, {quat_w:.6f}, -1\n"
                file.write(line)
            
            file.write("end\n")

        self.report({'INFO'}, "Export complete as IPL!")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}