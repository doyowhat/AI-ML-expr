import os
import shutil
from pathlib import Path

def create_test_files():
    # 确保目标目录存在
    data_dir = Path("./data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"在目录 {data_dir.resolve()} 中创建测试文件...")
    
    # 创建基本测试文件
    for name in ["photo1.jpg", "pic02.jpg", "IMG_123.jpg", "DSC00045.jpg"]:
        create_empty_file(data_dir / name)
    
    # # 创建特殊字符测试文件
    # for name in ["my image.jpg", "file-with-dash.jpg", "photo_with_underscore.jpg", "file with spaces.jpg", "中文文件名.jpg"]:
    #     create_empty_file(data_dir / name)
    
    # # 创建混合类型文件
    # for name in ["file1.jpg", "document.pdf", "text.txt", "data.png"]:
    #     create_empty_file(data_dir / name)
    
    # # 创建边界情况测试文件
    # for name in [".jpg", "file without extension", "file.double.ext.jpg", "123456.jpg", "CAPS.JPG", "mixed.CASE.Jpg"]:
    #     create_empty_file(data_dir / name)
    
    print("所有测试文件已创建完毕！")

def create_empty_file(file_path):
    """创建一个空文件"""
    try:
        # 确保父目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建空文件
        with open(file_path, 'w') as f:
            pass
        
        print(f"已创建: {file_path}")
    except Exception as e:
        print(f"创建文件 {file_path} 失败: {str(e)}")

if __name__ == "__main__":
    create_test_files()