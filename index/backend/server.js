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
    // password: "123456",
    password: "password",
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

// app.get("/questions", (req, res) => {
//     // 1. 获取题目总数
//     const sqlCount = "SELECT COUNT(*) AS total FROM questions";
//     db.query(sqlCount, (err, countResult) => {
//         if (err) return res.status(500).json(err);
//
//         const totalQuestions = countResult[0].total;
//         // console.log(totalQuestions)
//
//         // 2. 生成 10 个随机的题目 ID
//         const randomIds = new Set();
//         while (randomIds.size < 10) {
//             const randomId = Math.floor(Math.random() * totalQuestions) + 1;
//             randomIds.add(randomId);
//         }
//         // console.log(randomIds)
//
//         // 3. 查询随机的 10 道题目
//         const sqlQuestions = "SELECT * FROM questions WHERE id IN (?)";
//         db.query(sqlQuestions, [Array.from(randomIds)], (err, questions) => {
//             if (err) return res.status(500).json(err);
//
//             // 4. 获取这些题目的选项，并按 question_id 排序
//             const questionIds = questions.map(q => q.id);
//             const sqlOptions = "SELECT * FROM options WHERE question_id IN (?) ORDER BY question_id";
//             db.query(sqlOptions, [questionIds], (err, options) => {
//                 if (err) return res.status(500).json(err);
//
//                 // console.log(questions)
//                 // console.log(options)
//
//                 // 5. 将选项按 question_id 分组
//                 const optionsMap = new Map();
//                 options.forEach(opt => {
//                     if (!optionsMap.has(opt.question_id)) {
//                         optionsMap.set(opt.question_id, []);
//                     }
//                     optionsMap.get(opt.question_id).push(opt.option_text);
//                 });
//
//                 // 6. 格式化题目和选项
//                 const formattedQuestions = questions.map(q => ({
//                     id: q.id,
//                     question: q.question_text,
//                     type: q.type,
//                     options: q.type === "multiple"
//                         ? optionsMap.get(q.id) || [] // 获取对应题目的选项
//                         : ["正确", "错误"], // 判断题的固定选项
//                     answer: q.correct_answer
//                 }));
//
//                 res.json(formattedQuestions);
//             });
//         });
//     });
// });

// 启动服务器
app.listen(3000, () => {
    console.log("服务器运行在 http://127.0.0.1:3000");
});
