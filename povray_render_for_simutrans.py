import subprocess as sb

class render_povray():
    def __init__(self,infile,outfile,paksize,tilesize_x,tilesize_y,tilesize_z,winter,make_front=0):
        self.infile=infile
        self.outfile=outfile
        self.paksize=int(paksize)
        self.Nx=int(tilesize_x)
        self.Ny=int(tilesize_y)
        self.Nz=int(tilesize_z)
        self.winter=int(winter)
        self.make_front=int(make_front)
    def flag(self):
        def declare_povray(param,input_str):
            return "#declare "+str(param)+"="+str(input_str)+";\n"
        if self.paksize%4==0:
            # filesize define
            Width=self.paksize*(max(self.Nx,self.Ny))*4
            Height=self.paksize*(max(self.Nx,self.Ny,self.Nz//2))
            # make inc file which defines some values. 
            with open("temp.inc",mode="w") as f:
                f.write(declare_povray("int_x",self.Nx))
                f.write(declare_povray("int_y",self.Ny))
                f.write(declare_povray("int_z",max(self.Nz,1)))
                f.write(declare_povray("number_width",max(self.Nx,self.Ny)))
                f.write(declare_povray("number_hight",max(self.Nx,self.Ny,self.Nz//2)))
                f.write(declare_povray("winter",self.winter))
                f.write(declare_povray("make_front_image",self.make_front))
            # rendering
            outname=self.outfile[:-4]
            if outname=="":
                outname=self.infile[:-4]
            if self.winter==1:
                outname+="-winter"
            try:
                sb.run(["pvengine.exe","/EXIT","/RENDER",str(self.infile),"Width="+str(Width),"Height="+str(Height),"Antialias=Off","+O"+outname])
            except:
                try:
                    sb.run(["povray",str(self.infile),"Width="+str(Width),"Height="+str(Height),"Antialias=Off","+O"+outname])
                except:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

class povray_template():
    def __init__(self,outfile):
        self.outfile=outfile
    def write_snow(self):
        with open("snow.inc",mode="w") as f:
            f.write("#declare winter_light=\n")
            f.write("light_source {\n\t<0,173,0>\n\tcolor rgb 33\n\tparallel\n\tpoint_at<0,0,0>\n}\n")
        return
    def write_file(self,out):
        with open(out,mode="w") as f:
            f.write('#include "snow.inc"\n#include "temp.inc"\n')
            f.write('// ---add include files---\n\n\n')
            f.write('// -----------------------\n')
            f.write('// The default tile scale in this pov-ray file (not for pak file)\n')
            f.write('#local paksize=64;\n\n\n')
            f.write('// ---camera setting---\n')
            f.write('camera {\n\torthographic\n\tlocation <100,81.64965809277,100>*number_hight*paksize/128\n\tlook_at <0,0.425,0>*paksize/128\n\tright<1,0,-1> *paksize*number_width*2\n\tup<1,0,1>  *paksize*number_hight/2\n\t}\n\n\n')
            f.write('// ---light setting---\n')
            f.write('light_source {\n\t<0,173,100>\n\tcolor rgb 1\n\tparallel\n\tpoint_at<0,0,0>\n}\n// If winter==1, set a light to make the snow cover.\n#if(winter)\n\tlight_source{winter_light}\n#end\n\n\n')
            f.write('// ----------------------------------\n')
            f.write('//\n')
            f.write('// the name of the object with all objects merged must be "obj"\n')
            f.write('//\n')
            f.write('// ---make objects below this line---\n')
            f.write('#declare obj=\n')
            f.write('\n\n\n\n\n\n\n\n\n\n\n\n')
            f.write('// ---make objects above this line---\n')
            f.write('// \n//\n//\n')
            f.write('// ---put the obj---\n')
            f.write('#declare output_obj=\nobject{\n\tobj\n}\n')
            f.write('// ---output_area_set---\n')
            f.write('#declare output_area_set_x=\n')
            f.write('#if(make_front_image)\n')
            f.write('object{merge{box{<0-0.1,paksize/8,0-0.1>,<paksize*int_x/2+0.1,paksize*int_y,paksize*int_z/2+0.1>}box{<0-0.11,0+paksize/128,paksize*int_z/4>,<paksize*int_x/2+0.11,paksize*int_y,paksize*int_z/2+0.11>}}}\n')
            f.write('#else\n')
            f.write('object{box{<0-0.1,-paksize*int_y,0-0.1>,<paksize*int_x/2+0.1,paksize*int_y,paksize*int_z/2>}}\n')            
            f.write('#end\n')
            f.write('#declare output_area_set_z=\n')
            f.write('#if(make_front_image)\n')
            f.write('object{merge{box{<-paksize,paksize/8,-paksize>,<paksize*(int_x+2)/2+0.1,paksize*int_y,paksize*(int_z+2)/2+0.1>}box{<paksize*int_x/4,0+paksize/128,0-0.11>,<paksize*int_x/2+0.11,paksize*int_y,paksize*int_z/2+0.11>}}}\n')
            f.write('#else\n')
            f.write('object{box{<-paksize,-paksize*int_y,-paksize>,<paksize*(int_x+2)/2+0.1,paksize*int_y,paksize*(int_z+2)/2>}}\n')            
            f.write('#end\n')
            f.write('// Place objects in 4 directions\n')
            f.write('object{merge{\n\tobject{\n')
            f.write('\tintersection{object{output_obj}\n\tobject{output_area_set_x}}\n\t\ttranslate<-1,0,1>*paksize*number_width*3/4\n\t}\n\tobject{\n')
            f.write('\tintersection{object{output_obj\n\t\trotate<0,90,0>\n\t\ttranslate<0,0,1>*paksize*int_x/2}\n\tobject{output_area_set_z}}\n\t\ttranslate<-1,0,1>*paksize*number_width*1/4\n\t}\n\tobject{\n')
            f.write('\tintersection{object{output_obj\n\t\trotate<0,180,0>\n\t\ttranslate<0,0,1>*paksize*int_y/2\n\t\ttranslate<1,0,0>*paksize*int_x/2}\n\tobject{output_area_set_x}}\n\t\ttranslate<-1,0,1>*paksize*number_width*(-1)/4\n\t}\n\tobject{\n')
            f.write('\tintersection{object{output_obj\n\t\trotate<0,270,0>\n\t\ttranslate<1,0,0>*paksize*int_y/2}\n\tobject{output_area_set_z}}\n\t\ttranslate<-1,0,1>*paksize*number_width*(-3)/4\n\t}}\n\tscale<1,.8165,1> // To set 1 distance of y direction as 1px, rescaling the hight\n}\n')
        return
    def make_template(self):
        self.write_snow()
        print("make snow.inc")
        self.write_file(self.outfile)
        print("make "+self.outfile)
        print("make templates successfully")
        return