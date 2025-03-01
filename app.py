from flask import Flask, render_template, Response
import cv2
from ultralytics import YOLOv10
#  pip install git+https://github.com/THU-MIG/yolov10.git
app = Flask(__name__)

# 全局模型变量
model = None

# 加载模型
def load_model():
    global model
    model = YOLOv10.from_pretrained('jameslahm/yolov10n')

# 实时摄像头检测
def generate_frames():
    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 0 表示默认摄像头设备

    while True:
        # 读取一帧
        ret, frame = cap.read()
        if not ret:
            break

        # 进行目标检测
        detection_result = detect_objects(frame, model)

        # 将帧转换为 JPEG 格式
        ret, buffer = cv2.imencode('.jpg', detection_result)
        frame = buffer.tobytes()

        # 使用 yield 返回帧
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # 释放摄像头
    cap.release()

# 目标检测函数
def detect_objects(frame, model):
    # 使用 model.predict 进行推理
    results = model.predict(frame)

    # 提取第一个结果
    result = results[0]

    # 提取检测结果
    boxes = result.boxes.xyxy.cpu().numpy()  # 边界框坐标
    labels = result.boxes.cls.cpu().numpy()  # 类别标签
    confidences = result.boxes.conf.cpu().numpy()  # 置信度

    # 在帧上绘制检测结果
    for box, label, confidence in zip(boxes, labels, confidences):
        x1, y1, x2, y2 = map(int, box)  # 转换为整数
        label_name = model.names[int(label)]  # 获取类别名称

        # 绘制边界框
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 绘制类别和置信度
        cv2.putText(frame, f'{label_name} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

# 路由渲染前端页面
@app.route('/')
def index():
    return render_template('index.html')

# 路由处理实时摄像头检测请求
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# 初始加载模型
load_model()

if __name__ == '__main__':
    app.run(debug=True)