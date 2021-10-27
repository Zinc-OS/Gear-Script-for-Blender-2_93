import bpy
import bmesh
import os
from math import *
from bpy_extras.object_utils import AddObjectHelper
version="0.01"
import bpy.utils.previews
from bpy.props import *
def float2str(float,precision=2):
    if precision==0:
        return str(round(float))
    return str(round(float*10**precision)/10**precision)
bl_info = {
    "name": "Gear Script",
    "description": "Script that makes gears and aoutomatically assigns drivers based on gear radius and number of teeth. Right click on a gear to add a driven gear. Include helical gears.",
    "author": "Louis Sarwal",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Add > Mesh",
    "warning": "Still in development", # used for warning icon and text in addons panel
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "support": "COMMUNITY",
    "category": "Add Mesh",
}
    
def add_gear(radius,
            teeth,
            addendum,
            dedendum,
            pressure_angle,
            height,
            rows,
            twist,
            hub_height,
            hub_offset,
            hub_radius,
            axle_radius,
            axle_height,
            axle_angle):
    verts = [
        [0,0,0]
    ]
    faces=[]
    a_r=radius*teeth+addendum
    o_r=radius*teeth
    i_r=radius*teeth-dedendum
    teeth=teeth
    pressure=pressure_angle*pi/180
    num=-1
    x=0
    y=0
    z=0
    r=0
    while r<teeth:
        #tooth
        angle=(r/teeth)*2*pi
        num+=1
        verts[num][2]=0
        verts[num][1]=sin(angle-(pi/2)/teeth)*i_r
        verts[num][0]=cos(angle-(pi/2)/teeth)*i_r
        
        ############################################
        diff=(pi/2)*i_r/o_r
        verts.append([0,0,0])
        num+=1
        verts[num][2]=0
        verts[num][1]=sin(angle-diff/teeth)*o_r
        verts[num][0]=cos(angle-diff/teeth)*o_r
        #addendum#################################
        a_diff=((pi/2)-pressure)*i_r/a_r
        verts.append([0,0,0])
        num+=1
        verts[num][2]=0
        verts[num][1]=sin(angle-a_diff/teeth)*a_r
        verts[num][0]=cos(angle-a_diff/teeth)*a_r
        
        
        verts.append([0,0,0])
        num+=1
        verts[num][2]=0
        verts[num][1]=sin(angle+a_diff/teeth)*a_r
        verts[num][0]=cos(angle+a_diff/teeth)*a_r
        
        ###########################################
        verts.append([0,0,0])
        num+=1
        verts[num][2]=0
        verts[num][1]=sin(angle+diff/teeth)*o_r
        verts[num][0]=cos(angle+diff/teeth)*o_r
        ############################################
        
        verts.append([0,0,0])
        num+=1
        verts[num][2]=0
        verts[num][1]=sin(angle+(pi/2)/teeth)*i_r
        verts[num][0]=cos(angle+(pi/2)/teeth)*i_r
       
        
        r+=1
        if r<teeth:
            verts.append([0,0,0])
        else:
            verts.append([0,0,0])
            num+=1
            verts[num][2]=0
            verts[num][1]=sin(0-(pi/2)/teeth)*i_r
            verts[num][0]=cos(0-(pi/2)/teeth)*i_r
    xnum=len(verts)
    r=0
    n=0
    vnum=0
    r=len(verts)-2
    while r>=0:
        faces.append([])
        f=r-5
        while r>=f:
            faces[-1].append(r)
            r-=1
            #if r<0:
                #break
        #r-=1
    
   
    
        
    
    
    rows=abs(round(rows*((height*twist))))#twist can be negative, and is actually flipped with new gears
    if rows<1:
        rows=1
    rot=((twist*pi/180)/rows)*(height/(radius*teeth))
    while n<rows:
        
        tmp=len(verts)
        r=vnum
        while r<tmp:
            verts.append([cos(rot)*verts[r][0]+sin(rot)*verts[r][1],cos(rot+pi/2)*verts[r][0]+sin(rot+pi/2)*verts[r][1],((n+1)/rows)*height])
            num+=1
            r+=1
        b=vnum
        ####print(b,r,len(verts))
        while b+xnum+1<len(verts):
            faces.append([b+1,b+xnum+1,b+xnum,b])
            b+=1
        n+=1
        vnum=tmp
    r=vnum
    #if r<len(verts):
    #   faces.append([])
    #while r<len(verts):
    #    faces[-1].append(r)
    #    r+=5
    #    if r<len(verts):
    #        faces[-1].append(r)
    #    r+=1
    r=vnum
    while r<len(verts):
        faces.append([])
        f=r+6
        while r<f:
            if r<len(verts):
                faces[-1].append(r)
            r+=1
    faces[-1].append(vnum+1)
    faces[-1].append(vnum)
    #############################
    verts.append([0,0,0])
    #hub_height=10
    r=0
    TMP=len(verts)
    unum=len(verts)
    while r<teeth:
        angle=(r/teeth)*2*pi
        num+=1
        verts[num][2]=-hub_height*radius-hub_offset*hub_height*radius
        verts[num][1]=sin(angle-(pi/2)/teeth)*i_r*hub_radius
        verts[num][0]=cos(angle-(pi/2)/teeth)*i_r*hub_radius
        
        verts.append([0,0,0])
        num+=1
        verts[num][2]=-hub_height*radius-hub_offset*hub_height*radius
        verts[num][1]=sin(angle+(pi/2)/teeth)*i_r*hub_radius
        verts[num][0]=cos(angle+(pi/2)/teeth)*i_r*hub_radius
       
        
        r+=1
        if r<teeth:
            verts.append([0,0,0])
        else:
            verts.append([0,0,0])
            num+=1
            verts[num][2]=0
            verts[num][1]=sin(0-(pi/2)/teeth)*i_r
            verts[num][0]=cos(0-(pi/2)/teeth)*i_r
    #add hub face
    r=len(verts)-2
    if r>=TMP-1:
        faces.append([])
    while r>=TMP-1:
        faces[-1].append(r)
        r-=1
    r=xnum-7
    b=len(verts)-3
    #add hub
    while r>0:
        faces.append([])
        faces[-1].append(r)
        r-=1
        faces[-1].append(r)
        faces[-1].append(b-1)
        faces[-1].append(b)
        b-=1
        faces.append([])
        faces[-1].append(r)
        r-=5
        faces[-1].append(r)
        faces[-1].append(b-1)
        faces[-1].append(b)
        b-=1
    faces.append([len(verts)-3,len(verts)-2,xnum-2,xnum-7])   
    faces.append([len(verts)-2,b,xnum-1,xnum-2])  
    
    #bottom hub
    r=0
    
    rot=(twist*pi/180)*(height/(radius*teeth))
    u=vnum
    #=len(verts)
    #faces.append([])
    tmp=len(verts)
    while u<TMP-2:
        verts.append([
            verts[u][0]*hub_radius,
            verts[u][1]*hub_radius,
            hub_height*radius+height-hub_offset*hub_height*radius
        ])
        u+=5
        verts.append([
            verts[u][0]*hub_radius,
            verts[u][1]*hub_radius,
            hub_height*radius+height-hub_offset*hub_height*radius
        ])
        u+=1
        #add hub face
        #faces[-1].append(len(verts)-2)
        #faces[-1].append(len(verts)-1)
    r=tmp
    u=vnum#-(len(verts)-2-TMP)
    while r<len(verts)-2:
        faces.append([])
        faces[-1].append(r+1)
        faces[-1].append(r)
        r+=1
        faces[-1].append(u)
        u+=5
        faces[-1].append(u)
        
        
        faces.append([])
        faces[-1].append(r+1)
        faces[-1].append(r)
        r+=1
        faces[-1].append(u)
        u+=1
        faces[-1].append(u)
    faces.append([r,u,u+5,r+1])  
    faces.append([vnum,tmp,r+1,u+5])
    
    ##########################################################
    #axle
    r=0
    
    rot=(twist*pi/180)*(height/(radius*teeth))
    #=len(verts)
    #faces.append([])
    u=tmp
    tm=len(verts)
    while u<tm:
        verts.append([
            verts[u][0]*axle_radius/(teeth*hub_radius),
            verts[u][1]*axle_radius/(teeth*hub_radius),
            hub_height*radius+height-hub_offset*hub_height*radius
        ])
        u+=1
        #faces[-1].append(len(verts)-1)
    r=tm
    u=tmp#-(len(verts)-2-TMP)
    while r<len(verts)-2:
        faces.append([])
        faces[-1].append(r+1)
        faces[-1].append(r)
        r+=1
        faces[-1].append(u)
        u+=1
        faces[-1].append(u)
        
        
        faces.append([])
        faces[-1].append(r+1)
        faces[-1].append(r)
        r+=1
        faces[-1].append(u)
        u+=1
        faces[-1].append(u)
    faces.append([r,u,u+1,r+1])  
    faces.append([tmp,tm,r+1,u+1])
    tmp=tm
    ####print(faces)
    ##########################################################
    #axle
    r=0
    
    rot=(twist*pi/180)*(height/(radius*teeth))
    #=len(verts)
    faces.append([])
    u=tmp
    tm=len(verts)
    while u<tm:
        verts.append([
            verts[u][0]*(1-axle_angle),
            verts[u][1]*(1-axle_angle),
            hub_height*radius+height-hub_offset*hub_height*radius+axle_height
        ])
        u+=1
        faces[-1].append(len(verts)-1)
    r=tm
    u=tmp#-(len(verts)-2-TMP)
    while r<len(verts)-2:
        faces.append([])
        faces[-1].append(r+1)
        faces[-1].append(r)
        r+=1
        faces[-1].append(u)
        u+=1
        faces[-1].append(u)
        
        
        faces.append([])
        faces[-1].append(r+1)
        faces[-1].append(r)
        r+=1
        faces[-1].append(u)
        u+=1
        faces[-1].append(u)
    faces.append([r,u,u+1,r+1])  
    faces.append([tmp,tm,r+1,u+1])
    ####print(faces)
    return verts, faces


class AddGear(bpy.types.Operator, AddObjectHelper):
    """Add a simple gear mesh"""
    bl_idname = "mesh.primitive_gear_add"
    bl_label = "Add Gear"
    bl_options = {'REGISTER', 'UNDO'}
    #radius,
    #teeth,
    #addendum,
    #dedendum,
    #pressure_angle
    teeth: IntProperty(
        name="Teeth",
        description="Number of gear teeth",
        min=1,
        max=2000,
        default=12,
        #unit='LENGTH'
    )
    radius: FloatProperty(
        name="Radius X",
        description="Gear Radius Multiple",
        min=0.01,
        default=0.25,
        step=1,
        #unit='RADIANS',
    )
    addendum: FloatProperty(
        name="Addendum",
        description="Gear Adendum",
        min=0.01, 
        default=0.5,
    )
    dedendum: FloatProperty(
        name="Dedendum",
        description="Gear Dedendum",
        min=0.01,
        default=0.5,
    )
    pressure_angle: FloatProperty(
        name="Pressure Angle",
        description="Pressure Angle",
        min=0, max=360,
        default=45,
    )
    height: FloatProperty(
        name="Height",
        description="Gear Height",
        min=0.01, 
        default=1.0,
    )
    around_gear_rot: FloatProperty(
        name="Rotation",
        description="Rotation",
        default=180.0,
        step=20,
    )
    rows: FloatProperty(
        name="Row Resolution",
        description="How many rows given the amount of twist, height, radius, and teeth. 0 is none.",
        min=0.0, 
        default=0.01,
        step=5,
    )
    twist: FloatProperty(
        name="Twist",
        description="How many degrees the gear is spun",
        default=0.0,
    )
    hub_height: FloatProperty(
        name="Height",
        description="Height of Hub",
        default=0.0
    )
    hub_offset: FloatProperty(
        name="Offset",
        description="Offset of Hub",
        min=-1,
        max=1,
        default=0,
    )
    Pos: IntProperty(
        name="Postion",
        description="Position of gear. -1 is bottom. 0 is side. 1 is top",
        min=-1,
        max=1,
        default=0,
    )
    hub_radius: FloatProperty(
        name="Radius",
        description="Radius of Hub",
        min=0,
        max=1,
        default=1,
    )
    edit_gear: BoolProperty(
        name="edit",
        default=False,
    )
    init=0
    axle_radius:FloatProperty(
        name="Radius",
        description="Axle Radius",
        min=0,
        default=0
    )
    axle_height:FloatProperty(
        name="Height",
        description="Axle Height",
        default=0
    )
    axle_angle:FloatProperty(
        name="Pointiness",
        description="Axle Angle",
        default=0,
        min=0,
        max=1
    )
    old_keys=None#copy old keys
    def draw(self, context):
        layout = self.layout
        row = layout.box()
        end=row
        row.prop(self, 'teeth')
        row.prop(self, 'radius')
        row.prop(self, 'height')
        row.prop(self, 'dedendum')
        row.prop(self, 'addendum')
        row.prop(self, 'twist')
        row.prop(self, 'rows')
        row.prop(self, 'pressure_angle')
        row.prop(self, 'around_gear_rot')
        row.prop(self,"Pos")
        row=row.box()
        row.label(text="Axle")
        row.prop(self,'axle_radius')
        row.prop(self,'axle_height')
        row.prop(self,'axle_angle',slider=True)
        row=end
        row=row.box()
        row.label(text="Hub")
        row.prop(self, 'hub_height')
        row.prop(self, 'hub_offset',slider=True)
        row.prop(self, 'hub_radius',slider=True)
    def execute(self, context):
        s_obj=context.object
        if s_obj:
             if 'gear' in s_obj.data.keys():
                if not self.init>0:
                    self.radius=s_obj.data['radius']
                    self.teeth=s_obj.data['teeth']
                    self.addendum=s_obj.data['addendum']
                    self.dedendum=s_obj.data['dedendum']
                    self.pressure_angle=s_obj.data['pressure_angle']
                    self.rows=s_obj.data['rows']
                    if self.edit_gear:
                        self.twist=s_obj.data['twist']
                    else:
                        self.twist=s_obj.data['twist']*-1#so they mesh
                    self.init=True
                    self.hub_height=s_obj.data['hub_height']
                    self.hub_offset=s_obj.data['hub_offset']
                    self.hub_radius=s_obj.data['hub_radius']
                    self.axle_radius=s_obj.data['axle_radius']
                    self.height=s_obj.data['height']
                    if self.edit_gear:
                        self.Pos=s_obj.data['Pos']
                    if self.Pos==1 or self.Pos==-1 and not self.edit_gear:
                        self.around_gear_rot=s_obj.data['rot']+180
                    elif self.edit_gear:
                        self.around_gear_rot=s_obj.data['rot']
                    self.init=1
                    self.axle_angle=s_obj.data['axle_angle']
        verts_loc, faces = add_gear(
            self.radius,
            self.teeth,
            self.addendum,
            self.dedendum,
            self.pressure_angle,
            self.height,
            self.rows,
            self.twist,
            self.hub_height,
            self.hub_offset,
            self.hub_radius,
            self.axle_radius,
            self.axle_height,
            self.axle_angle
        )
        
       
        mesh = bpy.data.meshes.new('gear')
        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.new(v_co)

        bm.verts.ensure_lookup_table()
        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])
        
        bm.to_mesh(mesh)
        mesh.update()
            
        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        if self.edit_gear:
            o=context.object
            name=o.data.name
            n=o.data
            o.data=mesh
            o.data.name=name
            bpy.data.meshes.remove(n)
            
            ###print('PARENT',o.gear_parent)
            if o.gear_parent!='':
                s_obj=bpy.data.objects[o.gear_parent]
            ###print('S',s_obj)
            ###print('O',o)
        elif s_obj and 'gear' in s_obj.data.keys():# and not self.init>1:
            bpy.ops.object.duplicate({'object':s_obj})
            o=context.object#returned by duplicate. This is used to copy all modifiers(AND PHYSICS SETTINGS ;;;;;))))))
            #self.init=2
            #print(o.data)
            self.old_keys={}
            for key in o.data.keys():
                #print('key')
                if key not in props:
                    #print(key,o.data[key])
                    self.old_keys[key]=o.data[key]#copy all data keys except for the ones we set
            name=o.data.name
            n=o.data
            o.data=mesh
            o.data.name=name
            o.gear_children.clear()
            o.gear_parent=''
            bpy.data.meshes.remove(n)
            for key in self.old_keys:
                if key not in props:
                    o.data[key]=self.old_keys[key]#paste all data keys except for the ones we set
            o.keyframe_insert("rotation_euler")
            o.keyframe_insert("location")
            o.keyframe_delete("rotation_euler")
            o.keyframe_delete("location")
            o.driver_add("rotation_euler")
            o.driver_add("location")
            o.driver_remove("rotation_euler")
            o.driver_remove("location")
        else:
            #print("object compare check")
            #print(s_obj)
            #print(context.view_layer.objects.active)
            o=object_utils.object_data_add(context, mesh, operator=self)
            if self.old_keys:
                for key in self.old_keys:
                    if key not in props:
                        o.data[key]=self.old_keys[key]#paste all data keys except for the ones we set

        
        o.name=o.data.name+"|"+str(self.teeth)+'x'+float2str(self.radius,1)+'|'+float2str(self.addendum,1)+'-'+float2str(self.dedendum,1)+'|'+float2str(self.twist,1)+'deg|'+float2str(self.height,0)+'m'
        o.data['gear']=True
        o.data['radius']=self.radius
        o.data['teeth']=self.teeth
        o.data['addendum']=self.addendum
        o.data['dedendum']=self.dedendum
        o.data['pressure_angle']=self.pressure_angle
        o.data['lower']=self.hub_height*self.radius+self.hub_offset*self.hub_height*self.radius
        o.data['upper']=self.hub_height*self.radius+self.height-self.hub_offset*self.hub_height*self.radius
        o.data['rows']=self.rows
        o.data['twist']=self.twist
        o.data['rot']=self.around_gear_rot
        o.data['hub_offset']=self.hub_offset
        o.data['hub_height']=self.hub_height
        o.data['hub_radius']=self.hub_radius
        o.data['height']=self.height
        o.data['Pos']=self.Pos
        o.data['rot']=self.around_gear_rot
        o.data['axle_radius']=self.axle_radius
        o.data['axle_angle']=self.axle_angle
        o.rotation_mode='ZYX'
        r=self.around_gear_rot*pi/180
        c_child=0
        while c_child<len(o.gear_children):
            if o.gear_children[c_child].name not in bpy.data.objects:
                o.gear_children.remove(c_child)#if the name is changed, then the name will definitely be in the parent and child strings. But the old names haven't een deleted and will throw errors
            else:
                bpy.data.objects[o.gear_children[c_child].name].gear_parent=o.name
                self.updateGear(o.gear_children[c_child].name)
                c_child+=1
        if s_obj:
             if 'gear' in s_obj.data.keys():
                if s_obj!=o:
                    o.gear_parent=s_obj.name
                    #o.parent=s_obj
                    ###print("name",s_obj.name)
                    ###print("parent",o.gear_parent)
                    o.data['Pos']=self.Pos
                    if o.name not in s_obj.gear_children:
                        child=s_obj.gear_children.add()
                        child.name=o.name
                    self.updateGear(o.name)
        return {'FINISHED'}
    # seperate to allow for easy recursive coding ;)
    def updateGear(self,gear):
        o=bpy.data.objects[gear]
        o.rotation_mode='ZYX'
        s_obj=bpy.data.objects[o.gear_parent]
        r=o.data['rot']*pi/180
        o.keyframe_insert("rotation_euler")#the keyframe may not be set. In order to delete it we must add it. In order to get out of the hole one must first pick up the shovel to dig it if it isn't there, then climb in. Only then can you be sure of getting out.
        o.keyframe_delete("rotation_euler")#delete any keyframes in the rotations. These will interfere with drivers
        if o.data['Pos']==0:
            ###print(s_obj)
            ###print(o)
            if o.gear_parent!='':
                o.rotation_euler.x=0
                o.rotation_euler.y=0
                o.location.z=0#s_obj.location.z
            #x="("+str(s_obj.data['radius']*s_obj.data['teeth']+o.data['radius']*o.data['teeth']+(s_obj.data['addendum']+o.data['addendum'])/2-s_obj.data['dedendum'])+")*cos("+str(o.data['rot'])+"*3.1415/180)"
            #y="("+str(s_obj.data['radius']*s_obj.data['teeth']+o.data['radius']*o.data['teeth']+(s_obj.data['addendum']+o.data['addendum'])/2-s_obj.data['dedendum'])+")*sin("+str(o.data['rot'])+"*3.1415/180)"
            #o.rotation_euler=(0.0,0.0,2*pi/o.data['teeth']+(o.data['teeth']%2+1)*pi/o.data['teeth']+self.around_gear_rot*pi/180+(self.around_gear_rot*pi/180)*(s_obj.data['teeth']/o.data['teeth']))
            o.location.x=s_obj.location.x+(s_obj.data['radius']*s_obj.data['teeth']+o.data['radius']*o.data['teeth']+(s_obj.data['addendum']+o.data['addendum'])/2-s_obj.data['dedendum'])*cos(o.data['rot']*pi/180)
            o.location.y=s_obj.location.y+(s_obj.data['radius']*s_obj.data['teeth']+o.data['radius']*o.data['teeth']+(s_obj.data['addendum']+o.data['addendum'])/2-s_obj.data['dedendum'])*sin(o.data['rot']*pi/180)
            o.location.z=s_obj.location.z
            driver=o.driver_add("rotation_euler",2)
            if len(driver.driver.variables)>0:
                driver.driver.variables.remove(driver.driver.variables[0])
            var=driver.driver.variables.new()
            var.type='TRANSFORMS'
            var.targets[0].transform_type='ROT_Z'
            var.targets[0].rotation_mode='XYZ'
            #var.targets[0].transform_space='TRANSFORM_SPACE'
            var.targets[0].id=s_obj
            
            driver.driver.expression='-('+str(s_obj.data['teeth'])+'/'+str(o.data['teeth'])+')*var+'+str(2*pi/o.data['teeth']+(o.data['teeth']%2+1)*pi/o.data['teeth']+r)+"+"+str(r)+'*('+str(s_obj.data['teeth'])+'/'+str(o.data['teeth'])+')'
            
            #driver=o.driver_add("location",0)
            #if len(driver.driver.variables)>0:
            #    driver.driver.variables.remove(driver.driver.variables[0])
            #var=driver.driver.variables.new()
            #var.type='TRANSFORMS'
            #var.targets[0].transform_type='ROT_Z'
            #var.targets[0].rotation_mode='ZYX'
            #var.targets[0].transform_space='TRANSFORM_SPACE'
            #var.targets[0].id=s_obj
            #driver.driver.expression='cos(var)*'+x+'+sin(var)*'+y
            
            #driver=o.driver_add("location",1)
            #if len(driver.driver.variables)>0:
            #    driver.driver.variables.remove(driver.driver.variables[0])
            #var=driver.driver.variables.new()
            #var.type='TRANSFORMS'
            #var.targets[0].transform_type='ROT_Z'
            #var.targets[0].rotation_mode='ZYX'
            #var.targets[0].transform_space='TRANSFORM_SPACE'
            #var.targets[0].id=s_obj
            #driver.driver.expression='cos(var+'+str(pi/2)+')*'+x+'+sin(var+'+str(pi/2)+')*'+y
        elif o.data['Pos'] == 1:
            o.rotation_euler.x=0
            o.rotation_euler.y=0
            o.location.x=s_obj.location.x
            o.location.y=s_obj.location.y
            o.rotation_euler=(0,0,0)
            o.location.z=s_obj.location.z+s_obj.data['upper']+o.data['lower']
            #o.rotation_euler=(0.0,0.0,2*pi/o.data['teeth']+(o.data['teeth']%2+1)*pi/o.data['teeth']+self.around_gear_rot*pi/180+(self.around_gear_rot*pi/180)*(s_obj.data['teeth']/o.data['teeth']))
            driver=o.driver_add("rotation_euler",2)
            var=driver.driver.variables.new()
            var.type='TRANSFORMS'
            var.targets[0].transform_type='ROT_Z'
            var.targets[0].rotation_mode='XYZ'
            ##var.targets[0].transform_space='TRANSFORM_SPACE'
            var.targets[0].id=s_obj
            driver.driver.expression="var"
        else:
            o.rotation_euler.x=0
            o.rotation_euler.y=0
            o.location.x=s_obj.location.x
            o.location.y=s_obj.location.y
            o.location.z=s_obj.location.z-s_obj.data['lower']-o.data['upper']
            ##o.rotation_euler=(0.0,0.0,2*pi/o.data['teeth']+(o.data['teeth']%2+1)*pi/o.data['teeth']+self.around_gear_rot*pi/180+(self.around_gear_rot*pi/180)*(s_obj.data['teeth']/o.data['teeth']))
            driver=o.driver_add("rotation_euler",2)
            var=driver.driver.variables.new()
            var.type='TRANSFORMS'
            var.targets[0].transform_type='ROT_Z'
            var.targets[0].transform_space='TRANSFORM_SPACE'
            var.targets[0].rotation_mode='XYZ'
            #var.targets[0].id=s_obj
            driver.driver.expression="var"
        c_child=0
        while c_child<len(o.gear_children):
            if o.gear_children[c_child].name not in bpy.data.objects:
                o.gear_children.remove(c_child)
            else:
                bpy.data.objects[o.gear_children[c_child].name].gear_parent=o.name
                self.updateGear(o.gear_children[c_child].name)
                c_child+=1
class addGearChain(bpy.types.Operator, AddObjectHelper):
    """Edit a simple gear mesh"""
    bl_idname = "mesh.primitive_add_gear_chain"
    bl_label = "Edit Gear"
    bl_options = {'REGISTER', 'UNDO'}
    numGears:IntProperty(
        name="Pairs",
        description="How many gears in the chain.",
        default=1,
        soft_min=2
    )
    ratio:IntProperty(
        name="Ratio",
        description="Ratio of first gear to last gear",
        default=60,
        soft_min=1,
    )
    radius: FloatProperty(
        name="Radius X",
        description="Gear Radius Multiple",
        min=0.01,
        default=0.25,
        step=1,
        #unit='RADIANS',
    )
    addendum: FloatProperty(
        name="Addendum",
        description="Gear Adendum",
        min=0.01, 
        default=0.5,
    )
    dedendum: FloatProperty(
        name="Dedendum",
        description="Gear Dedendum",
        min=0.01,
        default=0.5,
    )
    pressure_angle: FloatProperty(
        name="Pressure Angle",
        description="Pressure Angle",
        min=0, max=360,
        default=45,
    )
    height: FloatProperty(
        name="Height",
        description="Base Gear Height",
        min=0.01, 
        default=1.0,
    )
    rows: FloatProperty(
        name="Row Resolution",
        description="How many rows given the amount of twist, height, radius, and teeth. 0 is none.",
        min=0.0, 
        default=0.01,
        step=5,
    )
    twist: FloatProperty(
        name="Twist",
        description="How many degrees the gear is spun",
        default=0.0,
    )
    hub_height: FloatProperty(
        name="Height",
        description="Height of Hub",
        default=0.0
    )
    hub_offset: FloatProperty(
        name="Offset",
        description="Offset of Hub",
        min=-1,
        max=1,
        default=0,
    )
    Pos: IntProperty(
        name="Postion",
        description="Position of gear. -1 is bottom. 0 is side. 1 is top",
        min=-1,
        max=1,
        default=0,
    )
    hub_radius: FloatProperty(
        name="Radius",
        description="Radius of Hub",
        min=0,
        max=1,
        default=1,
    )
    def execute(self,c):
        f=self.numGears
        rot=0
        ratio=60
        mod=self.ratio%self.numGears
        x=int(self.ratio/self.numGears)
        i=6
        j=x*6
        while f>0:
            bpy.ops.mesh.primitive_gear_add(
                teeth=i,
                radius=self.radius,
                height=self.height,
                Pos=1,
                around_gear_rot=rot,
                addendum=self.addendum,
                dedendum=self.dedendum,
                init=1,
            )
            bpy.ops.mesh.primitive_gear_add(
                teeth=j,
                radius=self.radius,
                height=self.height,
                Pos=0,
                around_gear_rot=rot,
                addendum=self.addendum,
                dedendum=self.dedendum,
                init=1
                
            )
            rot+=30
            f-=1
            if f==1:
                j+=mod
        return {'FINISHED'}
props=[
    'gear',#True
    'radius',#self.radius
    'teeth',#self.teeth
    'addendum',#self.addendum
    'dedendum',#self.dedendum
    'pressure_angle',#self.pressure_angle
    'lower',#self.hub_height*#self.radius+#self.hub_offset*#self.hub_height*#self.radius
    'upper',#self.hub_height*#self.radius+#self.height-#self.hub_offset*#self.hub_height*#self.radius
    'rows',#self.rows
    'twist',#self.twist
    'rot',#self.around_gear_rot
    'hub_offset',#self.hub_offset
    'hub_height',#self.hub_height
    'hub_radius',#self.hub_radius
    'height',#self.height
    'Pos',#self.Pos 
]
#too slow
'''class gearPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Gear Properties"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout.box()

        obj = context.object
        ####print(obj.data['gear'])
        if obj.data['gear']:
            active=False
            row = layout.row()
            row.label(text="Gear", icon='WORLD_DATA')
            row = layout.row()
            row.label(text="Gear: " + obj.name)
            row = layout.row()
            row.prop(obj, "name")
            ###print(active) 
            row = layout.box()
            row.prop(obj,"teeth")
            if row.active:
                active=True
            ###print(active)  
            row = layout.box()
            row.prop(obj,"radius")
            if row.active:
                active=True
                
            row = layout.box()
            row.prop(obj,"addendum")
            if row.active:
                active=True
                
            row = layout.box()
            row.prop(obj,"dedendum")
            if row.active:
                active=True
                
            row = layout.row()
            row.prop(obj,"pressure_angle")
            if row.active:
                active=True
                
            row = layout.box()
            row.prop(obj,"height")
            if row.active:
                active=True
                
            row = layout.box()
            row.prop(obj,"rows")
            if row.active:
                active=True
                
            row = layout.box()
            row.prop(obj,"twist")
            if row.active:
                active=True
                
            row = layout.box()
            row.operator("mesh.primitive_gear_add")
            if active:
                verts_loc, faces = add_gear(
                    obj.radius,
                    obj.teeth,
                    obj.addendum,
                    obj.dedendum,
                    obj.pressure_angle,
                    obj.height,
                    obj.rows,
                    obj.twist
                )
                bm = bmesh.new()

                for v_co in verts_loc:
                    bm.verts.new(v_co)

                bm.verts.ensure_lookup_table()
                for f_idx in faces:
                    bm.faces.new([bm.verts[i] for i in f_idx])
                mesh=bpy.context.object.data
                bm.to_mesh(mesh)
                mesh.update()
            
''' '''     
class MultiGearEdit(bpy.types.Operator, AddObjectHelper):
    """Edit a simple gear mesh"""
    bl_idname = "mesh.primitive_gear_edit_multiple"
    bl_label = "Edit Gear"
    bl_options = {'REGISTER', 'UNDO'}
    dc={
        "teeth":[],#:o.data['teeth',
        "radius":[],#radius[i],,#:o.data['radius'],,
        "addendum":[],#addendum[i],,#:o.data['addendum'],,
        "dedendum":[],#dedendum[i],,#:o.data['dedendum'],,
        "presssure_angle":[],#pressure_angle[i],,#:o.data['pressure_angle'],,
        "rows":[],#rows[i],,#:o.data['rows'],,
        "twist":[],#twist[i],,#:o.data['twist'],,        "    
        "hub_height":[],#hub_height[i],,#:o.data['hub_height'],,
        "hub_offset":[],#hub_offset[i],,#:o.data['hub_offset'],,
        "hub_radius":[],#hub_radius[i],,#:o.data['hub_radius'],,
        "height":[],#height[i],,#:o.data['height'],,
        "Pos":[],#Pos[i],,#:o.data['Pos'],,
        "around_gear_rot":[]#p_around_gear_rot[i],,#:o.data['rot'],,
    }
    p={  
        "teeth":[],#:o.data['teeth'],,
        "radius":[],#radius[i],,#:o.data['radius'],,
        "addendum":[],#addendum[i],,#:o.data['addendum'],,
        "dedendum":[],#dedendum[i],,#:o.data['dedendum'],,
        "presssure_angle":[],#pressure_angle[i],,#:o.data['pressure_angle'],,
        "rows":[],#rows[i],,#:o.data['rows'],,
        "twist":[],#twist[i],,#:o.data['twist'],,        "    
        "hub_height":[],#hub_height[i],,#:o.data['hub_height'],,
        "hub_offset":[],#hub_offset[i],,#:o.data['hub_offset'],,
        "hub_radius":[],#hub_radius[i],,#:o.data['hub_radius'],,
        "height":[],#height[i],,#:o.data['height'],,
        "Pos":[],#Pos[i],,#:o.data['Pos'],,
        "around_gear_rot":[]#p_around_gear_rot[i],,#=o.data['rot'],
    }
    init=False
    def execute(self,c):
        i=0
        edit_gear=True,
        init=False
        if not self.init:
            i=0
            for o in c.selected_objects:
                for d in self.dc:
                    if o.data[d] not in self.dc[d]:  
                        self.dc[d].append(o.data[c])
                        self.p[d].append(len(self.teeth)-1)
                    else:
                        r=0
                        while r<len(self.teeth):
                            if o.data[d]==dc[d][r]:
                                self.p[d].append(r)
                            r+=1
                i++1
        print(self.dc)
        for o in c.selected_objects:
            
            print(bpy.ops.mesh.primitive_gear_add(
                {'object':o,'selected_objects':[o],'active_object':o},
                edit_gear=True,
                teeth=self.d['teeth'][self.p['teeth']],#teeth[i],self.d[''][self.p['']],#=o.data['teeth'],
                radius=self.d['radius'][self.p['']],#radius[i],self.d[''][self.p['']],#=o.data['radius'],
                addendum=self.d['addendum'][self.p['addendum']],#addendum[i],self.d[''][self.p['']],#=o.data['addendum'],
                dedendum=self.d['dedendum'][self.p['dedendum']],#dedendum[i],self.d[''][self.p['']],#=o.data['dedendum'],
                presssure_angle=self.d['pressure_angle'][self.p['pressure_angle']],#pressure_angle[i],self.d[''][self.p['']],#=o.data['pressure_angle'],
                rows=self.d['rows'][self.p['rows']],#rows[i],self.d[''][self.p['']],#=o.data['rows'],
                twist=self.d['twist'][self.p['twist']],#twist[i],self.d[''][self.p['']],#=o.data['twist'],            
                hub_height=self.d['hub_height'][self.p['hub_height']],#hub_height[i],self.d[''][self.p['']],#=o.data['hub_height'],
                hub_offset=self.d['hub_offset'][self.p['hub_offset']],#hub_offset[i],self.d[''][self.p['']],#=o.data['hub_offset'],
                hub_radius=self.d['hub_radius'][self.p['hub_radius']],#hub_radius[i],self.d[''][self.p['']],#=o.data['hub_radius'],
                height=self.d['height'][self.p['height']],#height[i],self.d[''][self.p['']],#=o.data['height'],
                Pos=self.d['Pos'][self.p['Pos']],#Pos[i],self.d[''][self.p['']],#=o.data['Pos'],
                around_gear_rot=self.d['around_gear_rot'][self.p['around_gear_rot']],#around_gear_rot[i],#=o.data['rot'],
                init=2
            ))
            i+=1
        self.init=True
        return {'FINISHED'}
    def draw(self,c):
        l=self.layout
        
 '''       
class VIEW3D_MT_add_mesh_lwswl_gear(bpy.types.Menu):
    # Define the "Gears" menu
    bl_idname = "VIEW3D_MT_add_mesh_lwswl_gear"
    bl_label = "Gears"

    def draw(self, context):
        o = self.layout.operator(AddGear.bl_idname, text="Top")
        o.Pos =1
        o.edit_gear =False
        ###print(icons['gears']['GEAR'])
        o = self.layout.operator(AddGear.bl_idname, text="Side")
        o.Pos =0
        o.edit_gear =False
        o = self.layout.operator(AddGear.bl_idname, text="Bottom")
        o.Pos =-1
        o.edit_gear =False
        o = self.layout.operator(AddGear.bl_idname, text="Edit")
        o.edit_gear =True
        #o = self.layout.operator(MultiGearEdit.bl_idname, text="Edit Multiple Gears")
        o = self.layout.operator(addGearChain.bl_idname, text="GearChain")
        
        
def menu_func(self, context):
    self.layout.operator(AddGear.bl_idname, icon='PREFERENCES').edit_gear =False
    o = self.layout.operator(addGearChain.bl_idname, text="GearChain")
    
def gear_context_menu(self, context):
    bl_label='add'
    if 'gear' in context.object.data.keys():
        layout=self.layout.row()
        layout.menu("VIEW3D_MT_add_mesh_lwswl_gear", icon='PREFERENCES',text="Gears")
        #self.layout.operator(AddGear.bl_idname, icon='PREFERENCES', text="Side")
        
class gearParent(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Object Name", default="")
def register():
    bpy.utils.register_class(gearParent)
    #bpy.utils.register_class(MultiGearEdit)
    bpy.utils.register_class(addGearChain)
    bpy.utils.register_class(AddGear)
    bpy.utils.register_class(VIEW3D_MT_add_mesh_lwswl_gear)
    bpy.types.Object.gear_parent=StringProperty(default='')
    bpy.types.Object.gear_children=CollectionProperty(type=gearParent)
    #bpy.utils.register_class(gearPanel)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(gear_context_menu)
    # Note that preview collections returned by bpy.utils.previews
    # are regular py objects - you can use them to store custom data.
    ico = bpy.utils.previews.new()
    # path to the folder where the icon is
    # the path is calculated relative to this py file inside the addon folder
    dir = os.path.join(os.path.dirname(__file__), "icons")
    dir='/run/media/lwswl/LWS_SWL/3d mesh objects/BLENDS/mech/add_mesh_gears'
    # load a preview thumbnail of a file and store in the previews collection
    ico.load("GEAR", os.path.join(dir, "gear.png"), 'IMAGE')
    icons["gears"] = ico
icons={}
def unregister():
    #bpy.utils.unregister_class(gearPanel)
    bpy.utils.unregister_class(AddGear)
    bpy.utils.unregister_class(gearParent)
    #bpy.utils.unregister_class(MultiGearEdit)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.remove(gear_context_menu)
    for icon in coll.values():
        bpy.utils.previews.remove(icon)
    

if __name__ == "__main__":
    #unregister()
    register()
    
    # test call
    #bpy.ops.mesh.primitive_gear_add()
