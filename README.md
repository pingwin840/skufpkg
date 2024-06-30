# skufpkg

`skufpkg` is a simple package manager for Linux. It allows you to manage software packages using a custom `.skufpkg` format.

`skufpkg` — это простой менеджер пакетов для Linux. Он позволяет управлять программными пакетами с использованием собственного формата `.skufpkg`.


## Installation / Установка

To install `skufpkg`, run:

Чтобы установить `skufpkg`, выполните:

    python setup.py install

## Usage / Использование

### Adding a Repository / Добавление репозитория

To add a repository, use:

Чтобы добавить репозиторий, используйте:

    skufpkg add-repo <repository-url>

### Listing Repositories / Список репозиториев

To list all repositories, use:

Чтобы перечислить все репозитории, используйте:

    skufpkg list-repos

### Searching for Packages / Поиск пакетов

To search for a package in repositories, use:

Чтобы найти пакет в репозиториях, используйте:

    skufpkg search <package-name>

### Installing a Package / Установка пакета

To install a package, use:

Чтобы установить пакет, используйте:

    skufpkg install <package-name>

### Removing a Package / Удаление пакета

To remove an installed package, use:

Чтобы удалить установленный пакет, используйте:

    skufpkg remove <package-name>

### Listing Installed Packages / Список установленных пакетов

To list all installed packages, use:

Чтобы перечислить все установленные пакеты, используйте:

    skufpkg list-installed

### Creating a Package / Создание пакета

To create a `.skufpkg` package, use:

Чтобы создать пакет `.skufpkg`, используйте:

    skufpkg create-pkg <source-directory> <package-name> <version>

### Starting a Repository Server / Запуск сервера репозитория

To start a repository server, use:

Чтобы запустить сервер репозитория, используйте:

    skufpkg start-server --host 0.0.0.0 --port 5000

This will start a server on `http://<host>:<port>` serving your `.skufpkg` files. By default, it serves files from the `packages` directory.

Это запустит сервер по адресу `http://<host>:<port>`, обслуживающий ваши файлы `.skufpkg`. По умолчанию он обслуживает файлы из директории `packages`.

To add this repository to `skufpkg`, use:

Чтобы добавить этот репозиторий в `skufpkg`, используйте:

    skufpkg add-repo http://<host>:<port>

Make sure to place your `.skufpkg` files in the `packages` directory before starting the server.

Убедитесь, что вы разместили свои файлы `.skufpkg` в директории `packages` перед запуском сервера.

### Running Tests / Запуск тестов

To run the tests, execute the following command in the root directory:

Чтобы запустить тесты, выполните следующую команду в корневом каталоге:

    python -m unittest discover -s tests

