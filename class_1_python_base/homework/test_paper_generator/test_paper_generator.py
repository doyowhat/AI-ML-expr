import json
import random
import argparse
from typing import Dict, List, Any
from pathlib import Path

class QuestionBank:
    """题库管理类"""
    
    def __init__(self, bank_file: str):
        self.bank_file = bank_file
        self.questions = self.load_question_bank()
    
    def load_question_bank(self) -> List[Dict[str, Any]]:
        """加载题库文件"""
        try:
            with open(self.bank_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("题库文件格式错误：应该包含题目列表")
                return data
        except FileNotFoundError:
            print(f"错误：题库文件 '{self.bank_file}' 未找到")
            return []
        except json.JSONDecodeError:
            print(f"错误：题库文件 '{self.bank_file}' JSON格式错误")
            return []
    
    def get_random_questions(self, count: int, question_types: List[str] = None) -> List[Dict[str, Any]]:
        """随机获取指定数量的题目"""
        if not self.questions:
            print("警告：题库为空")
            return []
        
        # 过滤题型
        filtered_questions = self.questions
        if question_types:
            filtered_questions = [q for q in self.questions 
                                 if q.get('type', '') in question_types]
        
        # 确保不超出题库范围
        count = min(count, len(filtered_questions))
        
        # 随机选择题目
        return random.sample(filtered_questions, count)

class AnswerBank:
    """答案管理类"""
    
    def __init__(self, answer_file: str):
        self.answer_file = answer_file
        self.answers = self.load_answer_bank()
    
    def load_answer_bank(self) -> Dict[str, Any]:
        """加载答案文件"""
        try:
            with open(self.answer_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"错误：答案文件 '{self.answer_file}' 未找到")
            return {}
        except json.JSONDecodeError:
            print(f"错误：答案文件 '{self.answer_file}' JSON格式错误")
            return {}
    
    def get_answers(self, question_ids: List[str]) -> Dict[str, Any]:
        """获取指定题目的答案"""
        return {qid: self.answers.get(qid, "答案未找到") for qid in question_ids}

class ExamGenerator:
    """试卷生成器"""
    
    def __init__(self, question_bank: QuestionBank, answer_bank: AnswerBank):
        self.question_bank = question_bank
        self.answer_bank = answer_bank
    
    def generate_exam(self, exam_title: str, question_count: int, 
                     output_file: str, question_types: List[str] = None) -> Dict[str, Any]:
        """生成试卷和答案"""
        # 随机选择题目
        selected_questions = self.question_bank.get_random_questions(question_count, question_types)
        
        if not selected_questions:
            print("无法生成试卷：没有可用的题目")
            return {}
        
        # 提取题目ID
        question_ids = [q['id'] for q in selected_questions if 'id' in q]
        
        # 获取对应答案
        answers = self.answer_bank.get_answers(question_ids)
        
        # 生成试卷结构
        exam = {
            "title": exam_title,
            "date": "2025-09-14",  # 可以使用datetime自动生成
            "questions": selected_questions,
            "answers": answers
        }
        
        # 保存试卷文件
        self.save_exam(exam, output_file)
        
        # 同时生成答案文件
        answer_output = output_file.replace('.json', '_answers.json')
        self.save_answers(answers, answer_output)
        
        return exam
    
    def save_exam(self, exam: Dict[str, Any], output_file: str):
        """保存试卷到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(exam, f, indent=2, ensure_ascii=False)
            print(f"试卷已保存到: {output_file}")
        except IOError as e:
            print(f"保存试卷时出错: {str(e)}")
    
    def save_answers(self, answers: Dict[str, Any], output_file: str):
        """保存答案到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(answers, f, indent=2, ensure_ascii=False)
            print(f"答案已保存到: {output_file}")
        except IOError as e:
            print(f"保存答案时出错: {str(e)}")

def create_sample_files():
    """创建示例题库和答案文件（如果不存在）"""
    # 示例题库结构
    sample_questions = [
        {
            "id": "Q001",
            "type": "choice",
            "content": "Python中如何表示不等于？",
            "options": ["A. !=", "B. =!", "C. <>", "D. ><"],
            "difficulty": "easy",
            "subject": "编程",
            "grade": "初中"
        },
        {
            "id": "Q002",
            "type": "choice",
            "content": "下列哪个不是Python的数据类型？",
            "options": ["A. list", "B. tuple", "C. array", "D. dict"],
            "difficulty": "easy",
            "subject": "编程",
            "grade": "初中"
        },
        {
            "id": "Q003",
            "type": "fill_blank",
            "content": "Python中使用_____关键字定义函数",
            "difficulty": "easy",
            "subject": "编程",
            "grade": "初中"
        },
        {
            "id": "Q004",
            "type": "short_answer",
            "content": "简述Python中列表和元组的区别",
            "difficulty": "medium",
            "subject": "编程",
            "grade": "高中"
        }
    ]
    
    # 示例答案结构
    sample_answers = {
        "Q001": "A",
        "Q002": "C",
        "Q003": "def",
        "Q004": "列表是可变的，元组是不可变的。列表使用方括号[]，元组使用圆括号()。"
    }
    
    # 如果文件不存在，创建示例文件
    if not Path("question_bank.json").exists():
        with open("question_bank.json", "w", encoding='utf-8') as f:
            json.dump(sample_questions, f, indent=2, ensure_ascii=False)
        print("已创建示例题库文件: question_bank.json")
    
    if not Path("answer_bank.json").exists():
        with open("answer_bank.json", "w", encoding='utf-8') as f:
            json.dump(sample_answers, f, indent=2, ensure_ascii=False)
        print("已创建示例答案文件: answer_bank.json")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="试卷生成器")
    parser.add_argument("--count", type=int, default=5, help="题目数量")
    parser.add_argument("--title", type=str, default="期末测试", help="试卷标题")
    parser.add_argument("--output", type=str, default="exam.json", help="输出文件名")
    parser.add_argument("--types", nargs="+", default=["choice", "fill_blank", "short_answer"], 
                       help="题目类型")
    
    args = parser.parse_args()
    
    # 创建示例文件（如果不存在）
    create_sample_files()
    
    # 初始化题库和答案库
    question_bank = QuestionBank("question_bank.json")
    answer_bank = AnswerBank("answer_bank.json")
    
    # 生成试卷
    generator = ExamGenerator(question_bank, answer_bank)
    exam = generator.generate_exam(args.title, args.count, args.output, args.types)
    
    if exam:
        print(f"试卷生成成功！共包含 {len(exam['questions'])} 道题目")
        print(f"试卷文件: {args.output}")
        print(f"答案文件: {args.output.replace('.json', '_answers.json')}")

if __name__ == "__main__":
    main()