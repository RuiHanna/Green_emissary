const express = require("express");
const mysql = require("mysql");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors()); // 允许前端访问

// 连接数据库
const db = mysql.createConnection({
  host: "127.0.0.1",
  user: "root",
  password: "123456",
  database: "quiz_app",
});

db.connect((err) => {
  if (err) {
    console.error("数据库连接失败: " + err.message);
  } else {
    console.log("成功连接到数据库");
  }
});

// 获取所有题目及选项
app.get("/questions", (req, res) => {
  const sql = "SELECT * FROM questions";
  db.query(sql, (err, questions) => {
    if (err) return res.status(500).json(err);

    const questionIds = questions.map(q => q.id);
    const sqlOptions = "SELECT * FROM options WHERE question_id IN (?)";
    db.query(sqlOptions, [questionIds], (err, options) => {
      if (err) return res.status(500).json(err);

      const formattedQuestions = questions.map(q => ({
        id: q.id,
        question: q.question_text,
        type: q.type,
        options: q.type === "multiple" ? options.filter(opt => opt.question_id === q.id).map(opt => opt.option_text) : ["正确", "错误"],
        answer: q.correct_answer
      }));

      res.json(formattedQuestions);
    });
  });
});

// 启动服务器
app.listen(3000, () => {
  console.log("服务器运行在 http://127.0.0.1:3000");
});
