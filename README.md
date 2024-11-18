# Установка:
1. Скачать папки assets and model по ссылке https://disk.yandex.com/d/MSUbYL4N0FYFYQ в проект.
2. Установить необходимые модули:
   ```
   ./python.sh -m pip install ftfy regex tqdmip
   ./python.sh -m pip install git+https://github.com/openai/CLIP.git
   ./python.sh -m pip install ultralytics
   ```
3. Изменить общий путь до проекта в переменной general_path расположенной в файле configs/main_config.py
# Работа с пайплайном:
```
alias PYTHON_PATH=~/.local/share/ov/pkg/isaac_sim-*/python.sh
в файле train.py/eval.py в переменной в функции gymnasium.make вставить версию (пример: tasks:rlmodel-v0):
Для пунктов 4.1.1 и 4.2 (Обучение на множественном выборе):
rlmodel-v0 - подход 1
rlmodel-v1 - подход 2
rlmodel-v2 - обучение с множественным выбором
Для пункта 4.2 (Обучение с картой знаний)
rlmodel-v0 - обучение на графе знаний
rlmodel-v1 - обучение без графа знаний
```
## обучение:
1. В переменной расположенной eval в файле configs/main_config.py установить значение False
```
PYTHON_PATH train.py
```
## инференс:
В в файле configs/main_config.py
1. выбрать в переменной load_policy модель, которую необходимо протестировать;
2. eval = True
3. задать радиус и угол начального отклонения eval_radius, eval_angle
```
PYTHON_PATH train.py
```
