# nafsdm
**Current status: STABLE, version 1.2.4-stable**

Manages DNS nodes and makes sure domains are saved in the slaves configs. Runs on Python and SSH.

*nafsdm stands for "not advanced, fast, simple dns manager"*

# Prerequisites & Compatibility
Before installing nafsdm, make sure you have at least one master and one slave. The master needs to have SSH open (at least a firewall that only allows your slave IP's) and all slaves need to have bind already configured (**nafsdm DOES NOT install bind for you**)

nafsdm is tested to work with the following operating systems:

* Debian 8, 9 (7 should work fine)
* Ubuntu 16.04.2 (old versions like 14.04 should also work fine, but may lack systemd)
* CentOS 7

# Installation
To install, you will need at least one slave and one master. All slaves will connect to the master at a certain interval.

nafsdm now has install scripts for both master and slaves.

## Master installation
Connect to your master server, and download the installation script.

`wget https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/setupMaster.sh`

The file also needs to be executable.

`chmod +x setupMaster.sh`

Now run the installer. The installer will guide you through the steps.

`./setupMaster.sh`

Once it's finished, run the master daemon once, as it will generate keys (as the installer says).

`nafsdm-master`

Now, copy the SSH key contents somewhere to your computer as it will be needed on the slaves later on (as the output says).

`cat /home/master-nafsdm/.ssh/nafsdm_rsa` (this will print the key)

The master installation is now finished and should be ready to use. You can use `nafsdmctl` to add/remove domains.

## Slave installation
You will have to perform these steps on every slave you would like to install this on.
Connect to your slave and download the installation script.

`wget https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/setupSlave.sh`

The file also need to be executable.

`chmod +x setupSlave.sh`

Now run the slave installer. The installer will guide you through the steps.

`./setupSlave.sh`

Once it's finished, you can open up the config with your editor of choice (example below uses nano) to set it up correctly.

`nano /home/slave-nafsdm/config.conf`


Here is an explanation of what every option is.

`host` = hostname / IP for the master node we confgiured earlier

`user` = the username where nafsdm on the master installed. By default, it's master-nafsdm.

`update_interval` = how often the slave will update it's configuration (seconds).

`type` = type of the slave system. Is it ubuntu, debian or centos?

`bindPath` = path of configuration file nafsdm will write to (bind configuration)

`nodeName` = name of this node

Once that's done, you can paste over the SSH key you saved earlier to the slave. Paste it in to the file mentioned below.

`nano /home/slave-nafsdm/.ssh/master_key`

The key also needs to have correct permissions.

`chmod 600 /home/slave-nafsdm/.ssh/master_key` (nafsdm will NOT work if the correct permissions are not used)

You're done! You should now be able to start the slave (if everything is correctly configured).

`service nafsdm-slave start`

Replace start with stop or restart if you would like to do that later on (or status to check if it's running)

If anything fails, you can check the log.

`cat /home/slave-nafsdm/log.log`

When running the slave the first time, you will probably have to accept the "fingerprint". To accept it, stop the daemon.

`service nafsdm-slave stop`

And run the slave in debug mode, which will let you accept the fingerprint.

`python /home/slave-nafsdm/pythondaemon/__main__.py`

When it asks you, just type "yes" and hit enter. When it's done, hit Control+C to stop the daemon and then boot the daemon back up again using service (as usual). It should look something like this:

`The authenticity of host 'example.example (0.0.0.0)' can't be established.`

`ECDSA key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.`

`Are you sure you want to continue connecting (yes/no)?`

# Upgrading

To upgrade, please refer to the following wiki page: <https://github.com/MrKaKisen/nafsdm/wiki/Upgrading>

# Contributing
I gladly accept any pull requests that looks good! Just make sure you're working in the "development" branch and that you state in the request what you've modified and why. And don't create any new bugs :).

# Author
Email: contact@mrkakisen.net

nafsdm - Fast & easy DNS node manager for bind
Copyright (C) 2017 Vilhelm Prytz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
