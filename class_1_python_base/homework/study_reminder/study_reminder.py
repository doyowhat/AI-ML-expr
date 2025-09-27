import smtplib
import schedule
import time
import sys
import io
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import json

# 解决Windows命令行中文编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ====== 配置信息 ======
SENDER_EMAIL = "1426530692@qq.com"
# TODO 将AUTH_CODE设置为环境变量，用os.environ.get获取
AUTH_CODE = "garipdsffjmcjgdd"  # QQ邮箱授权码
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
RECIPIENTS = ["1426530692@qq.com"]  # 收件人列表

# ====== 学习计划数据 ======
STUDY_PLAN = [
    {"subject": "英语四级词汇", 
     "schedule": [
        {"time": "09:00", "task": "背诵Unit1-Unit3单词"},
        {"time": "14:00", "task": "完成阅读理解练习"}
     ]},
     
    {"subject": "高等数学", 
     "schedule": [
        {"time": "10:30", "task": "完成微积分习题集P45-50"},
        {"time": "16:00", "task": "复习极限与连续章节"}
     ]},
     
    {"subject": "Python编程", 
     "schedule": [
        {"time": "15:00", "task": "完成函数与模块练习"},
        {"time": "20:00", "task": "项目实战：邮件提醒系统优化"}
     ]}
]

# ====== 邮件发送功能 ======
def send_email(subject, content):
    """通过QQ邮箱发送提醒邮件"""
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECIPIENTS)

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, AUTH_CODE)
            server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())
            
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 邮件发送成功: {subject}")
        return True
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False

# ====== 学习计划生成与发送 ======
def generate_daily_plan():
    """生成今日学习计划内容"""
    # 使用英文格式避免编码问题
    today = datetime.now().strftime("%Y-%m-%d")
    email_content = f"📚 今日学习计划 ({today})\n\n"
    
    for course in STUDY_PLAN:
        email_content += f"【{course['subject']}】\n"
        for task in course['schedule']:
            email_content += f"⏰ {task['time']}: {task['task']}\n"
        email_content += "\n"
    
    email_content += "💡 温馨提示：请合理安排时间，完成计划后记得标记进度！"
    return f"📖 今日学习计划提醒 - {today}", email_content

def send_immediate_plan():
    """立即发送当天计划"""
    subject, content = generate_daily_plan()
    if send_email(subject, content):
        print("✅ 当天计划已立即发送")
    else:
        print("❌ 当天计划发送失败")

def specific_task_reminder(subject, task_info):
    """特定任务提醒"""
    send_email(f"🔔 任务提醒: {subject}", f"您计划的任务即将开始：\n\n{task_info}")

# ====== 定时任务设置 ======
def setup_schedules():
    """配置定时任务"""
    # 每日早晨7:30发送全天计划
    schedule.every().day.at("07:30").do(
        lambda: send_email(*generate_daily_plan())
    )
    
    # 为每个任务设置提前10分钟提醒
    for course in STUDY_PLAN:
        for task in course['schedule']:
            task_time = (datetime.strptime(task['time'], "%H:%M") 
                         - timedelta(minutes=10)).strftime("%H:%M")
            schedule.every().day.at(task_time).do(
                specific_task_reminder, 
                course['subject'], 
                f"{task['time']} - {task['task']}"
            )
    
    print("⏰ 定时提醒任务已启动...")

# ====== 主程序 ======
if __name__ == "__main__":
    # 保存学习计划到JSON文件（可选）
    with open('study_plan.json', 'w', encoding='utf-8') as f:
        json.dump(STUDY_PLAN, f, ensure_ascii=False, indent=2)
    
    # 立即发送当天计划
    send_immediate_plan()
    
    # 设置定时任务
    setup_schedules()
    
    # 保持程序持续运行
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次任务
    except KeyboardInterrupt:
        print("\n程序已退出")