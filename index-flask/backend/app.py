from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 数据库配置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'password',
    'database': 'quiz_app'
}

# 获取所有题目及选项
@app.route('/questions', methods=['GET'])
def get_questions():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # 获取所有问题
        cursor.execute("SELECT * FROM questions ORDER BY RAND() LIMIT 10")
        questions = cursor.fetchall()

        # 获取所有选项
        question_ids = [q['id'] for q in questions]
        format_strings = ','.join(['%s'] * len(question_ids))
        cursor.execute(f"SELECT * FROM options WHERE question_id IN ({format_strings})", tuple(question_ids))
        options = cursor.fetchall()

        # 格式化问题数据
        formatted_questions = []
        for q in questions:
            formatted_questions.append({
                'id': q['id'],
                'question': q['question_text'],
                'type': q['type'],
                'options': [opt['option_text'] for opt in options if opt['question_id'] == q['id']],
                'answer': q['correct_answer']
            })

        return jsonify(formatted_questions)

    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    app.run(port=3000)
