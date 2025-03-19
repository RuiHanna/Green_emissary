from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLOv10
from flask_cors import CORS
from collections import defaultdict
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort
import pymysql
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局模型变量和检测统计
model = None
tracker = DeepSort(max_age=30)
track_history = defaultdict(list)

# MySQL 连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    # 'password': 'root123',
    'password': 'password',
    'database': 'yolo'
}


# 加载模型
def load_model():
    global model
    model = YOLOv10.from_pretrained('jameslahm/yolov10n')
    # print("Model loaded successfully")


# 连接到 MySQL 数据库
def get_db_connection():
    try:
        connection = pymysql.connect(**db_config)
        # print("Database connection successful")
        return connection
    except Exception as e:
        # print(f"Error connecting to database: {e}")
        raise


# 存储检测数据到 MySQL
def store_detection_data(label, confidence, box, track_id):
    x1, y1, x2, y2 = box
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 先检查 track_id 是否已经存在
            cursor.execute('''SELECT COUNT(*) FROM detections WHERE track_id = %s''', (track_id,))
            result = cursor.fetchone()

            if result[0] == 0:  # 如果 track_id 不存在
                # 插入新的检测数据
                cursor.execute('''INSERT INTO detections (label, confidence, x, y, track_id) 
                                  VALUES (%s, %s, %s, %s, %s)''',
                               (label, confidence, (x1 + x2) / 2, (y1 + y2) / 2, track_id))
                conn.commit()
                # print(f"Stored detection: {label}, {confidence}, {box}, {track_id}")
    except Exception as e:
        print(f"Error storing detection data: {e}")
    finally:
        conn.close()


# 非极大值抑制 (NMS)
def nms(boxes, scores, iou_threshold=0.5):
    if len(boxes) == 0:
        return []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)
        inter = w * h
        iou = inter / (areas[i] + areas[order[1:]] - inter)
        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]
    return keep


# 实时摄像头检测
def generate_frames():
    cap = cv2.VideoCapture(3)
    # cap = cv2.VideoCapture(1)  # 0 表示默认摄像头设备
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        detection_result = detect_objects(frame, model)
        ret, buffer = cv2.imencode('.jpg', detection_result)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()


def detect_objects(frame, model):
    results = model.predict(frame)
    result = results[0]
    boxes = result.boxes.xyxy.cpu().numpy()  # 获取边界框
    labels = result.boxes.cls.cpu().numpy()  # 获取标签
    confidences = result.boxes.conf.cpu().numpy()  # 获取置信度

    # 使用 NMS 过滤重复检测
    keep_indices = nms(boxes, confidences, iou_threshold=0.5)
    boxes = boxes[keep_indices]
    labels = labels[keep_indices]
    confidences = confidences[keep_indices]

    # 使用 DeepSORT 进行追踪
    detections = []
    for box, label, confidence in zip(boxes, labels, confidences):
        x1, y1, x2, y2 = map(int, box)
        detections.append(([x1, y1, x2 - x1, y2 - y1], confidence, int(label)))

    # 更新追踪器
    tracks = tracker.update_tracks(detections, frame=frame)

    # 绘制检测框和标签
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        ltrb = track.to_ltrb()  # 获取跟踪框坐标
        x1, y1, x2, y2 = map(int, ltrb)
        label = model.names[int(track.det_class)] if track.det_class is not None else "Unknown"
        confidence = track.det_conf if track.det_conf is not None else 0.0

        # 存储检测数据
        store_detection_data(label, confidence, (x1, y1, x2, y2), track_id)

        # 绘制检测框和标签
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = f'{label} {confidence:.2f} ID:{track_id}'
        cv2.putText(frame, text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

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


# 路由返回柱状图数据
@app.route('/chart_data')
def chart_data():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 查询当天前五多的动物种类
            query = """
                SELECT label, COUNT(*) as count
                FROM detections
                WHERE DATE(timestamp) = CURDATE()
                GROUP BY label
                ORDER BY count DESC
                LIMIT 5
            """
            cursor.execute(query)
            results = cursor.fetchall()
            # print("Chart Data Results:", results)  # 打印查询结果
            labels = [row[0] for row in results]
            values = [row[1] for row in results]
        conn.close()
        return jsonify({
            'labels': labels,
            'values': values
        })
    except Exception as e:
        # print(f"Error fetching chart data: {e}")
        return jsonify({
            'labels': [],
            'values': []
        })


# 路由返回饼图数据
@app.route('/pie_data')
def get_pie_data():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 查询当天各个类别的数量
            query = """
                SELECT label, COUNT(*) as count
                FROM detections
                WHERE DATE(timestamp) = CURDATE()
                GROUP BY label
            """
            cursor.execute(query)
            results = cursor.fetchall()
            # print("Pie Data Results:", results)  # 打印查询结果
            data = [{"name": row[0], "value": row[1]} for row in results]
        conn.close()
        return jsonify(data)
    except Exception as e:
        # print(f"Error fetching pie data: {e}")
        return jsonify([])


@app.route('/time_series_data')
def get_time_series_data():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 查询前五多的动物种类
            top_5_query = """
                SELECT label
                FROM detections
                WHERE DATE(timestamp) >= %s
                GROUP BY label
                ORDER BY COUNT(*) DESC
                LIMIT 5
            """
            ten_days_ago = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
            cursor.execute(top_5_query, (ten_days_ago,))
            top_5_labels = [row[0] for row in cursor.fetchall()]

            # 查询近 10 天每天的目标数量（按种类分组）
            time_series_query = """
                SELECT DATE(timestamp) as date, label, COUNT(*) as count
                FROM detections
                WHERE timestamp >= %s
                GROUP BY DATE(timestamp), label
                ORDER BY date ASC
            """
            cursor.execute(time_series_query, (ten_days_ago,))
            results = cursor.fetchall()

            # 组织数据
            dates = sorted(list(set(row[0].strftime('%Y-%m-%d') for row in results)))
            counts = {label: [0] * len(dates) for label in top_5_labels}  # 初始化每个类别的数量为 0

            for row in results:
                date = row[0].strftime('%Y-%m-%d')
                label = row[1]
                count = row[2]
                if label in counts:
                    index = dates.index(date)
                    counts[label][index] = count

        conn.close()
        return jsonify({
            "dates": dates,
            "counts": counts
        })
    except Exception as e:
        print(f"Error fetching time series data: {e}")
        return jsonify({
            "dates": [],
            "counts": {}
        })


@app.route('/time_heatmap_data')
def get_time_heatmap_data():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 查询近 7 天每小时的活动频率
            query = """
                SELECT DAYOFWEEK(timestamp) as day, HOUR(timestamp) as hour, COUNT(*) as count
                FROM detections
                WHERE timestamp >= %s
                GROUP BY DAYOFWEEK(timestamp), HOUR(timestamp)
                ORDER BY day, hour
            """
            seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            cursor.execute(query, (seven_days_ago,))
            results = cursor.fetchall()
            # print("Time Heatmap Data Results:", results)  # 打印查询结果

            # 初始化热力图数据
            heatmap = defaultdict(int)
            for row in results:
                day = row[0] - 1  # DAYOFWEEK 返回 1-7，调整为 0-6
                hour = row[1]
                count = row[2]
                heatmap[(day, hour)] = count

            # 转换为前端需要的格式
            hours = list(range(24))
            days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            data = []
            for day_idx, day in enumerate(days):
                for hour_idx, hour in enumerate(hours):
                    value = heatmap.get((day_idx, hour_idx), 0)
                    data.append([hour_idx, day_idx, value])

        conn.close()
        return jsonify({
            'hours': hours,
            'days': days,
            'data': data
        })
    except Exception as e:
        print(f"Error fetching time heatmap data: {e}")
        return jsonify({
            'hours': [],
            'days': [],
            'data': []
        })


@app.route('/scatter_paths')
def get_scatter_paths():
    scatter_paths = [
        "path://M23.6 2c-3.363 0-6.258 2.736-7.599 5.594-1.342-2.858-4.237-5.594-7.601-5.594-4.637 0-8.4 3.764-8.4 8.401 0 9.433 9.516 11.906 16.001 21.232 6.13-9.268 15.999-12.1 15.999-21.232 0-4.637-3.763-8.401-8.4-8.401z",
        "path://M16 0c-8.837 0-16 7.163-16 16s7.163 16 16 16 16-7.163 16-16-7.163-16-16-16zM10 14c-1.105 0-2-1.343-2-3s0.895-3 2-3 2 1.343 2 3-0.895 3-2 3zM16 26c-2.209 0-4-1.791-4-4s1.791-4 4-4c2.209 0 4 1.791 4 4s-1.791 4-4 4zM22 14c-1.105 0-2-1.343-2-3s0.895-3 2-3 2 1.343 2 3-0.895 3-2 3z",
        "path://M32 2c0-1.422-0.298-2.775-0.833-4-1.049 2.401-3.014 4.31-5.453 5.287-2.694-2.061-6.061-3.287-9.714-3.287s-7.021 1.226-9.714 3.287c-2.439-0.976-4.404-2.886-5.453-5.287-0.535 1.225-0.833 2.578-0.833 4 0 2.299 0.777 4.417 2.081 6.106-1.324 2.329-2.081 5.023-2.081 7.894 0 8.837 7.163 16 16 16s16-7.163 16-16c0-2.871-0.757-5.565-2.081-7.894 1.304-1.689 2.081-3.806 2.081-6.106zM18.003 11.891c0.064-1.483 1.413-2.467 2.55-3.036 1.086-0.543 2.16-0.814 2.205-0.826 0.536-0.134 1.079 0.192 1.213 0.728s-0.192 1.079-0.728 1.213c-0.551 0.139-1.204 0.379-1.779 0.667 0.333 0.357 0.537 0.836 0.537 1.363 0 1.105-0.895 2-2 2s-2-0.895-2-2c0-0.037 0.001-0.073 0.003-0.109zM8.030 8.758c0.134-0.536 0.677-0.862 1.213-0.728 0.045 0.011 1.119 0.283 2.205 0.826 1.137 0.569 2.486 1.553 2.55 3.036 0.002 0.036 0.003 0.072 0.003 0.109 0 1.105-0.895 2-2 2s-2-0.895-2-2c0-0.527 0.204-1.005 0.537-1.363-0.575-0.288-1.228-0.528-1.779-0.667-0.536-0.134-0.861-0.677-0.728-1.213zM16 26c-3.641 0-6.827-1.946-8.576-4.855l2.573-1.544c1.224 2.036 3.454 3.398 6.003 3.398s4.779-1.362 6.003-3.398l2.573 1.544c-1.749 2.908-4.935 4.855-8.576 4.855z",
        "path://M16 0c-8.837 0-16 7.163-16 16s7.163 16 16 16 16-7.163 16-16-7.163-16-16-16zM10 8c1.105 0 2 1.343 2 3s-0.895 3-2 3-2-1.343-2-3 0.895-3 2-3zM16 28c-5.215 0-9.544-4.371-10-9.947 2.93 1.691 6.377 2.658 10 2.658s7.070-0.963 10-2.654c-0.455 5.576-4.785 9.942-10 9.942zM22 8c1.105 0 2 1.343 2 3s-0.895 3-2 3-2-1.343-2-3 0.895-3 2-3z",
        "path://M16 0c-8.837 0-16 7.163-16 16s7.163 16 16 16 16-7.163 16-16-7.163-16-16-16zM10 14c-1.105 0-2-1.343-2-3s0.895-3 2-3 2 1.343 2 3-0.895 3-2 3zM16 26c-2.209 0-4-1.791-4-4s1.791-4 4-4c2.209 0 4 1.791 4 4s-1.791 4-4 4zM22 14c-1.105 0-2-1.343-2-3s0.895-3 2-3 2 1.343 2 3-0.895 3-2 3z"
    ]
    return jsonify(scatter_paths)


@app.route('/daily_top_animals')
def get_daily_top_animals():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 查询每天前三多的动物种类
            query = """
                SELECT DATE(timestamp) as date, label, COUNT(*) as count
                FROM detections
                WHERE timestamp >= %s
                GROUP BY DATE(timestamp), label
                ORDER BY date, count DESC
            """
            ten_days_ago = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
            cursor.execute(query, (ten_days_ago,))
            results = cursor.fetchall()

            # 组织数据
            data = {}
            for row in results:
                date = row[0].strftime('%Y-%m-%d')
                label = row[1]
                count = row[2]

                if date not in data:
                    data[date] = []
                if len(data[date]) < 3:  # 只保留每天前三多的动物
                    data[date].append({"label": label, "count": count})

        conn.close()
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching daily top animals data: {e}")
        return jsonify({})


# @app.route('/animal_paths')
# def get_animal_paths():
#     animal_paths = [
#         "static/images/cat.png",
#         "static/images/dog.png",
#         "static/images/chang.png",
#         # "static/images/cat.png",
#         # 添加更多路径数据...
#     ]
#     return jsonify(animal_paths)

# 加载模型
load_model()

if __name__ == '__main__':
    app.run(debug=True)
