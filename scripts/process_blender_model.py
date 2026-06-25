import bpy
import sys
import os

def process_blender_model(input_obj_path, output_glb_path):
    print(f"Processing 3D model in Blender: {input_obj_path}")
    print(f"Output will be saved to: {output_glb_path}")

    # Clear existing objects in Blender
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Import the OBJ file
    try:
        # Check Blender version to use the correct operator
        if bpy.app.version >= (4, 0, 0):
            # Blender 4.0+ uses a new operator for OBJ import
            bpy.ops.wm.obj_import(filepath=input_obj_path)
        else:
            # Older versions
            bpy.ops.import_scene.obj(filepath=input_obj_path)
    except Exception as e:
        print(f"Error importing OBJ: {e}")
        # Fallback: Try the other one just in case
        try:
            bpy.ops.wm.obj_import(filepath=input_obj_path)
        except:
            sys.exit(1)

    # Here you can add Blender processing steps:
    # - Scaling
    # - Smoothing
    # - Decimation
    # - Material assignment
    # - Rigging (if applicable)

    # Process the mesh
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            
            # 1. Apply Smooth Shading
            bpy.ops.object.shade_smooth()
            
            # 2. Add Subdivision Surface modifier for higher quality
            mod = obj.modifiers.new(name="Subdiv", type='SUBSURF')
            mod.levels = 2
            mod.render_levels = 2
            
            # 3. Add a simple material
            mat = bpy.data.materials.new(name="MannequinMaterial")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            bsdf = nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0) # Grey
                bsdf.inputs['Roughness'].default_value = 0.4
            
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)

    # Export to GLB format
    try:
        # Note: In newer Blender versions, use bpy.ops.export_scene.gltf
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_glb_path), exist_ok=True)
        bpy.ops.export_scene.gltf(filepath=output_glb_path, export_format='GLB')
    except Exception as e:
        print(f"Error exporting GLB: {e}")
        sys.exit(1)

    print("Blender processing complete and model exported to GLB.")


if __name__ == "__main__":
    # Get arguments passed after --
    argv = sys.argv
    try:
        index = argv.index("--") + 1
    except ValueError:
        index = len(argv)
    argv = argv[index:]

    if len(argv) != 2:
        print("Usage: blender --background --python process_blender_model.py -- <input_obj_path> <output_glb_path>")
        sys.exit(1)

    input_obj = argv[0]
    output_glb = argv[1]

    process_blender_model(input_obj, output_glb)
