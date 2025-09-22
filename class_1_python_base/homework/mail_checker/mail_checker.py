import imaplib
import poplib
import email
import time
import argparse
from email.header import decode_header
from datetime import datetime

class MailChecker:
    def __init__(self, server, port, protocol, username, password, interval=300):
        """
        初始化邮件检查器
        
        参数:
            server: 邮件服务器地址
            port: 邮件服务器端口
            protocol: 协议类型 (POP3 或 IMAP)
            username: 邮箱用户名
            password: 邮箱密码
            interval: 检查间隔（秒），默认5分钟
        """
        self.server = server
        self.port = port
        self.protocol = protocol.upper()
        self.username = username
        self.password = password
        self.interval = interval
        self.last_check = None
        self.last_email_ids = set()
        
        # 验证协议类型
        if self.protocol not in ["POP3", "IMAP"]:
            raise ValueError("不支持的协议类型，请使用 POP3 或 IMAP")
    
    def connect(self):
        """连接到邮件服务器"""
        try:
            if self.protocol == "IMAP":
                # 使用SSL连接
                mail = imaplib.IMAP4_SSL(self.server, self.port)
                mail.login(self.username, self.password)
                mail.select("inbox")
                return mail
            else:  # POP3
                mail = poplib.POP3_SSL(self.server, self.port)
                mail.user(self.username)
                mail.pass_(self.password)
                return mail
        except Exception as e:
            print(f"连接失败: {str(e)}")
            return None
    
    def decode_subject(self, subject):
        """解码邮件主题"""
        decoded = decode_header(subject)
        subject_parts = []
        for part, encoding in decoded:
            if isinstance(part, bytes):
                try:
                    subject_parts.append(part.decode(encoding if encoding else "utf-8"))
                except:
                    subject_parts.append(part.decode("latin-1"))
            else:
                subject_parts.append(part)
        return "".join(subject_parts)
    
    def check_imap(self, mail):
        """检查IMAP邮箱中的新邮件"""
        # 搜索所有邮件
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print("无法获取邮件列表")
            return
        
        # 获取所有邮件ID
        email_ids = messages[0].split()
        new_email_ids = set(email_ids) - self.last_email_ids
        
        if not new_email_ids:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 没有新邮件")
            return
        
        print(f"\n发现 {len(new_email_ids)} 封新邮件:")
        
        # 处理新邮件
        for email_id in new_email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                continue
            
            # 解析邮件
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            
            # 获取邮件信息
            subject = self.decode_subject(email_message["Subject"])
            from_ = email.utils.parseaddr(email_message.get("From"))[1]
            date = email_message.get("Date")
            
            print(f" - 来自: {from_}")
            print(f"   主题: {subject}")
            print(f"   时间: {date}")
        
        # 更新最后检查的邮件ID
        self.last_email_ids = set(email_ids)
    
    def check_pop3(self, mail):
        """检查POP3邮箱中的新邮件"""
        # 获取邮件数量和大小
        num_messages = len(mail.list()[1])
        
        if num_messages == len(self.last_email_ids):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 没有新邮件")
            return
        
        print(f"\n发现 {num_messages - len(self.last_email_ids)} 封新邮件:")
        
        # 处理新邮件
        for i in range(len(self.last_email_ids) + 1, num_messages + 1):
            # 获取邮件
            _, lines, _ = mail.retr(i)
            raw_email = b"\n".join(lines)
            email_message = email.message_from_bytes(raw_email)
            
            # 获取邮件信息
            subject = self.decode_subject(email_message["Subject"])
            from_ = email.utils.parseaddr(email_message.get("From"))[1]
            date = email_message.get("Date")
            
            print(f" - 来自: {from_}")
            print(f"   主题: {subject}")
            print(f"   时间: {date}")
        
        # 更新最后检查的邮件ID
        self.last_email_ids = set(range(1, num_messages + 1))
    
    def check_mail(self):
        """检查新邮件"""
        print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 开始检查邮箱...")
        
        mail = self.connect()
        if not mail:
            return
        
        try:
            if self.protocol == "IMAP":
                self.check_imap(mail)
            else:
                self.check_pop3(mail)
        except Exception as e:
            print(f"检查邮件时出错: {str(e)}")
        finally:
            if self.protocol == "IMAP":
                mail.logout()
            else:
                mail.quit()
        
        self.last_check = datetime.now()
    
    def start(self):
        """开始定期检查邮箱"""
        print(f"开始监控邮箱: {self.username}")
        print(f"服务器: {self.server}:{self.port}")
        print(f"协议: {self.protocol}")
        print(f"检查间隔: {self.interval}秒")
        
        try:
            while True:
                self.check_mail()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n邮箱监控已停止")

def main():
    parser = argparse.ArgumentParser(description="邮箱监控工具")
    parser.add_argument("server", help="邮件服务器地址")
    parser.add_argument("port", type=int, help="邮件服务器端口")
    parser.add_argument("protocol", choices=["pop3", "imap"], help="协议类型 (POP3 或 IMAP)")
    parser.add_argument("username", help="邮箱用户名")
    parser.add_argument("password", help="邮箱密码")
    parser.add_argument("--interval", type=int, default=300, help="检查间隔（秒），默认300秒（5分钟）")
    
    args = parser.parse_args()
    
    try:
        checker = MailChecker(
            server=args.server,
            port=args.port,
            protocol=args.protocol,
            username=args.username,
            password=args.password,
            interval=args.interval
        )
        checker.start()
    except Exception as e:
        print(f"初始化失败: {str(e)}")

if __name__ == "__main__":
    main()
