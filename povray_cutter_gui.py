import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import cutting_povray_results as cpr
import povray_render_for_simutrans as prfs



def make_window():
    def ask_files():
        path=filedialog.askopenfilename(filetype=[("pov-ray files","*.pov")],defaultextension=".pov")
        file_path.set(path)
    def ask_template():
        output_file_template = filedialog.asksaveasfilename(
            filetype=[("pov-ray files","*.pov")],defaultextension=".pov"
        )
        print(output_file_template)
        prfs.povray_template(output_file_template).make_template()

    def app():
        paksize=(input_pak_box.get())
        input_file = file_path.get()
        N_East=Dims_x.get()
        N_South=Dims_y.get()
        N_Hight=Dims_z.get()
        with_front=int(make_front_var.get())
        with_winter=int(winter_var.get())
        with_dat=int(makedat_var.get())

        output_file = filedialog.asksaveasfilename(
            filetype=[("PNG Image Files","*.png")],defaultextension=".png"
        )
        print(output_file)
        if not input_file or not output_file or not paksize or not N_East or not N_South or not N_Hight:
            return
        if (int(paksize))%4!=0 or int(paksize)<0:
            messagebox.showinfo("エラー","4の倍数を指定してください")
            return
        afterfile = cpr.pov_ray_cutting(input_file,output_file,paksize,N_East,N_South,N_Hight,with_winter,with_dat,with_front)
        temp_flag=afterfile.flag()
        if temp_flag ==0:
            messagebox.showinfo("エラー","画像がありません")
        elif temp_flag ==1:
            makedat_var.set(False)
            messagebox.showinfo("完了","完了しました。")
        elif temp_flag ==2:
            messagebox.showinfo("エラー","画像サイズまたは数値の入力が正しくありません")
    main_win = tk.Tk()
    main_win.title("simutrans building addon maker with pov-ray")
    main_win.geometry("700x200")
    main_frm = ttk.Frame(main_win)
    main_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
    file_path=tk.StringVar()
    folder_label = ttk.Label(main_frm, text="pov-rayファイルを選択")
    folder_box = ttk.Entry(main_frm,textvariable=file_path)
    folder_btn = ttk.Button(main_frm, text="選択",command=ask_files)
    template_btn = ttk.Button(main_frm, text=".povファイルを作成",command=ask_template)
    input_pak_label = ttk.Label(main_frm, text="pak size")
    input_pak_box = ttk.Entry(main_frm)
    make_front_var = tk.BooleanVar()
    make_front_var.set(False)
    make_front_checkbutton = ttk.Checkbutton(main_frm,variable=make_front_var, text="Front画像も作る")
    winter_var = tk.BooleanVar()
    winter_var.set(False)
    winter_checkbutton = ttk.Checkbutton(main_frm,variable=winter_var, text="積雪画像も作る")
    makedat_var = tk.BooleanVar()
    makedat_var.set(False)
    makedat_checkbutton = ttk.Checkbutton(main_frm,variable=makedat_var, text="datファイル作成")
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
    template_btn.grid(column=4,columnspan=3,row=1)
    input_pak_box.grid(column=1,columnspan=2,row=1,sticky=tk.EW,padx=5)
    input_pak_label.grid(column=0,row=1)
    Dims_label.grid(column=0,row=2)
    Dims_x.grid(column=1,columnspan=2,row=2,padx=5)
    Dims_y.grid(column=3,columnspan=2,row=2,padx=5)
    Dims_z.grid(column=5,columnspan=2,row=2,padx=5)
    make_front_checkbutton.grid(column=0,columnspan=3,row=3,padx=5)
    winter_checkbutton.grid(column=2,columnspan=3,row=3,padx=5)
    makedat_checkbutton.grid(column=4,columnspan=3,row=3,padx=5)
    Dims_attantion_label.grid(column=1,columnspan=6,row=4)
    app_btn.grid(column=1,columnspan=5,row=5)
    #main_win.columnconfigure(0, wieght=1)
    #main_win.rowconfigure(0, wieght=1)
    #main_frm.columnconfigure(1, wieght=1)
    main_win.mainloop()
    