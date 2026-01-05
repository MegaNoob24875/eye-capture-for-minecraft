РУССКИЙ:
- ВАЖНО -
 перед запуском скрипта, нужно скачать эти библиотеки:
Питон(Пайтон) версия 3.10.0 писалось и тестировалось в программе py charm 2025.2.2 (лучше всего запускать как раз через это приложение)
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pyautogui
time - встроенная библиотека Python для работы со временем
collections - встроенная библиотека Python (используется deque)
 ЕСЛИ СЛИШКОМ СИЛЬНО СМОТРЕТЬ ВНИЗ, СКРИПТ ПОСЧИТАЕТ ЭТО ЗА МОРГАНИЕ!
так же, перед запуском скрипта поставьте английскую расскладку иначе скрипт не будет нажимать клавишу q при моргании.

если вылезает такая ошибка C:\Users\\PycharmProjects\PythonProject431232\.venv\Scripts\python.exe "C:\\\OneDrive\Рабочий стол\blink_detector.py" 
Traceback (most recent call last):
  File "C:\Users\\OneDrive\Рабочий стол\blink_detector.py", line 9, in <module>
    mp_face_mesh = mp.solutions.face_mesh
AttributeError: module 'mediapipe' has no attribute 'solutions'

Process finished with exit code 1

То нужно сделать полную переустановку Mediapipe

# Удалите старую версию
pip uninstall mediapipe -y

# Установите свежую версию
pip install mediapipe --upgrade

# Или конкретную версию (РЕКОМЕНДУЮ)
pip install mediapipe==0.10.8 (если не работает свежая версия)

так же лучше всего сделать путь без русских букв и всяких символов







English:
- IMPORTANT -
 before running the script, you need to download these libraries:
Python version 3.10.0 written and tested in the py charm 2025.2.2 program (it's best to launch it through this app)
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pyautogui
time - built-in Python library for working with time
collections - built-in Python library (deque is used)
 IF YOU LOOK DOWN TOO MUCH, THE SCREEN WILL CONSIDER IT AS A BLINK!
Also, before running the script, set the keyboard layout to English, otherwise the script will not press the q key when you blink.

if you get this error: C:\Users\\PycharmProjects\PythonProject431232\.venv\Scripts\python.exe "C:\\\OneDrive\Рабочий стол\blink_detector.py" 
Traceback (most recent call last):
 File "C:\Users\OneDrive\Рабочий стол\blink_detector.py", line 9, in <module>
 mp_face_mesh = mp.solutions.face_mesh
AttributeError: module 'mediapipe' has no attribute 'solutions'

Process finished with exit code 1

You need to do a full reinstallation of Mediapipe

# Uninstall the old version
pip uninstall mediapipe -y

# Install the latest version
pip install mediapipe --upgrade

# Or a specific version (RECOMMENDED)
pip install mediapipe==0.10.8 (if the latest version doesn't work)

It's also best to use a path without Russian letters or any other characters


