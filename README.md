# dns-manager
Manages DNS nodes and makes sure domains are saved in the slaves configs. Runs on Python, Django.

The master will always be running and be ready to accept connections from specified slaves. The slaves are set to fetch information from the master in a certain interval.

# Requirements
You need to have `python 2.7` installed for the slaves.
For the master, the normal version is made with `Flask`, but that might not be secure in a production environment. Otherwise, you can also use `django` with `apache` (`mod_wsgi`).

For `django`:

`pip install django`

For `Flask`:

`pip install Flask`
