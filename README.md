# Bake_cake_bot
[Russian](RU_README.md)

A telegram bot for ordering cakes.

## Usage examples

Start:

Choose from a cake catalog:

Build a cake from the ingredients you choose:

## How to install

1. Clone the repository to your local computer.
2. Install the necessary packages using `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory of the project.
4. Add the following variables to the `.env` file:
- `TG_BOT_CAKE` - your telegram bot token.
- `SECRET_KEY` - Default: '' (empty string).
The secret key for installing Django. It is used to provide a cryptographic signature and must have a unique value.

django-admin startproject automatically adds a randomly generated SECRET_KEY to each new project.
- `ALLOWED_HOSTS` - Default: [] (empty list).
A list of strings representing the hostnames/domains that this Django site can serve. This is a security measure to prevent HTTP host header attacks, which are possible even with many seemingly safe web server configurations.
- `DEBUG` - One of the main functions of debug mode is to display detailed error pages. If your app throws an exception when DEBUG is True, Django will display a detailed traceback, including a lot of metadata about your environment, such as all currently defined Django settings (from settings.py)

5. Run migrations with:

```
python manage.py migrate
```
6. Create a superuser to work with the admin panel:

```
python manage.py createsuperuser
```
7. To get started with the admin panel:

```
python manage.py runserver
```

### Project Goal

Team project on the online course for web developers [dvmn.org](https://dvmn.org/).

---
Project was worked on by:
* [Gulfiya Vakhlakova](https://github.com/Gulfia83)
* [Stepan Makarov](https://github.com/Stmkv)
* [Magomed Saygidnurov](https://github.com/Magomed993)
* [Viktor Rykov](https://github.com/aqwarius2003)