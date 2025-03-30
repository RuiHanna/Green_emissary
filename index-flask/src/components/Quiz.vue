<template>
  <div class="quiz-container">
    <h1 class="title">🌱 生态作物科普问答 🌿</h1>
    <div v-if="currentQuestion" class="question-box">
      <!-- 题目 -->
      <h2 class="question-text">{{ currentQuestion.question }}</h2>

      <!-- 判断题 -->
      <div v-if="currentQuestion.type === 'true_false'" class="true-false-container">
        <button v-for="(option, index) in ['正确', '错误']" :key="index" class="judge-button" @click="checkAnswer(option)">
          {{ option }}
        </button>
      </div>

      <!-- 选择题 -->
      <div v-else class="choice-container">
        <button v-for="(option, index) in currentQuestion.options" :key="index" class="option"
          @click="checkAnswer(option)">
          {{ option }}
        </button>
      </div>

      <!-- 反馈 & 下一题按钮 -->
      <div class="feedback-box">
        <div v-if="feedback" :class="['feedback', feedbackClass]">
          {{ feedback }}
        </div>
        <button v-if="showNextButton" class="next-button" @click="nextQuestion">
          下一题 →
        </button>
      </div>
    </div>

    <!-- 结束页面 -->
    <div v-else class="result-page">
      <h2>🎉 问答结束！🎉</h2>
      <div class="score-box">
        <p>您的得分：<span class="score">{{ score }}</span> / {{ totalQuestions }}</p>
      </div>
      <button class="restart-button" @click="restartQuiz">🔄 重新开始</button>
    </div>

    <!-- 返回首页按钮 -->
    <button class="home-button" @click="goHome">🏠 返回首页</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentIndex: 0,
      score: 0,
      feedback: "",
      feedbackClass: "",
      showNextButton: false,
      questions: []
    };
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentIndex] || null;
    },
    totalQuestions() {
      return this.questions.length;
    },
  },          
  methods: {
    async fetchQuestions() {
      try {
        const response = await fetch("http://localhost:3000/questions");
        this.questions = await response.json();
      } catch (error) {
        console.error("加载题目失败:", error);
      }
    },
    checkAnswer(selectedOption) {
      if (selectedOption === this.currentQuestion.answer) {
        this.feedback = "✅ 答对了！";
        this.feedbackClass = "correct";
        this.score++;
      } else {
        this.feedback = "❌ 回答错误";
        this.feedbackClass = "incorrect";
      }
      this.showNextButton = true;
    },
    nextQuestion() {
      this.feedback = "";
      this.showNextButton = false;
      this.currentIndex++;
    },
    restartQuiz() {
      this.currentIndex = 0;
      this.score = 0;
      this.feedback = "";
      this.showNextButton = false;
    },
    goHome() {
      this.$router.push("/"); // 确保 Vue Router 已启用
    },
  },
  mounted() {
    this.fetchQuestions();
  },
};
</script>

<style scoped>
/* 页面整体样式 */
.quiz-container {
  background: #d7ebd8;
  /* 淡绿色背景 */
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #2e7d32;
  margin-bottom: 1.5rem;
}

/* 题目框 */
.question-box {
  background: white;
  width: 60%;
  max-width: 600px;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  text-align: center;
}

/* 题目文本 */
.question-text {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

/* 判断题按钮 */
.true-false-container {
  display: flex;
  justify-content: center;
  gap: 1.2rem;
}

.judge-button {
  width: 120px;
  height: 50px;
  border: 2px solid #42b983;
  border-radius: 10px;
  background: white;
  color: #42b983;
  font-size: 1.1rem;
  cursor: pointer;
  transition: 0.3s;
}

.judge-button:hover {
  background: #42b983;
  color: white;
}

/* 选择题按钮 */
.choice-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.option {
  background: #fff;
  border: 2px solid #42b983;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: 0.3s;
}

.option:hover {
  background: #42b983;
  color: white;
}

/* 反馈框 */
.feedback-box {
  margin-top: 1.5rem;
}

.feedback {
  padding: 1rem;
  border-radius: 8px;
  font-weight: bold;
}

.correct {
  background: #e8f5e9;
  color: #2e7d32;
  border: 2px solid #66bb6a;
}

.incorrect {
  background: #ffebee;
  color: #c62828;
  border: 2px solid #ef5350;
}

/* 下一题按钮 */
.next-button {
  margin-top: 1rem;
  background: #42b983;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}

.next-button:hover {
  background: #369f6e;
}

/* 结果页 */
.result-page {
  text-align: center;
}

.score-box {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.score {
  color: #42b983;
  font-size: 1.5rem;
  font-weight: bold;
}

/* 重新开始按钮 */
.restart-button {
  margin-top: 1.5rem;
  background: #ffa726;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}

.restart-button:hover {
  background: #fb8c00;
}

/* 返回首页按钮 */
.home-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #2e7d32;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: 0.3s;
}

.home-button:hover {
  background: #1b5e20;
}
</style>
