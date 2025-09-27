import re
import sys
from collections import defaultdict
from operator import itemgetter

def count_word_frequency(file_path):
    """
    统计文件中各单词的出现频率（区分大小写）
    
    参数:
        file_path: 要处理的文件路径
        
    返回:
        按频率降序排列的单词频率列表
    """
    # 初始化单词计数器
    word_count = defaultdict(int)
    
    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            # 逐行读取文件
            for line in file:
                # 使用正则表达式分割单词（保留大小写）
                words = re.findall(r'\b\w+\b', line)
                
                # 统计每个单词的出现次数
                for word in words:
                    word_count[word] += 1
                    
        # 按频率降序排序
        sorted_words = sorted(word_count.items(), key=itemgetter(1), reverse=True)
        
        return sorted_words
        
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 未找到")
        return []
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return []

def print_word_frequency(word_freq):
    """
    打印单词频率统计结果
    
    参数:
        word_freq: 单词频率列表
    """
    if not word_freq:
        print("没有找到任何单词")
        return
        
    # 计算最大单词长度用于对齐输出
    max_word_len = max(len(word) for word, _ in word_freq)
    
    # 打印表头
    print(f"{'单词':<{max_word_len}} | 频率")
    print("-" * (max_word_len + 10))
    
    # 打印每个单词及其频率
    for word, count in word_freq:
        print(f"{word:<{max_word_len}} | {count}")

def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python word_frequency.py <文件路径>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    # 统计单词频率
    word_freq = count_word_frequency(file_path)
    
    # 打印结果
    print_word_frequency(word_freq)

if __name__ == "__main__":
    main()