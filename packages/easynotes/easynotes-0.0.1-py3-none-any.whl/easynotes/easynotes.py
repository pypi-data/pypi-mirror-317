#!/usr/bin/env python
# coding: utf-8

# 第一部分：程序说明###################################################################################
# coding=utf-8
# 药械不良事件工作平台
# 开发人：蔡权周
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk,GROOVE 
import pandas as pd
from tkinter.messagebox import showinfo 
class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("easynotes笔记软件 0.0.1")
        
        sw = self.root.winfo_screenwidth()  
        sh = self.root.winfo_screenheight()  
        ww = 1024  # 窗口宽度  
        wh = 768  # 窗口高度  
        x = (sw - ww) // 2  
        y = (sh - wh) // 2  
        self.root.geometry(f"{ww}x{wh}+{x}+{y}") 
		
        self.notes_df = pd.DataFrame(columns=["标题", "内容"])
        self.load_notes()
 
        # 顶部按钮
        self.create_buttons()
 
        # 左右框架
        self.create_frames()
 
        # 绑定事件
        self.title_listbox.bind("<<ListboxSelect>>", self.show_note_content)
        # 监听键盘和鼠标事件来检测内容变化
        self.content_text.bind("<Key>", self.on_content_change_key)
        self.content_text.bind("<Button-1>", self.on_content_change_click)  # 监听鼠标点击，但注意这可能导致频繁触发
    def on_content_change_key(self, event):
        """当用户在内容框中按键时更新内容"""
        self.on_content_change_internal()
 
    def on_content_change_click(self, event):
        """当用户在内容框中点击时尝试更新内容（注意：这可能导致频繁不必要的更新）"""
        # 这里我们可以添加一些逻辑来减少不必要的更新，比如检查光标位置是否改变等
        # 但为了简单起见，我们直接调用内部更新函数
        self.on_content_change_internal()
 
    def on_content_change_internal(self):
        """内部函数，用于实际更新 DataFrame 中的内容"""
        try:
            selected_index = self.title_listbox.curselection()[0]
            new_content = self.content_text.get(1.0, tk.END).strip()
            self.notes_df.loc[selected_index, "内容"] = new_content
        except IndexError:
            pass  # 无选中的标题 
 
    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X)
 
        self.open_button = tk.Button(button_frame, text="打开文件", command=self.open_file, bg="white", font=("微软雅黑", 10), relief=GROOVE, activebackground="green",)
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)
 
        self.add_button = tk.Button(button_frame, text="添加笔记", command=self.add_note, bg="white", font=("微软雅黑", 10), relief=GROOVE, activebackground="green",)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)
 
        self.delete_button = tk.Button(button_frame, text="删除笔记", command=self.delete_note, bg="white", font=("微软雅黑", 10), relief=GROOVE, activebackground="green",)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
 
        self.save_button = tk.Button(button_frame, text="保存笔记", command=self.save_notes, bg="white", font=("微软雅黑", 10), relief=GROOVE, activebackground="green",)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(button_frame, text="另存文件", command=self.save_file, bg="white", font=("微软雅黑", 10), relief=GROOVE, activebackground="green",)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.save_button = tk.Button(button_frame, text="开发信息", command=lambda:showinfo(title="关于", message="清粥小菜，411703730@qq.com"), bg="white", font=("微软雅黑", 10), relief=GROOVE, activebackground="green",)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
 
    def create_frames(self):
        # 左侧标题栏
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, expand=False)
 
        self.title_listbox = tk.Listbox(left_frame, width=40, height=20, exportselection=0)
        self.title_listbox.pack(fill=tk.BOTH, expand=True)
        self.update_title_listbox()
 
        # 右侧内容栏
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5, expand=True)
 
        self.content_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=60, height=20)
        self.content_text.pack(fill=tk.BOTH, expand=True)
 
    def load_notes(self):
        try:
            # 尝试加载.xlsx文件（确保已安装openpyxl库）
            self.notes_df = pd.read_excel("data.xlsx")
        except FileNotFoundError:
            messagebox.showwarning("警告", "未找到笔记文件，将使用空数据表。")
        except Exception as e:
            messagebox.showerror("错误", f"加载文件时出错: {e}")
 
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                self.notes_df = pd.read_excel(file_path)
                self.update_title_listbox()
                if self.title_listbox.size() > 0:
                    self.title_listbox.select_set(0)  # 默认选择第一个
                    self.show_note_content(event=None)
            except Exception as e:
                messagebox.showerror("错误", f"打开文件时出错: {e}")
 
    def add_note(self):
        
        
        roots = tk.Tk()
        roots.title("添加标题")
        
        sw = roots.winfo_screenwidth()  
        sh = roots.winfo_screenheight()  
        ww = 200  # 窗口宽度  
        wh = 80  # 窗口高度  
        x = (sw - ww) // 2  
        y = (sh - wh) // 2  
        roots.geometry(f"{ww}x{wh}+{x}+{y}") 
        
      # 创建标题输入框
        #title_var = tk.StringVar()
        title_entry = tk.Entry(roots, width=30)
        title_entry.pack(pady=10)
 
        # 创建确定和取消按钮
        def on_ok(title):           
            if title:
                new_row = {"标题": title, "内容": ""}
                self.notes_df.loc[len(self.notes_df)] = new_row
                self.update_title_listbox()
                self.title_listbox.select_set(self.title_listbox.size() - 1)
                self.show_note_content(event=None)
                roots.destroy()  # 关闭添加窗口
            else:
                messagebox.showwarning("警告", "标题不能为空！")
 
        def on_cancel():
            roots.destroy()  # 关闭添加窗口
 
        ok_button = tk.Button(roots, text="确定", command=lambda:on_ok(title_entry.get().strip()), bg="white", font=("微软雅黑",10), relief=GROOVE, activebackground="green",)
        ok_button.pack(side=tk.RIGHT, padx=5, pady=5)
 
        cancel_button = tk.Button(roots, text="取消", command=on_cancel, bg="white", font=("微软雅黑",10), relief=GROOVE, activebackground="green",)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)
 
        
    def delete_note(self):
        try:
            selected_index = self.title_listbox.curselection()[0]
            self.notes_df = self.notes_df.drop(selected_index).reset_index(drop=True)
            self.update_title_listbox()
            if selected_index < self.title_listbox.size():
                self.title_listbox.select_set(selected_index)
            elif self.title_listbox.size() > 0:
                self.title_listbox.select_set(self.title_listbox.size() - 1)
            self.show_note_content(event=None)
        except IndexError:
            pass  # 无选中的标题
 
    def save_notes(self):
        try:
            # 保存为.xlsx文件
            self.notes_df.to_excel("data.xlsx", index=False)
            messagebox.showinfo("保存成功", "笔记已保存至data.xlsx")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存文件时出错: {e}")

    def save_file(self):
        try:
            # 保存为.xlsx文件
            file_path_flhz = filedialog.asksaveasfilename(  
            title="保存文件",  
            initialfile="笔记",  
            defaultextension=".xlsx",  
            filetypes=[("Excel 工作簿", "*.xlsx")],  
            )  
            if not file_path_flhz:  
                return  # 如果用户点击取消，则退出函数
            self.notes_df.to_excel(file_path_flhz, index=False)
            messagebox.showinfo("保存成功", "笔记已保存。")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存文件时出错: {e}")

    def update_title_listbox(self):
        self.title_listbox.delete(0, tk.END)
        for _, row in self.notes_df.iterrows():
            self.title_listbox.insert(tk.END, row["标题"])
 
    def show_note_content(self, event):
        try:
            selected_index = self.title_listbox.curselection()[0]
            content = self.notes_df.loc[selected_index, "内容"]
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, content)
        except IndexError:
            self.content_text.delete(1.0, tk.END)
 
    def on_content_change(self, event):
        try:
            selected_index = self.title_listbox.curselection()[0]
            new_content = self.content_text.get(1.0, tk.END).strip()
            self.notes_df.loc[selected_index, "内容"] = new_content
        except IndexError:
            pass  # 无选中的标题
 
if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
