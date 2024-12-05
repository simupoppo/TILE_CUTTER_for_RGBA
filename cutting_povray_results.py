from TILE_CUTTER_RGBA import tile_cutter_rgba
from povray_render_for_simutrans import render_povray
import os
class cutting_results():
    def __init__(self,infile,outfile,paksize,tilesize_x,tilesize_y,tilesize_z,winter,with_dat,make_front=0):
        self.infile=infile
        self.outfile=outfile
        self.paksize=int(paksize)
        self.Nx=int(tilesize_x)
        self.Ny=int(tilesize_y)
        self.Nz=int(tilesize_z)
        self.winter=int(winter)
        self.with_dat=int(with_dat)
        self.make_front=int(make_front)
    def flag(self):
        for i in range(4):
            outfile_name=self.outfile[:-4]+"_"+str(i)
            if self.winter==1:
                outfile_name+="-winter"
            outfile_name+=".png"
            # base_point_x=self.paksize//2*max(self.Nx,self.Ny)*(2*i+1)
            # base_point_y=self.paksize//2*(max(self.Nx,self.Ny,self.Nz//2)+max(self.Nx,self.Ny))
            temp_Nx=((self.Nx+self.Ny)+(-1)**i*(self.Nx-self.Ny))//2
            temp_Ny=((self.Nx+self.Ny)-(-1)**i*(self.Nx-self.Ny))//2
            base_point_x=self.paksize//2*(max(self.Nx,self.Ny)*(2*i+1)+(-1)**i*(self.Nx-self.Ny))
            base_point_y=self.paksize//4*(2*max(self.Nx,self.Ny,self.Nz//2)+self.Nx+self.Ny)
            a=tile_cutter_rgba(self.infile,outfile_name,self.paksize,base_point_x,base_point_y,temp_Nx,temp_Ny,self.Nz)
            temp_flag=a.flag()
            if temp_flag!=1:
                return temp_flag
            elif self.with_dat==1:
                write_dat(self.outfile[:-4]+".dat",outfile_name[:-4],i,temp_Nx,temp_Ny,self.Nz,self.winter,int(max(1-self.winter-i,0)),self.make_front).writing_dat()
        return 1
class pov_ray_cutting():
    def __init__(self,infile,outfile,paksize,Nx,Ny,Nz,withwinter,with_dat,make_front=str(0)):
        self.infile=infile
        self.outfile=outfile
        self.paksize=int(paksize)
        self.Nx=int(Nx)
        self.Ny=int(Ny)
        self.Nz=int(Nz)
        self.withwinter=int(withwinter)
        self.with_dat=int(with_dat)
        self.make_front=int(make_front)
    def flag(self):
        if self.Nx<1 or self.Ny<1 or self.Nz<0:
            return 2
        if self.paksize%4!=0:
            return 2
        if os.path.isfile(self.infile)==False:
            return 2
        temp_flag=self.run_all(0)
        if temp_flag!=1:
            return temp_flag
        if self.withwinter==1:
            temp_flag=self.run_all(1)
            if temp_flag!=1:
                return temp_flag
        return 1
    def run_all(self,temp_winter):
        outfile_name=self.outfile
        temp_render=render_povray(self.infile,outfile_name,self.paksize,self.Nx,self.Ny,self.Nz,temp_winter,0)
        temp_flag_render=temp_render.flag()
        if temp_flag_render==False:
            return 3
        else:
            if temp_winter==0:
                temp_flag_cutter=cutting_results(outfile_name,outfile_name,self.paksize,self.Nx,self.Ny,self.Nz,temp_winter,self.with_dat,0)
            else:
                temp_flag_cutter=cutting_results(outfile_name[:-4]+"-winter"+".png",outfile_name,self.paksize,self.Nx,self.Ny,self.Nz,temp_winter,self.with_dat,0)    
            if temp_flag_cutter.flag()!=1:
                return temp_flag_cutter.flag()
        if self.make_front==1:
            outfile_name=outfile_name[:-4]+"_front"+".png"
            temp_render=render_povray(self.infile,outfile_name,self.paksize,self.Nx,self.Ny,self.Nz,temp_winter,1)
            temp_flag_render=temp_render.flag()
            if temp_flag_render==False:
                return 3
            else:
                if temp_winter==0:
                    temp_flag_cutter=cutting_results(outfile_name,outfile_name,self.paksize,self.Nx,self.Ny,self.Nz,temp_winter,self.with_dat,self.make_front)
                else:
                    temp_flag_cutter=cutting_results(outfile_name[:-4]+"-winter"+".png",outfile_name,self.paksize,self.Nx,self.Ny,self.Nz,temp_winter,self.with_dat,self.make_front)  
                return temp_flag_cutter.flag()  
        else: 
            return temp_flag_cutter.flag()
            
class write_dat():
    def __init__(self,outfile_dat,outfile,direc,Nx,Ny,Nz,winter,first,make_front=0,dims_number=4):
        self.outfile_dat=outfile_dat
        self.outfile=outfile
        self.direc=int(direc)
        self.Nx=int(Nx)
        self.Ny=int(Ny)
        self.Nz=int(Nz)
        self.winter=int(winter)
        self.with_Dims=int(first)
        self.make_front=int(make_front)
        self.dims_number=int(dims_number)
    def writing_dat(self):
        def writing_way(direc,temp_x,temp_y,temp_z,temp_Ny,winter,image):
            if self.make_front==1:
                return "FrontImage["+str(direc)+"]["+str(temp_y)+"]["+str(temp_x)+"]["+str(temp_z)+"][0]["+str(winter)+"]="+str(image)+"."+str(temp_x)+"."+str(temp_y+temp_z*temp_Ny)+"\n"
            else:
                return "BackImage["+str(direc)+"]["+str(temp_y)+"]["+str(temp_x)+"]["+str(temp_z)+"][0]["+str(winter)+"]="+str(image)+"."+str(temp_x)+"."+str(temp_y+temp_z*temp_Ny)+"\n"
        with open(self.outfile_dat,mode="a") as f:
            print(self.outfile_dat)
            if self.with_Dims==1:
                f.write("Dims="+str(self.Nx)+","+str(self.Ny)+","+str(self.dims_number)+"\n")
            for ix in range(self.Nx):
                for iy in range(self.Ny):
                    for iz in range(max(1,self.Nz)):
                        f.write(writing_way(self.direc,ix,iy,iz,self.Ny,self.winter,self.outfile))


