def count_letters(filename):
    # 初始化一个字典来存储每个字母的计数
    letter_count = {}
    try:
        # 打开文件并读取内容
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
            
            # 遍历文本中的每个字符
            for char in text:
                # 只处理字母字符（区分大小写）
                if ('a' <= char <= 'z') or ('A' <= char <= 'Z'):
                    # 更新字典中的计数
                    letter_count[char] = letter_count.get(char, 0) + 1
                    
        # 按字母顺序排序结果
        sorted_letters = sorted(letter_count.items())
        
        # 打印统计结果
        print(f"字母出现频率统计（文件: {filename}）:")
        for letter, count in sorted_letters:
            print(f"'{letter}': {count}")
            
        return letter_count
        
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    file_path = "./data/letter_frequancy.txt"
    count_letters(file_path)