# nafsdm
Manages DNS nodes and makes sure domains are saved in the slaves configs. Runs on Python and SSH.

*nafsdm stands for "not advanced, fast, simple dns manager"*

# Requirements
Requires python 2.

# How to install!
To install, you will need at least one slave and at least one master.

## Master
The master will handle most configuration and is the server all slaves connect to.

### Master install
On the master, create a new account if you haven't already with the command `useradd master-nafsdm`.
Then, copy over the data of `masterd/home/master-nafsdm` (GitHub) to your new users home dir (`/home/master-nafsdm`, locally). Please log in as the user (`su master-nafsdm`) or change owner for all files (`chown -R master-nafsdm:master-nafsdm /home/master-nafsdm`).

### Master setup
Run the daemon once so it creates the correct file system by typing `python /home/master-nafsdm/start.py` or just `./home/master-nafsdm/start.py` if it's executable.

## Slave(s)
The slave(s) will connect to the master and fetch latest domain information. Once the master daemon has been ran at least once, please transfer over the SSH keys to your slave(s) (read in `/home/master-nafsdm/log.log` for more info).

### Slave install
Same as on the master, create an account but name it `slave-nafsdm` (so `useradd slave-nafsdm` will be sufficient).
Then, copy over all the data from `slaved/home/slave-nafsdm` (GitHub) to your new users home dir (`/home/slave-nafsdm`, locally). And as for the master, please log in as the user when you do this or `chown` all the files in the home dir.
