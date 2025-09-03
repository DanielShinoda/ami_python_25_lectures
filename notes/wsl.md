# WSL

## Вступление

Начиная с Windows 10 доступна WSL (Windows Subsystem for Linux), позволяющая запускать Linux‑окружение прямо в Windows. Установка WSL занимает немного времени (рекомендуется WSL 2), а в VS Code есть полноценная интеграция через расширение Remote – WSL.

## Quick start

Полная инструкция https://learn.microsoft.com/ru-ru/windows/wsl/install:

0. (Рекомендуется, но необязательно) Установить [Windows Terminal](https://www.microsoft.com/store/apps/9n0dx20hk701), чтобы красиво пользоваться терминалом на Windows.
1. Открыть PowerShell в режиме администратора и выполнить `wsl --install`, перезапустить компьютер.
2. Открыть PowerShell и выполнить `wsl --install -d Ubuntu-20.04`.
3. Запустить Ubuntu-20.04 ([все способы](https://learn.microsoft.com/ru-ru/windows/wsl/install#ways-to-run-multiple-linux-distributions-with-wsl)).
4. Если вы используете VSCode, то он автоматически предложит использовать WSL. [WSL в VSCode](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode).


## P.S.

Рекомендую со временем перейти на Linux для разработки (лично использую Ubuntu). Не обязательно удалять Windows: можно настроить двойную загрузку (dual boot). Для установки воспользуйтесь одним из руководств по запросу "ubuntu dual boot windows". Перед началом обязательно сделайте резервную копию данных.

По интеграции WSL с CLion я не даю гарантий, поэтому целесообразно использовать VS Code (например, с расширением Remote – WSL) или "терминальные" редакторы вроде vim/neovim.
