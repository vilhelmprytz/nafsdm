# dns-manager
Manages DNS nodes and makes sure domains are saved in the slaves configs.

The master will always be running and be ready to accept connections from specified slaves. The slaves are set to fetch information from the master in a certain interval.

# Requirements
You need to have `python 2.7` installed with `django`.
