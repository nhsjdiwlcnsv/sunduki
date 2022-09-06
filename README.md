# SUNDUKI - MineRL AI Debil

## Repo Structure

- **bin** - main binstubs for the project
- **djangoReact** - code of the django project
- **mainapp** - code of models/views for django
- **mainapp-ui** - code of the main React app
- **static** - project statics ( + from React App ) 

## Setup

Be sure to execute commands in zsh (Binstubs not optimised for Windows. I've tried...)

1. Run `bin/setup`
2. Run `bin/start/app` to run application in localhost
3. Open [React App : 127.0.0.1:8000](http://127.0.0.1:8000/)

## binstubs

This project includes my own binstubs so fell free to use them ;)

Here is a list with some of them:

1. If your using VScode feel free to use `bin/code` to open project code.
2. `bin/migrate` command to apply migrations to db.
3. `bin/build` to create statics for application.

See [bin/folder](bin) for available binstubs.

## Running Application

### If you want to look through db models and create some by yourself - create admin:

1. Run `source envs/bin/acitvate`.
2. Run `python manage.py createsuperuser` and fill the form.
3. Visit [Project/Admin/desk](http://127.0.0.1:8000/admin)
4. Log in as an Admin with login + password from the form.

#### To make changes in React App:

1. `bin/build` create build out from `mainapp-ui` react app. It makes sense to run it every time after you made changes in `mainapp-ui/folder`
   1.1 If your changes didn't apply after `bin/build`, try stopping the application server and run the command `python manage.py collectstatic`

#### To make changes in Django:

1. Be sure to `Ctrl+C` old connection.
2. Run `bin/start/server` to run server once again.

## Development

1. Run `bin/start/dev`. (If you're using VScode)
2. Look through the source code. Enjoy :).