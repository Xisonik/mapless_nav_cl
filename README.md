Установка:
1. Скачать папки assets and model по ссылке https://disk.yandex.com/d/MSUbYL4N0FYFYQ в проект.
2. Установить необходимые модули:
   """
   ./python.sh -m pip install ftfy regex tqdmip
   ./python.sh -m pip install git+https://github.com/openai/CLIP.git
   ./python.sh -m pip install ultralytics
   """
3. Изменить общий путь до проекта в переменной general_path расположенной в файле configs/main_config.py

Работа с пайплайном:
alias PYTHON_PATH=~/.local/share/ov/pkg/isaac_sim-*/python.sh
обучение:
В переменной расположенной eval в файле configs/main_config.py установить значение False
PYTHON_PATH train.py
инференс:
В переменной расположенной eval в файле configs/main_config.py установить значение True
В load_policy заменить название модели, которую необходимо использовать.
PYTHON_PATH train.py
