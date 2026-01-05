import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
from collections import deque

# Инициализация MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Точные индексы для глаз (ear) MediaPipe
LEFT_EYE = [362, 385, 387, 263, 373, 380]  # Правый глаз
RIGHT_EYE = [33, 160, 158, 133, 153, 144]  # Левый глаз

# Настройки по данным
EAR_THRESHOLD = 0.220  # порог между прищуром (0.230) и закрытием (0.210)
EAR_CONSEC_FRAMES = 3  # Сколько кадров подряд EAR < порога для регистрации моргания
DEBOUNCE_TIME = 0.5  # Защита от двойных срабатываний (секунды)


def calculate_ear(eye_points, landmarks, img_shape):
    """Вычисляет EAR для одного глаза"""
    h, w = img_shape[:2]
    points = []
    for idx in eye_points:
        landmark = landmarks.landmark[idx]
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        points.append((x, y))

    # Формула EAR: (вертикаль1 + вертикаль2) / (2 * горизонталь)
    A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
    B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
    C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))
    ear = (A + B) / (2.0 * C)
    return ear, points


def press_q_key():
    """Нажимает клавишу Q и показывает подтверждение"""
    try:
        pyautogui.press('q')
        print(f"[{time.strftime('%H:%M:%S')}] ✓ Нажата клавиша Q")
        return True
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ✗ Ошибка: {e}")
        return False


def main():
    cap = cv2.VideoCapture(0)

    # Переменные для детекции
    ear_history = deque(maxlen=5)  # Сглаживание значений
    closed_frames = 0  # Счетчик кадров с закрытыми глазами
    blinking = False  # Флаг активного моргания
    last_blink_time = 0  # Время последнего моргания
    blink_count = 0  # Счетчик морганий

    print("=" * 60)
    print("ДЕТЕКТОР МОРГАНИЙ С НАЖАТИЕМ КЛАВИШИ Q")
    print(f"Порог EAR: {EAR_THRESHOLD}")
    print(f"Требуется кадров: {EAR_CONSEC_FRAMES}")
    print("=" * 60)
    print("СПРАВКА:")
    print("- Сядьте так, чтобы лицо было хорошо освещено")
    print("- Смотрите прямо в камеру")
    print("- Моргайте естественно, не слишком быстро")
    print("- ESC для выхода")
    print("=" * 60)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Зеркальное отображение
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Обработка MediaPipe
        results = face_mesh.process(rgb_frame)

        current_ear = 0.3  # Значение по умолчанию
        ear_status = "ОЖИДАНИЕ"
        status_color = (100, 100, 100)

        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                # Вычисляем EAR для обоих глаз
                left_ear, left_points = calculate_ear(LEFT_EYE, landmarks, frame.shape)
                right_ear, right_points = calculate_ear(RIGHT_EYE, landmarks, frame.shape)
                current_ear = (left_ear + right_ear) / 2.0

                # Сглаживание (медианный фильтр)
                ear_history.append(current_ear)
                smoothed_ear = np.median(list(ear_history)[-3:]) if len(ear_history) >= 3 else current_ear

                # Визуализация точек глаз
                for (x, y) in left_points + right_points:
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

                # Детекция моргания
                current_time = time.time()

                if smoothed_ear < EAR_THRESHOLD:
                    closed_frames += 1
                    ear_status = f"ЗАКРЫТЫ ({closed_frames}/{EAR_CONSEC_FRAMES})"
                    status_color = (0, 0, 255)  # Красный

                    # Если глаза закрыты достаточно долго и прошло время дебаунса
                    if (closed_frames >= EAR_CONSEC_FRAMES and
                            not blinking and
                            current_time - last_blink_time > DEBOUNCE_TIME):
                        blinking = True
                        blink_count += 1
                        last_blink_time = current_time

                        # Нажимаем клавишу Q
                        press_q_key()

                else:
                    if closed_frames >= EAR_CONSEC_FRAMES:
                        ear_status = "МОРГАНИЕ!"
                        status_color = (0, 255, 255)  # Желтый
                    else:
                        ear_status = "ОТКРЫТЫ"
                        status_color = (0, 255, 0)  # Зеленый

                    closed_frames = 0
                    blinking = False

        # Отображение информации на кадре
        y_offset = 30
        line_height = 30

        # EAR значение
        cv2.putText(frame, f"EAR: {current_ear:.3f}", (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Пороговая линия
        cv2.putText(frame, f"Порог: {EAR_THRESHOLD:.3f}", (10, y_offset + line_height),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

        # Статус
        cv2.putText(frame, f"Статус: {ear_status}", (10, y_offset + line_height * 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

        # Счетчик морганий
        cv2.putText(frame, f"Морганий: {blink_count}", (10, y_offset + line_height * 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)

        # Визуальный индикатор EAR
        indicator_x = 300
        indicator_y = y_offset
        indicator_width = 150
        indicator_height = 20

        # Фон индикатора
        cv2.rectangle(frame,
                      (indicator_x, indicator_y),
                      (indicator_x + indicator_width, indicator_y + indicator_height),
                      (50, 50, 50), -1)

        # Заполнение индикатора (нормализованное значение EAR)
        fill_width = int((current_ear / 0.4) * indicator_width)
        fill_width = max(0, min(fill_width, indicator_width))

        # Цвет индикатора: зеленый > порога, красный < порога
        indicator_color = (0, 255, 0) if current_ear > EAR_THRESHOLD else (0, 0, 255)
        cv2.rectangle(frame,
                      (indicator_x, indicator_y),
                      (indicator_x + fill_width, indicator_y + indicator_height),
                      indicator_color, -1)

        # Линия порога на индикаторе
        threshold_x = indicator_x + int((EAR_THRESHOLD / 0.4) * indicator_width)
        cv2.line(frame,
                 (threshold_x, indicator_y - 5),
                 (threshold_x, indicator_y + indicator_height + 5),
                 (0, 255, 255), 2)

        # Отображение кадра
        cv2.imshow('Blink Detector - Q Presser', frame)

        # Выход по ESC
        if cv2.waitKey(1) & 0xFF == 27:
            print(f"\nЗавершение. Всего морганий: {blink_count}")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Убедитесь, что установлена библиотека pyautogui
    # pip install pyautogui
    main()