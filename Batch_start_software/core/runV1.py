import os
import sys
import json
import time
import psutil
import subprocess
import tkinter as tk
import uuid
import threading
from tkinter import ttk, filedialog, simpledialog, messagebox, Menu, Toplevel


class ModernSoftwareLauncher:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # 软件列表数据结构：[{id, name, path, delay, group}, ...]
        self.software_list = []
        self.config_path = os.path.join(os.path.expanduser("~"), ".launcher_config_v2.json")
        self.selected_items = set()  # 存储选中软件的ID
        self.current_group = "所有分组"  # 当前筛选分组
        
        # 创建界面和加载配置
        self.create_widgets()
        self.create_menu()
        self.apply_styles()
        # 使用after方法确保界面组件完全初始化后再加载配置
        self.root.after(100, self.load_config_and_refresh)
        
    def load_config_and_refresh(self):
        """加载配置并刷新界面"""
        self.load_config()
        self.refresh_tree()
        
    def setup_window(self):
        """设置主窗口属性"""
        self.root.title("现代软件启动器 v2.1")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        self.center_window()
        
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    # def apply_styles(self):
    #     """应用现代化样式"""
    #     style = ttk.Style()
        
    #     # 1. Treeview基础样式（交替行+选中效果）
    #     style.configure("Treeview", 
    #                    background="white",
    #                    foreground="#333333",
    #                    rowheight=32,
    #                    fieldbackground="white",
    #                    borderwidth=0,
    #                    font=("微软雅黑", 9))
        
    #     # 交替行颜色+选中高亮
    #     style.map("Treeview",
    #              background=[('selected', '#3498db'), ('alternate', '#f8f9fa')],
    #              foreground=[('selected', 'white')],
    #              relief=[('active', 'groove')])
        
    #     # 2. Treeview表头样式（深色背景）
    #     style.configure("Treeview.Heading",
    #                    background="#2c3e50",
    #                    foreground="white",
    #                    font=("微软雅黑", 10, "bold"),
    #                    padding=(12, 0),
    #                    relief="flat")
        
    #     # 3. 按钮样式区分（主次按钮）
    #     style.configure("Primary.TButton",  # 启动类（绿色）
    #                    foreground="white",
    #                    background="#2ecc71",
    #                    font=("微软雅黑", 10, "bold"),
    #                    padding=(15, 6),
    #                    borderwidth=0)
    #     style.map("Primary.TButton", background=[('active', '#27ae60')])
        
    #     style.configure("Secondary.TButton",  # 编辑/删除类（灰色）
    #                    foreground="#333333",
    #                    background="#e0e0e0",
    #                    font=("微软雅黑", 10),
    #                    padding=(12, 6),
    #                    borderwidth=0)
    #     style.map("Secondary.TButton", background=[('active', '#bdc3c7')])
        
    #     style.configure("Accent.TButton",  # 分组/搜索类（蓝色）
    #                    foreground="white",
    #                    background="#3498db",
    #                    font=("微软雅黑", 10),
    #                    padding=(12, 6),
    #                    borderwidth=0)
    #     style.map("Accent.TButton", background=[('active', '#2980b9')])
        
    #     # 4. 标签样式
    #     style.configure("Title.TLabel",
    #                    font=("微软雅黑", 16, "bold"),
    #                    foreground="#2c3e50",
    #                    padding=(0, 5))
        
    #     style.configure("Status.TLabel",
    #                    font=("微软雅黑", 9),
    #                    foreground="#7f8c8d",
    #                    background="#ecf0f1",
    #                    padding=(5, 3))

    def apply_styles(self):
        """应用现代化样式（移除状态映射，确保Primary.TButton显示）"""
        style = ttk.Style()
        
        # 1. 修复Primary.TButton（仅保留基础样式，无状态映射）
        style.configure("Primary.TButton",
                    foreground="#333333",       
                    background="#e0e0e0",     # 背景绿色（启动类按钮）
                    font=("微软雅黑", 10, "bold"),  # 字体加粗
                    padding=(15, 6),          # 上下内边距6，左右15（按钮更饱满）
                    borderwidth=1,            # 保留1px边框（避免无边框导致不显示）
                    relief="solid")           # 实心边框（确保按钮轮廓可见）
        
        # 2. Secondary.TButton（编辑/删除类，同样移除状态映射）
        style.configure("Secondary.TButton",
                    foreground="#333333",     # 文字深灰
                    background="#e0e0e0",     # 背景浅灰
                    font=("微软雅黑", 10),
                    padding=(12, 6),
                    borderwidth=1,
                    relief="solid")
        
        # 3. Treeview基础样式（保持不变，确保表格正常）
        style.configure("Treeview", 
                    background="white",
                    foreground="#333333",
                    rowheight=32,
                    fieldbackground="white",
                    borderwidth=0,
                    font=("微软雅黑", 9))
        
        # Treeview交替行颜色（仅基础配置，无状态映射）
        style.map("Treeview",
                background=[('selected', '#3498db'), ('alternate', '#f8f9fa')],
                foreground=[('selected', 'white')])
        
        # 4. Treeview表头样式
        style.configure("Treeview.Heading",
                    background="#2c3e50",
                    foreground="white",
                    font=("微软雅黑", 10, "bold"),
                    padding=(12, 0),
                    relief="flat")
        
        # 5. 标签样式（标题+状态栏）
        style.configure("Title.TLabel",
                    font=("微软雅黑", 16, "bold"),
                    foreground="#2c3e50",
                    padding=(0, 5))
        
        style.configure("Status.TLabel",
                    font=("微软雅黑", 9),
                    foreground="#7f8c8d",
                    background="#ecf0f1",
                    padding=(5, 3))
        



    def create_menu(self):
        """创建菜单栏"""
        menubar = Menu(self.root, font=("微软雅黑", 10))
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = Menu(menubar, tearoff=0, font=("微软雅黑", 9))
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导入配置", command=self.import_config)
        file_menu.add_command(label="导出配置", command=self.export_config)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 编辑菜单
        edit_menu = Menu(menubar, tearoff=0, font=("微软雅黑", 9))
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="编辑选中项", command=self.edit_selected)
        edit_menu.add_command(label="全选", command=self.select_all)
        edit_menu.add_command(label="取消选择", command=self.deselect_all)
        
        # 帮助菜单
        help_menu = Menu(menubar, tearoff=0, font=("微软雅黑", 9))
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)

    def create_widgets(self):
        """创建界面组件"""
        # 1. 标题区域
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=25, pady=(20, 10))
        ttk.Label(title_frame, text="软件批量启动管理器", style="Title.TLabel").pack(side=tk.LEFT)
        
        # 2. 分组筛选+搜索区域
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(fill=tk.X, padx=25, pady=(0, 10))
        
        # 分组下拉框
        ttk.Label(filter_frame, text="分组筛选：", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=(0, 10))
        self.group_var = tk.StringVar(value=self.current_group)
        self.group_combobox = ttk.Combobox(filter_frame, textvariable=self.group_var, state="readonly", font=("微软雅黑", 10))
        self.update_group_combobox()  # 加载分组选项
        self.group_combobox.pack(side=tk.LEFT, padx=(0, 15))
        self.group_combobox.bind("<<ComboboxSelected>>", self.on_group_change)
        
        # 搜索框（带清除按钮）
        search_inner_frame = ttk.Frame(filter_frame)
        search_inner_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_inner_frame, text="搜索：", font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        self.search_entry = ttk.Entry(search_inner_frame, textvariable=self.search_var, font=("微软雅黑", 10))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        
        # 搜索清除按钮
        self.clear_btn = ttk.Button(search_inner_frame, text="×", width=3, command=self.clear_search, style="Secondary.TButton")
        self.clear_btn.pack(side=tk.RIGHT)
        self.clear_btn.pack_forget()  # 初始隐藏
        self.search_var.trace('w', self.toggle_clear_btn)
        
        # 3. 功能按钮区域
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=25, pady=(0, 10))
        
        ttk.Button(btn_frame, text="添加软件", command=self.add_software, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑选中", command=self.edit_selected, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除选中", command=self.delete_software, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="启动当前分组", command=self.start_current_group_threaded, style="Secondary.TButton").pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="启动选中", command=self.start_selected_threaded, style="Secondary.TButton").pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="全部启动", command=self.start_all_threaded, style="Secondary.TButton").pack(side=tk.RIGHT, padx=5)
        
        # 4. 进度条（启动时显示）
        self.progress_frame = ttk.Frame(self.root)
        self.progress_frame.pack(fill=tk.X, padx=25, pady=(0, 5))
        self.progress_frame.pack_forget()  # 初始隐藏
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, expand=True, ipady=4)
        
        # 5. 软件列表表格（带滚动条）
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 10))
        
        # 滚动条
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # 表格列定义（新增分组列）
        columns = ("name", "group", "path", "delay", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 滚动条绑定
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # 列配置（宽度+对齐）
        self.tree.heading("name", text="软件名称", anchor=tk.W)
        self.tree.heading("group", text="所属分组", anchor=tk.CENTER)
        self.tree.heading("path", text="文件路径", anchor=tk.W)
        self.tree.heading("delay", text="启动延迟(秒)", anchor=tk.CENTER)
        self.tree.heading("status", text="状态", anchor=tk.CENTER)
        
        self.tree.column("name", width=180, minwidth=150)
        self.tree.column("group", width=120, minwidth=100)
        self.tree.column("path", width=350, minwidth=300)
        self.tree.column("delay", width=120, minwidth=100)
        self.tree.column("status", width=100, minwidth=80)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # 事件绑定
        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # 6. 状态栏
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=25, pady=(0, 20))
        
        self.status_var = tk.StringVar(value="就绪 | 点击「添加软件」开始配置")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style="Status.TLabel")
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, anchor=tk.W)
        
        self.count_var = tk.StringVar()
        count_label = ttk.Label(status_frame, textvariable=self.count_var, style="Status.TLabel")
        count_label.pack(side=tk.RIGHT, anchor=tk.E)
        
        # 初始化表格和计数
        self.refresh_tree()
        self.update_count_label()

    # ------------------------------
    # 基础交互逻辑
    # ------------------------------
    def toggle_clear_btn(self, *args):
        """控制搜索清除按钮显示/隐藏"""
        self.clear_btn.pack(side=tk.RIGHT) if self.search_var.get() else self.clear_btn.pack_forget()

    def clear_search(self):
        """清除搜索内容"""
        self.search_var.set("")

    def on_group_change(self, event):
        """分组筛选变更"""
        self.current_group = self.group_var.get()
        self.refresh_tree()

    def on_search_change(self, *args):
        """搜索内容变更"""
        self.refresh_tree()

    def update_group_combobox(self):
        """更新分组下拉框选项"""
        groups = {"所有分组"}  # 默认包含"所有分组"
        for software in self.software_list:
            groups.add(software["group"])
        self.group_combobox['values'] = sorted(groups)

    def on_tree_click(self, event):
        """表格点击事件（切换选中状态）"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            if item:
                software_id = self.tree.item(item, "tags")[0] if self.tree.item(item, "tags") else None
                if software_id:
                    # 切换选中状态
                    if software_id in self.selected_items:
                        self.selected_items.remove(software_id)
                    else:
                        self.selected_items.add(software_id)
                    self.refresh_tree()

    def on_double_click(self, event):
        """表格双击事件（编辑选中项）"""
        item = self.tree.identify_row(event.y)
        if item:
            self.edit_selected()

    # ------------------------------
    # 表格数据刷新
    # ------------------------------
    def refresh_tree(self):
        """刷新表格数据（含分组+搜索筛选）"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 筛选条件
        search_term = self.search_var.get().lower()
        filtered_softwares = []
        
        for software in self.software_list:
            # 分组筛选
            if self.current_group != "所有分组" and software["group"] != self.current_group:
                continue
            # 搜索筛选（名称/路径/分组）
            if search_term and not (
                search_term in software["name"].lower() or
                search_term in software["path"].lower() or
                search_term in software["group"].lower()
            ):
                continue
            filtered_softwares.append(software)
        
        # 插入筛选后的数据
        for idx, software in enumerate(filtered_softwares):
            # 状态图标化（运行中=绿色对勾，未运行=灰色圆圈）
            if self.is_running(software["path"]):
                status = "✅"
                status_tag = "status_running"
            else:
                status = "○"
                status_tag = "status_stopped"
            
            # 插入行（tags存储软件ID）
            item_id = self.tree.insert(
                "", tk.END,
                values=(software["name"], software["group"], software["path"], software["delay"], status),
                tags=(software["id"], status_tag)
            )
            
            # 设置选中状态
            if software["id"] in self.selected_items:
                self.tree.selection_add(item_id)
        
        # 配置状态标签颜色
        self.tree.tag_configure("status_running", foreground="#2ecc71", font=("Arial", 12))
        self.tree.tag_configure("status_stopped", foreground="#95a5a6", font=("Arial", 12))
        
        # 更新计数和分组下拉框
        self.update_count_label(len(self.software_list), len(filtered_softwares))
        self.update_group_combobox()

    def update_count_label(self, total_count=None, visible_count=None):
        """更新计数标签"""
        if total_count is None:
            total_count = len(self.software_list)
        if visible_count is None:
            visible_count = len(self.tree.get_children())
        self.count_var.set(f"总计: {total_count} | 显示: {visible_count} | 选中: {len(self.selected_items)}")

    # ------------------------------
    # 软件管理（添加/编辑/删除）
    # ------------------------------
    def add_software(self):
        """添加新软件"""
        # 选择可执行文件
        file_path = filedialog.askopenfilename(
            title="选择软件可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")],
            initialdir="C:/Program Files"
        )
        if not file_path:
            return

        # 弹出编辑对话框（复用编辑逻辑）
        default_name = os.path.basename(file_path).split(".")[0]
        default_group = "默认分组"
        dialog = EditDialog(self.root, {
            "name": default_name,
            "path": file_path,
            "delay": 2,
            "group": default_group
        }, is_new=True)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            # 生成唯一ID
            new_software = {
                "id": str(uuid.uuid4()),
                "name": dialog.result["name"],
                "path": dialog.result["path"],
                "delay": dialog.result["delay"],
                "group": dialog.result["group"]
            }
            self.software_list.append(new_software)
            self.selected_items.clear()  # 清空选中
            self.refresh_tree()
            self.save_config()
            self.update_status(f"已添加软件：{new_software['name']}（{new_software['group']}）")

    def edit_selected(self):
        """编辑选中软件"""
        if len(self.selected_items) != 1:
            messagebox.showinfo("提示", "请选择1个软件进行编辑")
            return

        # 获取选中软件信息
        software_id = next(iter(self.selected_items))
        software = next((s for s in self.software_list if s["id"] == software_id), None)
        if not software:
            messagebox.showerror("错误", "选中的软件不存在")
            self.selected_items.clear()
            self.refresh_tree()
            return

        # 弹出编辑对话框
        dialog = EditDialog(self.root, software.copy(), is_new=False)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            # 更新软件信息
            for key in ["name", "path", "delay", "group"]:
                software[key] = dialog.result[key]
            self.refresh_tree()
            self.save_config()
            self.update_status(f"已更新软件：{software['name']}")

    def delete_software(self):
        """删除选中软件"""
        if not self.selected_items:
            messagebox.showinfo("提示", "请先选择要删除的软件")
            return

        # 确认删除
        count = len(self.selected_items)
        if not messagebox.askyesno("确认删除", f"确定要删除选中的 {count} 个软件吗？\n删除后不可恢复！"):
            return

        # 收集要删除的软件名称
        deleted_names = []
        for software in self.software_list:
            if software["id"] in self.selected_items:
                deleted_names.append(software["name"])

        # 按ID删除
        self.software_list = [
            s for s in self.software_list
            if s["id"] not in self.selected_items
        ]
        
        # 重置选中状态
        self.selected_items.clear()
        self.refresh_tree()
        self.save_config()
        self.update_status(f"已删除 {count} 个软件：{', '.join(deleted_names[:3])}{'...' if count>3 else ''}")

    # ------------------------------
    # 软件启动（线程安全）
    # ------------------------------
    def update_status(self, msg):
        """线程安全的状态更新方法"""
        self.status_var.set(msg)
        self.update_count_label()  # 同步更新计数

    def update_progress(self, value):
        """线程安全的进度条更新方法"""
        self.progress_var.set(value)

    def show_progress(self, show=True):
        """显示/隐藏进度条"""
        if show:
            self.progress_frame.pack(fill=tk.X, padx=25, pady=(0, 5))
            self.update_progress(0)
        else:
            self.progress_frame.pack_forget()
            self.update_progress(0)

    def start_selected_threaded(self):
        """线程启动选中软件（避免界面冻结）"""
        if not self.selected_items:
            messagebox.showinfo("提示", "请先选择要启动的软件")
            return
        thread = threading.Thread(target=self.start_software_batch, args=(list(self.selected_items),))
        thread.daemon = True
        thread.start()

    def start_all_threaded(self):
        """线程启动所有软件"""
        if not self.software_list:
            messagebox.showinfo("提示", "暂无软件可启动")
            return
        software_ids = [s["id"] for s in self.software_list]
        thread = threading.Thread(target=self.start_software_batch, args=(software_ids,))
        thread.daemon = True
        thread.start()

    def start_current_group_threaded(self):
        """线程启动当前分组软件"""
        group_softwares = [s for s in self.software_list if s["group"] == self.current_group]
        if not group_softwares:
            messagebox.showinfo("提示", f"当前分组「{self.current_group}」无软件")
            return
        software_ids = [s["id"] for s in group_softwares]
        thread = threading.Thread(target=self.start_software_batch, args=(software_ids,))
        thread.daemon = True
        thread.start()

    def start_software_batch(self, software_ids):
        """批量启动软件（核心逻辑）"""
        # 准备启动列表
        batch_list = [s for s in self.software_list if s["id"] in software_ids]
        total = len(batch_list)
        success = 0
        
        # 显示进度条和初始状态
        self.root.after(0, self.show_progress, True)
        self.root.after(0, self.update_status, f"开始启动 {total} 个软件...")
        time.sleep(0.5)

        # 逐个启动
        for idx, software in enumerate(batch_list, 1):
            name = software["name"]
            path = software["path"]
            delay = software["delay"]
            progress = (idx / total) * 100

            # 1. 检查是否已运行
            if self.is_running(path):
                self.root.after(0, self.update_status, f"[{idx}/{total}] {name} 已在运行，跳过")
                self.root.after(0, self.update_progress, progress)
                time.sleep(0.8)
                continue

            # 2. 尝试启动软件
            self.root.after(0, self.update_status, f"[{idx}/{total}] 正在启动：{name}")
            self.root.after(0, self.update_progress, progress)
            
            if self.start_software(path):
                success += 1
                self.root.after(0, self.update_status, f"[{idx}/{total}] 启动成功：{name}，等待 {delay} 秒")
                time.sleep(delay)  # 按设置延迟启动下一个
            else:
                self.root.after(0, self.update_status, f"[{idx}/{total}] 启动失败：{name}")
                time.sleep(1.5)

        # 启动完成清理
        final_msg = f"启动完成！成功：{success}/{total} | 失败：{total-success}"
        self.root.after(0, self.update_status, final_msg)
        self.root.after(0, self.update_progress, 100)
        time.sleep(1)
        self.root.after(0, self.show_progress, False)
        self.root.after(0, self.refresh_tree)  # 刷新状态
        messagebox.showinfo("启动结果", final_msg)

    def is_running(self, path):
        """检查软件是否已运行（通过进程名匹配）"""
        try:
            process_name = os.path.basename(path).lower()
            for proc in psutil.process_iter(["name"]):
                if proc.info.get("name", "").lower() == process_name:
                    return True
            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def start_software(self, path):
        """启动单个软件（跨平台支持）"""
        try:
            if os.name == "nt":  # Windows
                os.startfile(path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", path], check=True, capture_output=True)
            else:  # Linux
                subprocess.run(["xdg-open", path], check=True, capture_output=True)
            return True
        except Exception as e:
            self.root.after(0, messagebox.showerror, "启动失败", f"{os.path.basename(path)}\n错误：{str(e)[:100]}")
            return False

    # ------------------------------
    # 配置管理（导入/导出/加载/保存）
    # ------------------------------
    def save_config(self):
        """保存配置到文件"""
        try:
            # 确保使用UTF-8编码并正确处理中文字符
            with open(self.config_path, "w", encoding="utf-8") as f:
                # 仅保存必要字段（排除临时状态）
                save_list = [{k: s[k] for k in ["id", "name", "path", "delay", "group"]} for s in self.software_list]
                json.dump(save_list, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("保存失败", f"无法写入配置文件：{str(e)}")
            return False

    def load_config(self):
        """从文件加载配置"""
        try:
            if os.path.exists(self.config_path):
                # 确保使用UTF-8编码并正确处理中文字符和BOM
                with open(self.config_path, "r", encoding="utf-8-sig") as f:
                    loaded_list = json.load(f)
                # 校验配置格式（补全缺失字段）
                self.software_list = []
                for item in loaded_list:
                    # 基础字段校验
                    if not all(k in item for k in ["name", "path", "delay"]):
                        print(f"跳过无效配置项：{item}")
                        continue
                    # 补全缺失字段
                    software = {
                        "id": item.get("id", str(uuid.uuid4())),  # 无ID则生成
                        "name": item["name"],
                        "path": item["path"],
                        "delay": max(0, int(item["delay"])),  # 延迟不小于0
                        "group": item.get("group", "默认分组")  # 无分组则默认
                    }
                    self.software_list.append(software)
                self.update_status(f"成功加载 {len(self.software_list)} 个软件配置")
            else:
                self.update_status("首次使用，暂无配置文件")
        except Exception as e:
            messagebox.showerror("加载失败", f"配置文件损坏：{str(e)}\n将使用空配置")
            self.software_list = []

    def import_config(self):
        """导入外部配置"""
        file_path = filedialog.askopenfilename(
            title="选择配置文件",
            filetypes=[("JSON配置", "*.json"), ("所有文件", "*.*")]
        )
        if not file_path:
            return

        try:
            # 确保使用UTF-8编码并正确处理中文字符和BOM
            with open(file_path, "r", encoding="utf-8-sig") as f:
                imported_list = json.load(f)
            
            # 校验并处理导入数据
            valid_list = []
            for item in imported_list:
                if not all(k in item for k in ["name", "path", "delay"]):
                    continue
                valid_list.append({
                    "id": str(uuid.uuid4()),  # 重新生成ID避免冲突
                    "name": item["name"],
                    "path": item["path"],
                    "delay": max(0, int(item["delay"])),
                    "group": item.get("group", "导入分组")
                })
            
            if not valid_list:
                messagebox.showerror("导入失败", "配置文件中无有效软件信息")
                return
            
            # 合并配置（询问是否覆盖）
            if self.software_list and not messagebox.askyesno("导入确认", f"当前已有 {len(self.software_list)} 个软件，是否覆盖？\n（选择「否」将追加到现有配置）"):
                self.software_list.extend(valid_list)
            else:
                self.software_list = valid_list
            
            # 刷新界面并保存
            self.selected_items.clear()
            self.refresh_tree()
            self.save_config()
            self.update_status(f"成功导入 {len(valid_list)} 个软件配置")
        except Exception as e:
            messagebox.showerror("导入失败", f"配置文件解析错误：{str(e)}")

    def export_config(self):
        """导出当前配置"""
        if not self.software_list:
            messagebox.showinfo("提示", "暂无软件配置可导出")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存配置文件",
            defaultextension=".json",
            filetypes=[("JSON配置", "*.json"), ("所有文件", "*.*")],
            initialfile=f"launcher_config_{len(self.software_list)}.json"
        )
        if not file_path:
            return

        try:
            # 确保使用UTF-8编码并正确处理中文字符
            with open(file_path, "w", encoding="utf-8") as f:
                export_list = [{k: s[k] for k in ["name", "path", "delay", "group"]} for s in self.software_list]
                json.dump(export_list, f, ensure_ascii=False, indent=2)
            self.update_status(f"配置已导出到：{os.path.basename(file_path)}")
            messagebox.showinfo("导出成功", f"共导出 {len(self.software_list)} 个软件配置\n路径：{file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"无法写入文件：{str(e)}")

    # ------------------------------
    # 辅助功能
    # ------------------------------
    def select_all(self):
        """全选当前显示的软件"""
        visible_ids = [self.tree.item(item, "tags")[0] for item in self.tree.get_children()]
        self.selected_items = set(visible_ids)
        self.refresh_tree()

    def deselect_all(self):
        """取消所有选择"""
        self.selected_items.clear()
        self.refresh_tree()

    def show_about(self):
        """显示关于对话框"""
        about_text = """现代软件启动器 v2.1
一款高效的批量软件启动工具

核心功能：
• 软件分组管理（按场景分类）
• 启动前自动检查运行状态
• 自定义启动延迟（避免卡顿）
• 配置导入/导出（数据备份）
• 实时状态显示+进度跟踪

使用说明：
1. 点击「添加软件」选择.exe文件
2. 可按分组或关键词筛选软件
3. 选中软件后点击「启动选中」即可批量启动

© 2025 高效工具集"""
        messagebox.showinfo("关于", about_text)


class EditDialog:
    """软件编辑对话框（新增/编辑通用）"""
    def __init__(self, parent, software_data, is_new=True):
        self.parent = parent
        self.software_data = software_data
        self.is_new = is_new  # 是否为新增（True=新增，False=编辑）
        self.result = None  # 存储编辑结果
        
        # 创建对话框
        self.top = Toplevel(parent)
        self.top.title("添加软件" if is_new else "编辑软件")
        self.top.geometry("600x400")
        self.top.resizable(False, False)
        self.top.transient(parent)  # 依附于父窗口
        self.top.grab_set()  # 独占焦点
        
        # 居中显示
        self.center_dialog()
        
        # 创建界面组件
        self.create_widgets()

    def center_dialog(self):
        """对话框居中"""
        self.top.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_w = self.parent.winfo_width()
        parent_h = self.parent.winfo_height()
        
        dialog_w = self.top.winfo_width()
        dialog_h = self.top.winfo_height()
        
        x = parent_x + (parent_w // 2) - (dialog_w // 2)
        y = parent_y + (parent_h // 2) - (dialog_h // 2)
        self.top.geometry(f"+{x}+{y}")

    def create_widgets(self):
        """创建对话框组件"""
        # 基础样式
        label_font = ("微软雅黑", 11)
        entry_font = ("微软雅黑", 10)
        pad_y = 8
        
        # 1. 软件名称
        name_frame = ttk.Frame(self.top, padding=(20, pad_y, 20, 0))
        name_frame.pack(fill=tk.X)
        
        ttk.Label(name_frame, text="软件名称 *", font=label_font, foreground="#2c3e50").pack(anchor=tk.W)
        self.name_var = tk.StringVar(value=self.software_data["name"])
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, font=entry_font)
        name_entry.pack(fill=tk.X, pady=(5, 0), ipady=4)
        name_entry.focus_set()  # 默认焦点
        
        # 2. 所属分组
        group_frame = ttk.Frame(self.top, padding=(20, pad_y, 20, 0))
        group_frame.pack(fill=tk.X)
        
        ttk.Label(group_frame, text="所属分组 *", font=label_font, foreground="#2c3e50").pack(anchor=tk.W)
        self.group_var = tk.StringVar(value=self.software_data["group"])
        group_entry = ttk.Entry(group_frame, textvariable=self.group_var, font=entry_font)
        group_entry.pack(fill=tk.X, pady=(5, 0), ipady=4)
        
        # 3. 软件路径
        path_frame = ttk.Frame(self.top, padding=(20, pad_y, 20, 0))
        path_frame.pack(fill=tk.X)
        
        ttk.Label(path_frame, text="软件路径 *", font=label_font, foreground="#2c3e50").pack(anchor=tk.W)
        path_inner_frame = ttk.Frame(path_frame)
        path_inner_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.path_var = tk.StringVar(value=self.software_data["path"])
        path_entry = ttk.Entry(path_inner_frame, textvariable=self.path_var, font=entry_font, state="readonly" if not self.is_new else "normal")
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        
        # 浏览按钮（新增可修改路径，编辑不可修改）
        if self.is_new:
            ttk.Button(path_inner_frame, text="浏览", command=self.browse_path, style="Secondary.TButton", width=8).pack(side=tk.RIGHT, padx=(5, 0))
        
        # 4. 启动延迟
        delay_frame = ttk.Frame(self.top, padding=(20, pad_y, 20, 0))
        delay_frame.pack(fill=tk.X)
        
        ttk.Label(delay_frame, text="启动延迟(秒) *", font=label_font, foreground="#2c3e50").pack(anchor=tk.W)
        delay_inner_frame = ttk.Frame(delay_frame)
        delay_inner_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.delay_var = tk.StringVar(value=str(self.software_data["delay"]))
        delay_spin = ttk.Spinbox(
            delay_inner_frame,
            from_=0, to=60,
            textvariable=self.delay_var,
            font=entry_font,
            width=10,
            state="readonly"
        )
        delay_spin.pack(side=tk.LEFT, ipady=4)
        ttk.Label(delay_inner_frame, text="  建议：轻量软件1-2秒，大型软件5-10秒", font=("微软雅黑", 9), foreground="#7f8c8d").pack(side=tk.LEFT, padx=10)
        
        # 5. 按钮区域
        btn_frame = ttk.Frame(self.top, padding=(20, pad_y*2, 20, 0))
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="取消", command=self.cancel, style="Secondary.TButton").pack(side=tk.RIGHT, padx=(0, 10))
        ttk.Button(btn_frame, text="确定", command=self.ok, style="Primary.TButton").pack(side=tk.RIGHT)

    def browse_path(self):
        """浏览软件路径"""
        file_path = filedialog.askopenfilename(
            title="选择软件可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")],
            initialdir="C:/Program Files"
        )
        if file_path:
            self.path_var.set(file_path)
            # 自动填充名称（如果名称为空）
            if not self.name_var.get():
                self.name_var.set(os.path.basename(file_path).split(".")[0])

    def ok(self):
        """确定按钮逻辑"""
        # 数据校验
        name = self.name_var.get().strip()
        group = self.group_var.get().strip()
        path = self.path_var.get().strip()
        
        try:
            delay = int(self.delay_var.get().strip())
        except ValueError:
            messagebox.showerror("错误", "启动延迟必须是数字")
            return
        
        # 基础校验
        if not name:
            messagebox.showerror("错误", "软件名称不能为空")
            return
        if not group:
            messagebox.showerror("错误", "所属分组不能为空")
            return
        if not path:
            messagebox.showerror("错误", "软件路径不能为空")
            return
        if not os.path.exists(path) and self.is_new:
            if not messagebox.askyesno("警告", "指定的路径不存在，是否继续？"):
                return
        
        # 存储结果并关闭对话框
        self.result = {
            "name": name,
            "group": group,
            "path": path,
            "delay": delay
        }
        self.top.destroy()

    def cancel(self):
        """取消按钮逻辑"""
        self.result = None
        self.top.destroy()


if __name__ == "__main__":
    # 检查并安装依赖
    try:
        import psutil
    except ImportError:
        print("正在安装依赖模块 psutil...")
        subprocess.run([sys.executable, "-m", "pip", "install", "psutil", "--upgrade"], 
                      check=True, capture_output=True, text=True)
        import psutil

    # 启动应用
    root = tk.Tk()
    app = ModernSoftwareLauncher(root)
    root.mainloop()