import os
import re
import argparse
from datetime import datetime
from pathlib import Path

class BatchFileRenamer:
    def __init__(self):
        self.counter_map = {}  # 用于存储每种文件类型的计数器
    
    def parse_filter(self, filter_pattern):
        """
        解析过滤器模式，提取命名模式、数字位数和文件扩展名
        支持两种格式：
        1. name##.ext (如: myimage##.jpg)
        2. prefix-#*.ext (如: imgDate-#*.jpg)
        """
        # 检查第一种格式: name##.ext
        if '##' in filter_pattern:
            parts = filter_pattern.split('##')
            if len(parts) == 2:
                name_pattern = parts[0]
                extension = parts[1]
                num_digits = 3  # 默认3位数
                return name_pattern, num_digits, extension, False
        
        # 检查第二种格式: prefix-#*.ext
        match = re.match(r'(.+?)-(\#+)\.(.+)', filter_pattern)
        if match:
            name_pattern = match.group(1)
            num_digits = len(match.group(2))
            extension = match.group(3)
            return name_pattern, num_digits, extension, True
        
        # 如果没有匹配的格式，使用默认
        return filter_pattern, 3, "*", False
    
    def generate_new_filename(self, original_file, filter_pattern, file_type, count):
        """
        生成新的文件名
        """
        name_pattern, num_digits, extension, use_original = self.parse_filter(filter_pattern)
        
        # 处理日期格式
        if 'Date' in name_pattern:
            current_date = datetime.now().strftime("%Y%m%d")
            name_pattern = name_pattern.replace('Date', current_date)
        
        # 生成数字部分
        number_part = str(count).zfill(num_digits)
        
        # 获取原文件扩展名
        original_ext = os.path.splitext(original_file)[1]
        # 确定使用的扩展名
        final_extension = extension if extension != "*" else original_ext[1:]  # 去掉点
        
        # 生成新文件名
        if use_original:
            # 使用原文件名部分
            original_name = os.path.splitext(original_file)[0]
            # 正确处理扩展名 - 只在有扩展名时添加点
            if final_extension:
                new_name = f"{name_pattern}-{number_part}-{original_name}{final_extension}"
            else:
                new_name = f"{name_pattern}-{number_part}-{original_name}"
        else:
            # 正确处理扩展名 - 只在有扩展名时添加点
            if final_extension:
                new_name = f"{name_pattern}{number_part}{final_extension}"
            else:
                new_name = f"{name_pattern}{number_part}"
        
        return new_name
    
    def process_files(self, directory, filter_pattern, file_types=None):
        """
        批量处理文件重命名
        """
        if not os.path.exists(directory):
            print(f"错误：目录 '{directory}' 不存在")
            return False
        
        # 获取所有文件
        all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # 按文件类型分组
        file_groups = {}
        for file in all_files:
            ext = os.path.splitext(file)[1].lower()
            if file_types and ext[1:] not in file_types:  # 去掉点号
                continue
            
            if ext not in file_groups:
                file_groups[ext] = []
            file_groups[ext].append(file)
        
        # 对每组文件单独处理
        for ext, files in file_groups.items():
            # 初始化该类型的计数器
            if ext not in self.counter_map:
                self.counter_map[ext] = 1
            
            # 处理该类型的所有文件
            for file in files:
                new_name = self.generate_new_filename(
                    file, filter_pattern, ext, self.counter_map[ext]
                )
                
                # 重命名文件
                old_path = os.path.join(directory, file)
                new_path = os.path.join(directory, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"重命名: {file} -> {new_name}")
                    self.counter_map[ext] += 1
                except Exception as e:
                    print(f"重命名 {file} 失败: {str(e)}")
        
        return True

def main():
    parser = argparse.ArgumentParser(description="文件批量重命名工具")
    parser.add_argument("directory", help="要处理的目录路径")
    parser.add_argument("filter_pattern", help="文件名过滤器模式，如: myimage##.jpg 或 imgDate-#*.jpg")
    parser.add_argument("--types", nargs="+", help="只处理指定扩展名的文件(如: jpg png pdf)", default=None)
    
    args = parser.parse_args()
    
    renamer = BatchFileRenamer()
    success = renamer.process_files(args.directory, args.filter_pattern, args.types)
    
    if success:
        print("文件重命名完成！")
    else:
        print("文件重命名失败！")

if __name__ == "__main__":
    main()