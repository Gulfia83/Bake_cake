# Bake_cake_bot
[Russian](RU_README.md)

Telegram bot for ordering cakes. With the bot, you can order TTRT from the presented catalog, or you can assemble the cake yourself from the presented parameters and ingredients. It is possible to change the delivery time and choose a convenient time slot. For an additional fee, you can add any inscription to the cake. With the bot, you can check the status of your orders. The bot sends notifications about new orders to the administrator.

### Examples of use

#### Start:

![старт](https://github.com/user-attachments/assets/866e1a14-f558-43c1-8e47-daa0c361a9d3)

#### Choose from the cake catalog:

![выбор из готовых тортов](https://github.com/user-attachments/assets/9fd4ce25-057b-4ee0-a234-447691f63e0f)

#### Assemble a cake from the presented ingredients:

![собрать свой торт](https://github.com/user-attachments/assets/8806e15c-a220-47f5-893b-a6e86b01d6be)

#### Ability to speed up delivery and choose the time

![возможность ускорить доставку и выбрать время](https://github.com/user-attachments/assets/e635feb4-f244-4413-998c-108dd2e3768b)

## How to install

1. Clone the repository to your local computer.
2. Install the necessary packages using `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory of the project.
4. Add the following variables to the `.env` file:
- `TG_BOT_TOKEN` - your telegram bot token.
- `TG_CHAT_ID` - Telegram ID of the admin (who will receive notifications about new orders)
- `SECRET_KEY` - Default: '' (empty string).
Secret key for Django installation. It is used to provide cryptographic signature and must have a unique value.

django-admin startproject automatically adds a randomly generated SECRET_KEY to each new project.
- `ALLOWED_HOSTS` - Default: [] (empty list).
List of strings representing hostnames/domains that this Django site can serve. This is a security measure to prevent HTTP host header attacks, which are possible even with many seemingly safe web server configurations.
- `DEBUG` - One of the main functions of debug mode is to display detailed error pages. If your app throws an exception when DEBUG is True, Django will display a detailed traceback, including a lot of metadata about your environment, such as all currently defined Django settings (from settings.py)

5. Run migrations with:

```
python manage.py migrate
```
6. Create a superuser to work with the admin panel:

```
python manage.py createsuperuser
```
7. To get started in the admin panel:

```
python manage.py runserver
```
### Example of display in the admin panel

#### Customers and their orders

![админ панель клиента](https://github.com/user-attachments/assets/5e7ff27b-827a-40dd-96f6-a1b42af1f88e)

#### Cakes

![админка торты](https://github.com/user-attachments/assets/b4ee1ae8-b8b1-4c5a-8cc4-a0d68231a05d)

### Project goal

Team project on the online course for web developers [dvmn.org](https://dvmn.org/).

---
Project was worked on by:
* [Gulfiya Vakhlakova](https://github.com/Gulfia83)
* [Stepan Makarov](https://github.com/Stmkv)
* [Magomed Saygidnurov](https://github.com/Magomed993)
* [Viktor Rykov](https://github.com/aqwarius2003)
