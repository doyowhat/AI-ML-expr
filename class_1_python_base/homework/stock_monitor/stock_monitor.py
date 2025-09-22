import requests
import time
import json
from colorama import Fore, Style, init
import sys
import argparse

# 初始化colorama，支持Windows系统
init(autoreset=True)

class StockTracker:
    def __init__(self, stock_code, refresh_interval=None):
        self.last_price = None
        self.stock_code = stock_code
        self.refresh_interval = refresh_interval if refresh_interval else 5  # 默认5秒刷新一次
    
    def get_stock_price(self):
        """从新浪财经API获取股票价格"""
        try:
            # 新浪财经API接口，需要将股票代码转换为其格式
            # 沪市股票代码以6开头，格式为sh6xxxxxx
            # 深市股票代码以0或3开头，格式为sz0xxxxxx或sz3xxxxxx
            if self.stock_code.startswith('6'):
                api_code = f"sh{self.stock_code}"
            else:
                api_code = f"sz{self.stock_code}"
                
            url = f"http://hq.sinajs.cn/list={api_code}"
            response = requests.get(url, timeout=10)
            response.encoding = 'gbk'
            
            # 解析返回结果
            if response.status_code == 200:
                data = response.text.split('=')[1].strip('";\n')
                data_list = data.split(',')
                
                if len(data_list) > 3:
                    # 股票名称
                    name = data_list[0]
                    # 当前价格
                    price = float(data_list[3])
                    # 涨跌幅
                    change_percent = float(data_list[31])
                    return {
                        'name': name,
                        'price': price,
                        'change_percent': change_percent
                    }
                else:
                    print("无法解析股票数据，请检查股票代码是否正确")
                    return None
            else:
                print(f"获取数据失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取股票数据时出错: {str(e)}")
            return None
    
    def display_price(self, stock_data):
        """显示股票价格和走势"""
        if not stock_data:
            return
            
        current_price = stock_data['price']
        name = stock_data['name']
        change_percent = stock_data['change_percent']
        
        # 确定箭头和颜色
        if self.last_price is None:
            arrow = " "
            color = Style.NORMAL
        elif current_price > self.last_price:
            arrow = "↑"
            color = Fore.GREEN
        elif current_price < self.last_price:
            arrow = "↓"
            color = Fore.RED
        else:
            arrow = "→"
            color = Style.NORMAL
        
        # 更新最后价格
        self.last_price = current_price
        
        # 清除当前行并显示新数据
        sys.stdout.write("\r")
        sys.stdout.flush()
        
        # 格式化输出
        time_str = time.strftime("%H:%M:%S")
        print(f"{time_str} {name}({self.stock_code}): {color}{current_price:.2f} {arrow} {change_percent:+.2f}%{Style.RESET_ALL}", end="")
    
    def run(self):
        """运行股价跟踪器"""
        print("A股实时股价查询工具")
        print("-------------------")
        print(f"正在监控股票: {self.stock_code}")
        print(f"刷新间隔: {self.refresh_interval}秒")
        
        print("\n正在获取数据... (按Ctrl+C停止)")
        
        try:
            while True:
                stock_data = self.get_stock_price()
                if stock_data:
                    self.display_price(stock_data)
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            print("\n程序已停止")

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='A股实时股价查询工具')
    parser.add_argument('stock_code', help='股票代码，例如：600519（贵州茅台）、300750（宁德时代）')
    parser.add_argument('-i', '--interval', type=int, help=f'刷新间隔时间（秒），默认5秒')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 创建并运行跟踪器
    tracker = StockTracker(args.stock_code, args.interval)
    tracker.run()

# python stock_tracker_cli.py 600519 -i 10