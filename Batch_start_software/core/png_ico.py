from PIL import Image

def png_to_ico_simple(png_path, ico_path, size=(64, 64)):
    """简化的PNG转ICO（单尺寸）"""
    try:
        # 打开PNG并转换为带透明通道的格式
        with Image.open(png_path).convert("RGBA") as img:
            # 调整图片尺寸并保存为ICO
            img.resize(size).save(ico_path, format="ICO")
        print(f"✅ 已生成ICO：{ico_path}（尺寸：{size[0]}x{size[1]}）")
    except Exception as e:
        print(f"❌ 转换失败：{str(e)}")

# 示例：替换为你的图片路径
if __name__ == "__main__":
    png_to_ico_simple(
        png_path=r"Batch_start_software\core\image.png",  # 你的绿色启动按钮PNG
        ico_path=r"Batch_start_software\core\app_icon.ico",          # 输出的ICO文件名
        size=(64, 64)                     # 可修改为(32,32)、(128,128)等
    )