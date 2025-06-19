import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os

class tile_cutter_rgba():
    def __init__(self, input_file, output_file, paksize,location_x,location_y,N_East,N_South,N_Hight):
        self.input=input_file
        self.output=output_file
        self.paksize=int(paksize)
        self.location_x=int(location_x)
        self.location_y=int(location_y)
        self.Nx=int(N_East)
        self.Ny=int(N_South)
        self.Nz=int(N_Hight)
    def flag(self):
        if os.path.isfile(self.input)==False:
            return 0
        else:
            imge = Image.open(self.input)
            print(imge.mode)
            im = np.array(imge)
            print(im.shape)
            imX = im.shape[1]
            imY = im.shape[0]
            if self.location_x<0 or self.location_x>=imX:
                print(self.location_x)
                return 2
            if self.location_y<0 or self.location_y>imY:
                print(self.location_y)
                return 2
            if self.Nz<0:
                return 2
            if imge.mode == "RGBA":
                modemode=2
            elif imge.mode=="RGB":
                modemode=0
            else:
                return 2
            #if imge.mode=="P":
            #    modemode=1
            print(im[0,0])
            if self.paksize>0 and self.paksize%4==0:
                output=Image.fromarray(cutting_program(im,self.paksize,modemode,self.location_x,self.location_y,self.Nx,self.Ny,self.Nz,imX,imY))
                output.save(self.output)
                return 1
            else: 
                return 2
def cutting_program(inimg,paksize,mode,basepoint_x,basepoint_y,Nx,Ny,Nz,max_x,max_y):
    temp_img=inimg
    if Nz==0:
        temp_mode=0
        using_Nz=1
    else:
        temp_mode=1
        using_Nz=Nz
    def def_bg_color(mode):
        if mode == 0:
            return np.array([231,255,255])
        elif mode == 2:
            return np.array([0,0,0,0])
    bgcolor=def_bg_color(mode)
    outimg=np.zeros(Nx*Ny*using_Nz*paksize**2*len(bgcolor)).reshape((Ny*using_Nz)*paksize,Nx*paksize,len(bgcolor))
    def cutting(temp_base_x,temp_base_y,temp_Nx,temp_Ny,temp_Nz):
        for ix in range(paksize):
            for iy in range(paksize):
                temp_x=ix+temp_base_x-paksize//2
                temp_y=iy+temp_base_y-paksize
                if 0<=temp_x<max_x:
                    if 0<=temp_y<max_y:
                        if temp_Nz == 1:
                            if ix<paksize//2:
                                if temp_mode==0:
                                    if -(ix//2)+temp_base_y-paksize//4<=temp_y<=(ix//2)+temp_base_y-paksize//4:
                                        temp_return=temp_img[temp_y,temp_x]
                                    else:
                                        temp_return=bgcolor
                                else:
                                    if temp_base_y-paksize<=temp_y<=(ix//2)+temp_base_y-paksize//4:
                                        temp_return=temp_img[temp_y,temp_x]
                                        # print(temp_return,temp_img[temp_y,temp_x],temp_y,temp_x)
                                    else:
                                        temp_return=bgcolor
                            else:
                                if temp_mode==0:
                                    if -((paksize-ix-1)//2)+temp_base_y-paksize//4<=temp_y<=((paksize-ix-1)//2)+temp_base_y-paksize//4:
                                        temp_return=temp_img[temp_y,temp_x]
                                    else:
                                        temp_return=bgcolor
                                else:
                                    if temp_base_y-paksize<=temp_y<=((paksize-ix-1)//2)+temp_base_y-paksize//4:
                                        temp_return=temp_img[temp_y,temp_x]
                                    else:
                                        temp_return=bgcolor
                        else:
                            temp_return=temp_img[temp_y,temp_x]
                    else:
                        temp_return=bgcolor
                else:
                    temp_return=bgcolor
                outimg[(temp_Ny+Ny*temp_Nz)*paksize+iy,temp_Nx*paksize+ix]=temp_return
                if temp_mode!=0:
                    if (ix<paksize//2 and temp_base_y-paksize*3//4<=temp_y<=(ix//2)+temp_base_y-paksize//4) or (ix>paksize//2-1 and temp_base_y-paksize*3//4<=temp_y<=((paksize-ix-1)//2)+temp_base_y-paksize//4):
                        temp_img[temp_y,temp_x]=bgcolor
    def extract_copy():
        for temp_Nz in range(using_Nz):
            for temp_Nx in range(Nx):
                for temp_Ny in range(Ny):
                    temp_base_x=basepoint_x-(Nx-1-temp_Nx)*paksize//2+(Ny-1-temp_Ny)*paksize//2
                    temp_base_y=basepoint_y-(Nx-1-temp_Nx)*paksize//4-(Ny-1-temp_Ny)*paksize//4-(temp_Nz)*paksize
                    cutting(temp_base_x,temp_base_y,temp_Nx,temp_Ny,temp_Nz)
        
                        
    # def change_size(inimg,beforesize,aftersize):
    #     imX = inimg.shape[0]
    #     imY = inimg.shape[1]
    #     ratioX = imX//beforesize
    #     ratioY = imY//beforesize
    #     print(bgcolor)
    #     if beforesize==aftersize:
    #         return inimg
    #     else:
    #         if beforesize<aftersize:
    #             results=np.zeros(ratioX*aftersize*ratioY*aftersize*len(bgcolor)).reshape(ratioX*aftersize,ratioY*aftersize,len(bgcolor))
    #             if beforesize>31 and aftersize>31: 
    #                 iconlist=search_icon(inimg,beforesize)
    #             else:
    #                 iconlist=[]
    #             for i in range(ratioX*aftersize):
    #                 for j in range(ratioY*aftersize):
    #                     ratioi=i%aftersize-(aftersize-beforesize)//2
    #                     ratioj=j%aftersize-(aftersize-beforesize)//2
    #                     coli=i//aftersize
    #                     colj=j//aftersize
    #                     if [coli,colj]in iconlist:
    #                         if 0<=i-coli*aftersize<32 and 0<=j-colj*aftersize<32:
    #                             results[i,j]=inimg[i-coli*aftersize+coli*beforesize,j-colj*aftersize+colj*beforesize]
    #                         else:
    #                             results[i,j]=bgcolor                        
    #                     elif 0<=ratioi<beforesize:
    #                         if 0<=ratioj<beforesize:
    #                             results[i,j]=inimg[coli*beforesize+ratioi,colj*beforesize+ratioj]
    #                         else:
    #                             results[i,j]=bgcolor
    #                     else:
    #                         results[i,j]=bgcolor
    #             return results
    #         else:
    #             changeratio=beforesize//aftersize+1
    #             results=np.zeros(ratioX*aftersize*ratioY*aftersize*changeratio**2).reshape(ratioX*aftersize*changeratio,changeratio*ratioY*aftersize)
    #             for i in range(ratioX):
    #                 for j in range(ratioY):
    #                     ratioi=i%aftersize
    #                     ratioj=j&aftersize
    #                     coli=i//aftersize
    #                     colj=j//aftersize
    extract_copy() 
    outimg=outimg.astype(np.uint8)
    # print(outimg)
    print(outimg.shape)
    return outimg



def make_window():
    def ask_files():
        path=filedialog.askopenfilename()
        file_path.set(path)

    def app():
        paksize=(input_pak_box.get())
        input_file = file_path.get()
        location_x=basepoint_box_x.get()
        location_y=basepoint_box_y.get()
        N_East=Dims_x.get()
        N_South=Dims_y.get()
        N_Hight=Dims_z.get()
        output_file = filedialog.asksaveasfilename(
            filetype=[("PNG Image Files","*.png")],defaultextension=".png"
        )
        print(output_file)
        if not input_file or not output_file or not paksize or not location_x or not location_y or not N_East or not N_South or not N_Hight:
            return
        if (int(paksize))%4!=0 or int(paksize)<0:
            messagebox.showinfo("エラー","4の倍数を指定してください")
            return
        afterfile = tile_cutter_rgba(input_file,output_file,paksize,location_x,location_y,N_East,N_South,N_Hight)
        if afterfile.flag() ==0:
            messagebox.showinfo("エラー","画像がありません")
        elif afterfile.flag() ==1:
            messagebox.showinfo("完了","完了しました。")
        elif afterfile.flag() ==2:
            messagebox.showinfo("エラー","画像サイズまたは数値の入力が正しくありません")
    main_win = tk.Tk()
    main_win.title("TILE CUTTER for RGBA")
    main_win.geometry("700x200")
    main_frm = ttk.Frame(main_win)
    main_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
    file_path=tk.StringVar()
    folder_label = ttk.Label(main_frm, text="ファイルを選択")
    folder_box = ttk.Entry(main_frm,textvariable=file_path)
    folder_btn = ttk.Button(main_frm, text="選択",command=ask_files)
    input_pak_label = ttk.Label(main_frm, text="pak size")
    input_pak_box = ttk.Entry(main_frm)
    basepoint_label_x = ttk.Label(main_frm, text="起点の頂点座標 x,y")
    basepoint_box_x = ttk.Entry(main_frm)
    basepoint_box_y = ttk.Entry(main_frm)
    basepoint_box_x.insert(tk.END,"64")
    basepoint_box_y.insert(tk.END,"128")
    Dims_label=ttk.Label(main_frm,text="建物の形状(Dims)=(東西,南北,高さ)")
    Dims_attantion_label=ttk.Label(main_frm,text="高さを0にすると、地面のみの画像として切り出されます")
    Dims_x=ttk.Entry(main_frm)
    Dims_y=ttk.Entry(main_frm)
    Dims_z=ttk.Entry(main_frm)
    Dims_x.insert(tk.END,"1")
    Dims_y.insert(tk.END,"1")
    Dims_z.insert(tk.END,"1")

    app_btn=ttk.Button(main_frm, text="変換を実行",command=app)
    folder_label.grid(column=0,row=0,pady=10)
    folder_box.grid(column=1,columnspan=5,row=0,sticky=tk.EW, padx=5)
    folder_btn.grid(column=6,row=0)
    input_pak_box.grid(column=1,columnspan=2,row=1,sticky=tk.EW,padx=5)
    input_pak_label.grid(column=0,row=1)
    basepoint_label_x.grid(column=0,row=2)
    basepoint_box_x.grid(column=1,columnspan=2,row=2,padx=5)
    basepoint_box_y.grid(column=3,columnspan=2,row=2,padx=5)
    Dims_label.grid(column=0,row=3)
    Dims_x.grid(column=1,columnspan=2,row=3,padx=5)
    Dims_y.grid(column=3,columnspan=2,row=3,padx=5)
    Dims_z.grid(column=5,columnspan=2,row=3,padx=5)
    Dims_attantion_label.grid(column=1,columnspan=6,row=4)
    app_btn.grid(column=1,columnspan=5,row=5)
    #main_win.columnconfigure(0, wieght=1)
    #main_win.rowconfigure(0, wieght=1)
    #main_frm.columnconfigure(1, wieght=1)
    main_win.mainloop()
    