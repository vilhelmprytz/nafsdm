# dns-manager
Manages DNS nodes and makes sure domains are saved in the slaves configs. Runs on Python, Django.

The master will always be running and be ready to accept connections from specified slaves. The slaves are set to fetch information from the master in a certain interval.

# Requirements
You need to have `python 2.7` installed. For the master, you need to have it installed with `django` and have `apache` installed with `mod_wsgi`.

For `django`:

`pip install django`

For `mod_wsgi`:

`sudo apt-get install libapache2-mod-wsgi`
