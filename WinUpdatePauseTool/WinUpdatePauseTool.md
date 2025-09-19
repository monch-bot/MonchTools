# 🛠 Windows 更新暂停助手

一个轻量级的小工具，支持一键将 Windows 更新暂停 **10 年 / 20 年 / 自定义年数**，也可快速恢复。  
采用 PowerShell + WPF 编写，并可打包为独立 EXE 运行。  

> 💡 本工具的初衷：解决 Windows 强制更新带来的困扰，让用户拥有更多的自主选择权。

---

## ✨ 功能特性
- 一键暂停 Windows 更新 **10 年 / 20 年 / 自定义年限**  
- 一键恢复（撤销暂停）  
- 托盘常驻，支持最小化到托盘  
- 自带美观的 WPF 界面（圆角按钮、卡片阴影）  
 

---

## 📦 使用方法
1. **下载工具**：  
   - 直接下载（推荐）：[点击此处下载 WinUpdatePauseTool.exe](https://raw.githubusercontent.com/monch-bot/MonchTools/main/WinUpdatePauseTool/WinUpdatePauseTool.exe)  
   - 备用方式：访问 [文件预览页](https://github.com/monch-bot/MonchTools/blob/main/WinUpdatePauseTool/WinUpdatePauseTool.exe)，点击页面右上角的 **↓ Download** 按钮保存文件。  
2. **环境要求**：确保系统已安装 **PowerShell 5.1+**（Windows 10/11 默认自带，无需额外安装）。  
3. **运行工具**：双击下载后的 `WinUpdatePauseTool.exe`，按提示操作即可（首次运行可能需要允许管理员权限）。



## 🔧 注意事项
- 本工具仅暂停 Windows 更新，不影响其他系统服务或功能。  
- 暂停更新后，系统将不再检查和安装新的 Windows 更新。  
- 若需恢复更新，请使用工具内的恢复按钮或手动修改注册表。  
