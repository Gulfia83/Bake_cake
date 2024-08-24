# Bake_cake_bot
[Russian](RU_README.md)

Telegram bot for ordering cakes. With the bot, you can order TTRT from the presented catalog, or you can assemble the cake yourself from the presented parameters and ingredients. It is possible to change the delivery time and choose a convenient time slot. For an additional fee, you can add any inscription to the cake. With the bot, you can check the status of your orders. The bot sends notifications about new orders to the administrator.

### Examples of use

#### Start:

![старт](https://github.com/user-attachments/assets/a1f1ee3d-281b-4526-8111-5a4a11b3462a)

#### Choose from the cake catalog:

![выбор из готовых тортов](https://github.com/user-attachments/assets/55880f5b-775e-4de5-87ea-ca846eeee7f1)

#### Assemble a cake from the presented ingredients:

![собрать свой торт](https://github.com/user-attachments/assets/fc767e2c-a671-4af0-9403-5430c9f03246)

#### Ability to speed up delivery and choose the time

![возможность ускорить доставку и выбрать время](https://github.com/user-attachments/assets/dabe6e4c-1e3f-41ec-9fe3-cf7c0686a06f)

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

![админ панель клиента](https://github.com/user-attachments/assets/5d6c852a-0b15-4dcd-a124-eb9cfadee48b)

#### Cakes

![админка торты](https://github.com/user-attachments/assets/94341dc8-f8c7-48c6-9fc4-27fb84f15156)

### Project goal

Team project on the online course for web developers [dvmn.org](https://dvmn.org/).

---
Project was worked on by:
* [Gulfiya Vakhlakova](https://github.com/Gulfia83)
* [Stepan Makarov](https://github.com/Stmkv)
* [Magomed Saygidnurov](https://github.com/Magomed993)
* [Viktor Rykov](https://github.com/aqwarius2003)
