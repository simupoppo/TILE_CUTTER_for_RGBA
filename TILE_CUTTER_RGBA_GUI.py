import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import TILE_CUTTER_RGBA


class TILE_CUTTER_RGBA_GUI:
    def __init__(self, root, language="ja"):
        self.root = root
        self.language = tk.StringVar(value=language)
        # タイトル
        self.root.title("TILE CUTTER for RGBA GUI ver")

        # 翻訳辞書
        self.translations = {
            "ja": {
                "title": "画像ビューア",
                "file": "ファイル",
                "open_image": "画像を開く",
                "export_cut": "切り出し画像を出力",
                "exit": "終了",
                "setting": "設定",
                "output_dat": "DATファイルを出力",
                "inverse_drag": "右ドラッグ反転",
                "language": "言語/Language",
                "lang_ja": "日本語",
                "lang_en": "English",
                "pak_size": "pakサイズ",
                "east": "東",
                "south": "南",
                "height": "高さ",
                "refresh": "更新",
                "frame_base": "基準点",
                "direction": "方向",
                "error": "エラー",
                "Message": "メッセージ",
                "No Image!": "画像がありません!",
                "Export done!": "出力成功",
                "Invalid figure size!": "画像サイズが不正です"
            },
            "en": {
                "title": "Image Viewer",
                "file": "File",
                "open_image": "Open Image",
                "export_cut": "Export Cutting Image",
                "exit": "Exit",
                "setting": "Settings",
                "output_dat": "Export DAT file",
                "inverse_drag": "Reverse Right Drag",
                "language": "Language/言語",
                "lang_ja": "日本語",
                "lang_en": "English",
                "pak_size": "Pak size",
                "east": "East",
                "south": "South",
                "height": "Height",
                "refresh": "Refresh",
                "frame_base": "Frame Base",
                "direction": "Direction",
                "error": "Error",
                "Message": "Message",
                "No Image!": "No Imamge!",
                "Export done!": "Export Done!",
                "Invalid figure size!": "Invalid figure size!"
            }
        }

        # GUI変数
        self.base_size = 128
        self.num_x = 1
        self.num_y = 1
        self.num_h = 1
        self.output_direction = 0
        # 選択範囲（複数ポリゴンを "selection" タグで管理）
        self.selection_group = [] 
        self.selection_origin_x = self.base_size//2 
        self.selection_origin_y = self.base_size

        self.reverse_right_drag = tk.BooleanVar(value=False)
        self.output_dat = tk.BooleanVar(value=False)

        # キャンバス
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # 画像関連 
        self.original_image = None 
        self.display_image = None 
        self.image_id = None 
        self.image_scale = 1.0 
        self.image_offset_x = 0 
        self.image_offset_y = 0
        # ドラッグ用変数 
        self.drag_start_x = 0 
        self.drag_start_y = 0 
        self.rect_dragging = False 
        self.image_dragging = False 
        # 右ドラッグ反転フラグ 
        self.reverse_right_drag = tk.BooleanVar(value=False) 
        # DAT出力フラグ 
        self.output_dat = tk.BooleanVar(value=False) 
        # 出力方向 
        self.output_direction = 0 
        # イベント 
        self.canvas.bind("<ButtonPress-1>", self.on_left_press) 
        self.canvas.bind("<B1-Motion>", self.on_left_drag) 
        self.canvas.bind("<ButtonPress-3>", self.on_right_press) 
        self.canvas.bind("<B3-Motion>", self.on_right_drag) 
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel) 
        # Windows/mac 
        self.canvas.bind("<Button-4>", self.on_mouse_wheel_linux) 
        # Linux 上スクロール 
        self.canvas.bind("<Button-5>", self.on_mouse_wheel_linux) 
        # Linux 下スクロール

        # 入力欄フレーム
        self.base_label_var=tk.StringVar()
        self.east_label_var=tk.StringVar()
        self.south_label_var=tk.StringVar()
        self.height_label_var=tk.StringVar()
        self.refresh_btn_var=tk.StringVar()
        self.frame_base_label_var=tk.StringVar()
        self.direction_label_var=tk.StringVar()
        self.separatesize_frame = tk.Frame(root)
        self.separatesize_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.base_label = tk.Label(self.separatesize_frame,textvariable=self.base_label_var)
        self.base_entry = tk.Entry(self.separatesize_frame, width=5)
        self.base_entry.insert(0, str(self.base_size))

        self.east_label = tk.Label(self.separatesize_frame,textvariable=self.east_label_var)
        self.numx_entry = tk.Entry(self.separatesize_frame, width=5)
        self.numx_entry.insert(0, str(self.num_x))

        self.south_label = tk.Label(self.separatesize_frame,textvariable=self.south_label_var)
        self.numy_entry = tk.Entry(self.separatesize_frame, width=5)
        self.numy_entry.insert(0, str(self.num_y))

        self.height_label = tk.Label(self.separatesize_frame,textvariable=self.height_label_var)
        self.numh_entry = tk.Entry(self.separatesize_frame, width=5)
        self.numh_entry.insert(0, str(self.num_h))

        self.refresh_btn = tk.Button(self.separatesize_frame, command=self.update_selection_size,textvariable=self.refresh_btn_var)

        self.base_label.pack(side=tk.LEFT)
        self.base_entry.pack(side=tk.LEFT)
        self.east_label.pack(side=tk.LEFT)
        self.numx_entry.pack(side=tk.LEFT)
        self.south_label.pack(side=tk.LEFT)
        self.numy_entry.pack(side=tk.LEFT)
        self.height_label.pack(side=tk.LEFT)
        self.numh_entry.pack(side=tk.LEFT)
        self.refresh_btn.pack(side=tk.LEFT)

        # 位置フレーム
        self.position_frame = tk.Frame(root)
        self.position_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.frame_base_label = tk.Label(self.position_frame,textvariable=self.frame_base_label_var)
        self.ox_entry = tk.Entry(self.position_frame, width=5)
        self.ox_entry.insert(0, "64")
        self.oy_entry = tk.Entry(self.position_frame, width=5)
        self.oy_entry.insert(0, "128")

        self.direction_label = tk.Label(self.position_frame,textvariable=self.direction_label_var)
        self.direction_entry = tk.Entry(self.position_frame, width=5)
        self.direction_entry.insert(0, str(self.output_direction))

        self.frame_base_label.pack(side=tk.LEFT)
        self.ox_entry.pack(side=tk.LEFT)
        self.oy_entry.pack(side=tk.LEFT)
        self.direction_label.pack(side=tk.LEFT)
        self.direction_entry.pack(side=tk.LEFT)

        # メニュー
        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.settingmenu = tk.Menu(self.menubar, tearoff=0)
        self.langmenu = tk.Menu(self.menubar, tearoff=0)
        self.language.trace_add("write", lambda *args: self.update_language())

        self.update_language()

    def update_language(self):
        self.filemenu.delete(0,tk.END)
        self.settingmenu.delete(0,tk.END)
        self.langmenu.delete(0,tk.END)
        
        lang = self.language.get()
        tr = self.translations[lang]
        
        # 新しいメニューオブジェクトを作成し、インスタンス変数として保持する
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.settingmenu = tk.Menu(self.menubar, tearoff=0)
        self.langmenu = tk.Menu(self.menubar, tearoff=0)
        
        # ファイルメニュー
        self.filemenu.add_command(label=tr["open_image"], command=self.open_image)
        self.filemenu.add_command(label=tr["export_cut"], command=self.output_image)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=tr["exit"], command=self.root.quit)

        # 設定メニュー
        self.settingmenu.add_checkbutton(
            label=tr["output_dat"],
            variable=self.output_dat
        )
        self.settingmenu.add_checkbutton(
            label=tr["inverse_drag"],
            variable=self.reverse_right_drag
        )

        # 言語メニュー
        self.langmenu.add_radiobutton(label="日本語", variable=self.language, value="ja")
        self.langmenu.add_radiobutton(label="English", variable=self.language, value="en")

        # メニューバーに各メニューをカスケードする
        self.menubar.add_cascade(label=tr["file"], menu=self.filemenu)
        self.menubar.add_cascade(label=tr["setting"], menu=self.settingmenu)
        self.menubar.add_cascade(label=tr["language"], menu=self.langmenu)
        if self.menubar.index("end") > 3:
            print(self.menubar.index("end"))
            self.menubar.delete(0,3)
        
        # メニューバーをウィンドウに設定
        self.root.config(menu=self.menubar)
        
        # 入力欄ラベル更新
        self.base_label_var.set(tr["pak_size"] + ":")
        self.east_label_var.set(tr["east"])
        self.south_label_var.set(tr["south"])
        self.height_label_var.set(tr["height"])
        self.refresh_btn_var.set(tr["refresh"])
        self.frame_base_label_var.set(tr["frame_base"])
        self.direction_label_var.set(tr["direction"])
        print("language change done")


    def update_selection_size(self):
        try:
            base = int(self.base_entry.get())
            numx = int(self.numx_entry.get())
            numy = int(self.numy_entry.get())
            numh = int(self.numh_entry.get())
            numox = int(self.ox_entry.get())
            numoy = int(self.oy_entry.get())
            direction = int(self.direction_entry.get())
        except ValueError:
            messagebox.showerror(("error"), ("must be integer value"))
            return

        if base % 4 != 0:
            messagebox.showerror(("error"), ("paksize must be multiple of 4"))
            return

        self.base_size = base
        self.output_direction = direction
        if(self.output_direction%2 == 0):
            self.num_x = numx
            self.num_y = numy
        else:
            self.num_x = numy
            self.num_y = numx
        self.num_h = numh
        self.selection_origin_x = numox
        self.selection_origin_y = numoy

        self.draw_selection()

    def open_image(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if not self.file_path:
            return

        self.original_image = Image.open(self.file_path)
        self.image_scale = 1.0
        self.image_offset_x = 0
        self.image_offset_y = 0
        self.update_image_display()
        self.draw_selection()

    def output_image(self):    
        lang = self.language.get()
        tr = self.translations[lang]
        if not self.image_id:
            messagebox.showinfo(tr["error"],tr["No Image!"])
            return
        output_file_path = filedialog.asksaveasfilename(
            filetype=[("PNG Image Files","*.png")],defaultextension=".png"
        )
        afterfile = TILE_CUTTER_RGBA.tile_cutter_rgba(self.file_path,output_file_path,self.base_size,self.selection_origin_x,self.selection_origin_y,self.num_x,self.num_y,self.num_h)
        if afterfile.flag() ==0:
            messagebox.showinfo(tr["error"],tr["No Image!"])
        elif afterfile.flag() ==1:
            if self.output_dat.get():
                outdatfile = output_file_path[:-3]+"dat"
                dat_results=TILE_CUTTER_RGBA.write_dat(outdatfile,output_file_path,0,self.num_x,self.num_y,self.num_h)
                dat_results.writing_dat()
            messagebox.showinfo(tr["Message"],tr["Export done!"])
        elif afterfile.flag() ==2:
            messagebox.showinfo(tr["error"],tr["Invalid figure size!"])

    def update_image_display(self):
        if self.original_image is None:
            return
        w, h = self.original_image.size
        new_size = (int(w * self.image_scale), int(h * self.image_scale))
        resized = self.original_image.resize(new_size, Image.LANCZOS)
        self.display_image = ImageTk.PhotoImage(resized)

        if self.image_id is None:
            self.image_id = self.canvas.create_image(self.image_offset_x, self.image_offset_y,
                                                    anchor="nw", image=self.display_image)
        else:
            self.canvas.itemconfig(self.image_id, image=self.display_image)
            self.canvas.coords(self.image_id, self.image_offset_x, self.image_offset_y)

        # 選択範囲を追従させる
        self.draw_selection()
    def draw_selection(self):
        self.canvas.delete("selection")
        if self.original_image is None:
            return

        size = self.base_size
        ox, oy = self.selection_origin_x, self.selection_origin_y


        # 四隅の座標
        if self.num_h>0:
            corners_img = [
                (ox, oy ),   # bottom
                (ox + (self.num_y * size)//2, oy - (self.num_y * size)//4),   # 右
                (ox + (self.num_y * size)//2, oy - (self.num_y * size)//4 - self.num_h * size + size//2 ),   #top_right
                (ox + (self.num_y-self.num_x) * size//2, oy - (self.num_x + self.num_y )*size//4 - self.num_h * size + size//2 ), # top
                (ox - (self.num_x * size)//2, oy - (self.num_x * size)//4 - self.num_h * size + size//2 ),   #top_left
                (ox - (self.num_x * size)//2, oy - (self.num_x * size)//4)    # 左
            ]
        else:
            corners_img = [
                (ox, oy ),   # bottom
                (ox + (self.num_y * size)//2, oy - (self.num_y * size)//4),   # 右
                (ox + (self.num_y-self.num_x) * size//2, oy - (self.num_x + self.num_y )*size//4 ), #top
                (ox - (self.num_x * size)//2, oy - (self.num_x * size)//4)    # 左
            ]


        # Canvas座標に変換
        def to_canvas(px, py):
            return (self.image_offset_x + px * self.image_scale,
                    self.image_offset_y + py * self.image_scale)

        coords = []
        for px, py in corners_img:
            coords.extend(to_canvas(px, py))

        self.canvas.create_polygon(
            coords, outline="red", fill="", width=2, tags="selection"
        )
    def on_left_press(self, event):
        if not self.canvas.find_withtag("selection"):
            return
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.rect_dragging = True

    def on_left_drag(self, event):
        if not self.rect_dragging:
            return
        dx_canvas = event.x - self.drag_start_x
        dy_canvas = event.y - self.drag_start_y
        self.drag_start_x = event.x
        self.drag_start_y = event.y

        dx_img = dx_canvas / self.image_scale
        dy_img = dy_canvas / self.image_scale

        new_ox = self.selection_origin_x + dx_img
        new_oy = self.selection_origin_y + dy_img

        # 移動後も画像内に収める制約
        size = self.base_size
        img_w, img_h = self.original_image.size
        total_w_r = self.num_y * size * .5
        total_w_l = self.num_x * size * .5
        total_h = (self.num_x+self.num_y) * size * .25 + max(0,self.num_h-1) * size

        # 画像に収まるように制限
        if new_ox < total_w_l:
            new_ox = total_w_l
        if new_ox + total_w_r > img_w:
            new_ox = img_w - total_w_r
        if new_oy < total_h:
            new_oy = total_h
        if new_oy > img_h:
            new_oy = img_h

        self.selection_origin_x = int(new_ox)
        self.selection_origin_y = int(new_oy)
        self.ox_entry.delete(0,tk.END)
        self.oy_entry.delete(0,tk.END)
        self.ox_entry.insert(0,str(self.selection_origin_x))
        self.oy_entry.insert(0,str(self.selection_origin_y))

        self.draw_selection()


    # ==== 右ドラッグで画像移動 ====
    def on_right_press(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.image_dragging = True

    def on_right_drag(self, event):
        if not self.image_dragging or self.image_id is None:
            return
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        if self.reverse_right_drag.get():
            dx = -dx
            dy = -dy

        self.image_offset_x += dx
        self.image_offset_y += dy
        self.update_image_display()
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    # ==== マウスホイールで拡大縮小 ====
    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.image_scale *= 1.1
        else:
            self.image_scale /= 1.1
        self.update_image_display()

    def on_mouse_wheel_linux(self, event):
        if event.num == 4:
            self.image_scale *= 1.1
        elif event.num == 5:
            self.image_scale /= 1.1
        self.update_image_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = TILE_CUTTER_RGBA_GUI(root)
    root.mainloop()
