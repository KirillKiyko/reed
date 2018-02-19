*REED

**Setup Environment

For using REED need to  install Python 3.5.2

***Install Newspaper

Install pip3 command needed to install newspaper3k package:

```
sudo apt-get install python3-pip
```

Python development version, needed for Python.h:

```
sudo apt-get install python-dev
```

lxml requirements:

```
sudo apt-get install libxml2-dev libxslt-dev
```

For PIL to recognize .jpg images:

```
sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev
```

NOTE: If you find problem installing libpng12-dev, try installing libpng-dev.

Install the distribution via pip:

```
pip3 install newspaper3k
```

Install requirements.txt:

```
sudo pip install -r requirements.txt
```

** Run Project

Create database:

```
python3 create_table.py
```

Create admin-user:

In file create_user.py change fild 'status' from 'user' to 'admin'

Run server.py:

```
python3 server.py
```

Registrate your user in fild 'Sign up'

Then log out and change status from 'admin' to 'user' in create_user.py

After all this steps you can create users.
