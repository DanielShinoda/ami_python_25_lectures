# Visual Studio Code

## Установка

Переходим по [ссылке](https://code.visualstudio.com/), скачиваем и устанавливаем.

## После установки

Откройте VS Code.

Открытие папки:
- File -> Open Folder -> выберите директорию, в которой хотите работать.

Создание файлов:
- В левой панели Explorer: правый клик по папке проекта -> New File -> укажите имя файла.

Запуск:
- Запуск по кнопке ▶️ возможен после установки расширения Code Runner: https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner.
- Этот способ я не рекомендую; предпочтительнее запуск из терминала (shell). См. раздел: [shell](shell.md).

## Плагины

Для комфортной работы в VS Code рекомендуются следующие расширения (подробности — в их описаниях на Marketplace):
- [Python Extension Pack](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack), для IntelliSense (Pylance), Linting;
- [Code Runner](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner) для запуска питон скрипта из интерфейса `VsCode`.
- [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) для того, чтобы открывать тетрадки.
- [Sort lines](https://marketplace.visualstudio.com/items?itemName=Tyriar.sort-lines) - опционально, позволяет сортировать строки в файле. Надо выделить и нажать `F9`. Я в основном пользуюсь для того, чтобы сортировать импорты.
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) - black форматер, вообще black это утилита которая форматирует python код, скорее всего если вы им будете пользоваться то на контесте все будет проходить, но хочется заметить, что [black нарушает pep8](https://github.com/psf/black/issues/1178?ysclid=m0p8xjbrzq927128426). Смотри также [black](black.md)
- [isort][https://marketplace.visualstudio.com/items?itemName=ms-python.isort] - сортирует импорты, я лично не пользуюсь этим расширением, я пользуюсь [Sort lines](https://marketplace.visualstudio.com/items?itemName=Tyriar.sort-lines). Смотри также [isort](isort.md)

## Полезные комбинации клавиш

- [Windows](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)
- [MacOS](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf)
- [Linux](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf)

Ниже — полезные клавиатурные сочетания. Я привожу варианты для Linux/Windows:
- `Ctrl + O` - открыть файл.
- `Ctrl + P` - перейти к файлу, если написать `:` и номер строки (можно -1, если нужно в конец файла), то перейдете к строке.
- `Ctrl + Shift + P` - тоже самое, что `Ctrl + P` и написать `>`. Это откроет вам `command palette` (извиняйте русский перевод мне не нравится). Здесь можно перезагрузить окно - `Developer: Reload windows`, открыть настройки шорткатов `Preferences: Open Keyboard Shortcuts`, изменение темы `Preferences: Color Theme` и т.д. Также можно пользоваться штуками из плагинов, - просто начните писать название плагина и оно вам покажет, что доступно.
- `Ctrl + ЛКМ` по слову в коде или `F12` - часто говорят прямо на английском `Go to definition`, что в переводе и значит переход к определению чего-либо.
- `Ctrl + B` - открывает/закрывает левую панель.
- `Ctrl + ~` - открывает/закрывает терминал.
- `Ctrl + K Z` - включает/выключает Zen Mode. Также можно два раза нажать `Esc`, чтобы выйти.
- `Ctrl + Space` - автодополнение в коде.
- `F2` - рефакторинг - надо выделить нужную переменную и нажать F2, тогда можно будет переименовать ее везде (на самом деле неправда, но почти все переименовывает).
- `Ctrl + D` - выделите текст и нажмите эту комбинацию, тогда при каждом нажимании курсор будет размножаться на выделенный вами текст.
- `Ctrl + ↑`, `Ctrl + ↓` - переместить курсор вверх/вниз.
- `Ctrl + L` - выделить строку.
- `Ctrl + X` - вырезать строку.
- `Ctrl + /` - закомментировать строку кода.
- `Alt + Z` - включить режим `word wrap`.
- `Shift + Alt + F` - форматнуть документ. Нажмите эту комбинацию в `.py` файле, тогда расширение [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) предложит вам скачать один из форматеров. Я пользуюсь `black`, так как у нас им пользуются на работе. Таким образом можно будет быстро поправлять ваш код на `PEP8`.

## Открыть VSCode из терминала

```bash
code /home/chopik/python
```

Для открытия папки в VS Code из терминала используйте команду `code <путь_к_директории>`. Если путь не указан, будет открыта текущая директория. См. также: [Ссылка на базовые команды в терминале](terminal.md).


## Автоматическое удаление лишних пробелов в конце строк

https://bobbyhadz.com/blog/remove-trailing-whitespace-vscode

## Автоматическое добавление последней пустой строки в файле

https://stackoverflow.com/questions/44704968/visual-studio-code-insert-newline-at-the-end-of-files
