# Проект по ранжированию кандидатов для Газпром-Нефти

## Инструкция по ручной установке

### ! Обязательно должен быть запущен docker run -it -p 9200:9200 -p 9600:9600 -e OPENSEARCH_INITIAL_ADMIN_PASSWORD=bestteam1984A. -e "discovery.type=single-node"  --name opensearch-node opensearchproject/opensearch:latest !

### Обязательно поменять в файлах list_objects.py save_vacancy.py и llm_request_for_opensearch на адрес доступа к Opensearch hosts=[{"host": "localhost", "port": 9200}]
### Linux

```aiignore
git clone https://github.com/learn2pr0ge/bluetreasure.git
cd bluetreasure
```

Создание виртуального окружения

```aiignore
python -m venv venv_hackaton
source venv_hackaton/bin/activate
```
Установка пакетов

```aiignore
pip install -r requirements.txt
```

Запуск 

```aiignore
python app.py
```

Открывайте браузер 127.0.0.1:5000 и наслаждайтесь


### Windows

Убедитесь, что установлены Python и Git:
- **Python**: [python.org/downloads](https://www.python.org/downloads) — при установке обязательно отметьте галочку **"Add Python to PATH"**
- **Git**: [git-scm.com/download/win](https://git-scm.com/download/win)

Откройте **PowerShell** или **CMD** и выполните:

```bat
git clone https://github.com/learn2pr0ge/bluetreasure.git
cd bluetreasure
```

Создайте виртуальное окружение и активируйте его

```bat
python -m venv venv_hackaton
venv_hackaton\Scripts\activate
```

Установка пакетов

```bat
pip install -r requirements.txt
```

Запуск

```bat
python app.py
```

Открывайте браузер [127.0.0.1:5000](http://127.0.0.1:5000) и наслаждайтесь

> **Важно:** если PowerShell выдаёт ошибку при активации venv, выполните:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

## Инструкция по установке через docker-compose

### Обязательно поменять в файлах адрес доступа к Opensearch hosts=[{"host": "localhost", "port": 9200}], для запуска через docker-compose поменять на opensearch

#### Собрать

```aiignore
docker-compose build
```

#### Запустить

```aiignore
docker-compose up
```

