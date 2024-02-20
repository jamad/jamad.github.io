<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />

# 連番静止画から動画の作成方法　Scriptで簡単にできそう
* sequencer に切り替え、連番画像を読み込みし、movieに切り替えて render animation すれば C:\tmp に動画が作成された
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/7a786188-69c3-40ae-9d07-fcd9df7eb5a6)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/4e5d2629-1221-4f06-823e-31026b2ea472)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/12d49ed4-70a4-4a55-9714-de3ec21490ee)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/96e089dd-613f-4225-a1df-7be8f3d4aac3)
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/2defe826-86a1-47d9-850b-20b1eb9622d9)






# tips
#### blender tips 200
* 1 - absolute grid snap checkbox
* 2 - presets
* 3 - navigate hierarchy by [ ] (up and down)
* 4 - focus shift (alt+MMB click)  not drag because it rotates the view
* 5 - ?
* 109 : i key to skip selecting location etc  (  Timeline > Keying > Active Keying sets )

# troubleshooting_blender
* get object in the scene by name
  * ob = bpy.context.scene.objects["Cube"]
  * dt = ob.data

# how_to_blender

## numpyを扱う
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/aab25db9-11b8-4ae1-aba4-f5bfb2727e35)

```
import subprocess

try:
    import numpy as np
except:
    command="pip install numpy"
    result = subprocess.check_output(command.split())
    print(result)
   
import numpy as np
A=[[1,2,3],[4,5,6]]
M = np.array(A, int)
for X in (M, np.rot90(M),np.fliplr(M), np.flipud(M)):
    print(X)
    print('-'*20)
```


# Iteration - seelcted objects
* before-after ![image](https://github.com/jamad/jamad.github.io/assets/949913/b84824bb-70d9-4a2a-b074-43d69c9586eb) >>  ![image](https://github.com/jamad/jamad.github.io/assets/949913/1c68a32a-44d5-4d0c-a668-2b2efcd0d8b6)

```
import bpy
for obj in bpy.context.selected_objects:
    obj.name='new_name'
```


# shader node	
* before-after ![image](https://github.com/jamad/jamad.github.io/assets/949913/6aee3d27-9e8f-4bde-bb3a-a9139b3adac8) >> ![image](https://github.com/jamad/jamad.github.io/assets/949913/e4e6b192-0781-4576-9544-fa722ebaee52)

```
import bpy
mat = bpy.data.materials.new('Hoge')
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
texImage = mat.node_tree.nodes.new('ShaderNodeTexMagic')
mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
ob =bpy.context.view_layer.objects.active    #
if ob.data.materials:    ob.data.materials[0] = mat
else: ob.data.materials.append(mat)           
```

* example after the script ![image](https://github.com/jamad/jamad.github.io/assets/949913/396b55e8-7111-4e59-914a-69157e56adba)

```
import bpy
import math

START=0
END=100
N=5
bpy.context.scene.frame_start = START
bpy.context.scene.frame_end   = END

# Add a camera
bpy.ops.object.camera_add(
    location=(70, -40, 50),
    rotation=(1.1, 0, 0.8)
)

# Add color cubes
for x in range(0, N):
    for y in range(0, N):
        for z in range(0, N):
            # Add a color cube
            bpy.ops.mesh.primitive_cube_add( location=(x*3, y*3, z*3) )
           
            obj =bpy.context.view_layer.objects.active
           
            mat = bpy.data.materials.new('Cube')
            mat.use_nodes = True
           
            bsdf = mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (x/N, y/N, z/N,1) # color
            bsdf = mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.5 # alpha
            mat.blend_method = 'BLEND'

            obj.data.materials.append(mat)
           
            # Set the start key frame
            bpy.context.scene.frame_set(START)
            obj.keyframe_insert( data_path='rotation_euler' )
            obj.keyframe_insert( data_path='location' )
           
            # Set the end key frame
            bpy.context.scene.frame_set(END)
            obj.location = ( (N-x)*3, (N-y)*3, (N-z)*3 )
            obj.rotation_euler = (math.pi, math.pi, math.pi)
            obj.keyframe_insert( data_path='location' )
            obj.keyframe_insert( data_path='rotation_euler' )
```

# animation		
* example after the script for the selected object ![image](https://github.com/jamad/jamad.github.io/assets/949913/ee6ed791-bd66-4beb-b02b-c4fdd339e000)

```
import bpy

bpy.context.scene.frame_set(0)
obj =bpy.context.view_layer.objects.active   
obj.keyframe_insert(data_path='location')
bpy.context.scene.frame_set(20)
obj.location.z += 1
obj.keyframe_insert(data_path='location')
old_type = bpy.context.area.type
bpy.context.area.type = 'GRAPH_EDITOR'
bpy.ops.graph.interpolation_type(type='LINEAR')
bpy.context.area.type = old_type
bpy.context.scene.frame_end = 20
```

### trajectory
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/3c570c40-592e-45fb-8f97-7197b0805b4f) ![image](https://github.com/jamad/jamad.github.io/assets/949913/73029f6d-f891-45b3-82f1-b1582152433a) ![image](https://github.com/jamad/jamad.github.io/assets/949913/7c94287f-626c-459e-abb8-e5fe5c8837e0)


* example - https://github.com/jamad/blender_jamad/blob/master/animation_trajectory.py
* example - https://github.com/jamad/blender_jamad/blob/master/animation_trajectory.blend

# light and camera
* example after script ![image](https://github.com/jamad/jamad.github.io/assets/949913/b5766a5c-a858-4de2-80fb-55effa382515)

```
import bpy
import math

# create a light
bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(0, 0, 0))

# create a camera
bpy.ops.object.camera_add()

# create a plane
bpy.ops.mesh.primitive_plane_add(    location=( 1, 2, 3 ),    rotation=( math.pi/3, math.pi/4, math.pi/5 ),   )
```


# 逆引き
* タイムラインを　frame 0 に移動 [ref](https://blender.stackexchange.com/questions/14809/location-of-an-object-at-a-specific-frame)
  * bpy.context.scene.frame_set(0)	
* 'target'という名前のオブジェクトを変数に登録し、位置と回転をゲット　[ref](https://blender.stackexchange.com/questions/39677/how-do-you-get-an-objects-position-and-rotation-through-script)
  * targetOBJ=bpy.data.objects["target"]
  * pX,pY,pZ=targetOBJ.matrix_world.to_translation()
  * rX,rY,rZ=targetOBJ.matrix_world.to_euler('XYZ')	



