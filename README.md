# nafsdm
**Current status: UNSTABLE (nafsdm is not yet finished)**

Manages DNS nodes and makes sure domains are saved in the slaves configs. Runs on Python and SSH.

*nafsdm stands for "not advanced, fast, simple dns manager"*

# Requirements
Requires python 2 & 'requests' module (installer installs these automatically)

# Installation
To install, you will need at least one slave and at least one master. All slaves will connect to the master under a certain interval.

nafsdm now has install scripts for both master and slaves.

## Master installation
Connect to your master server, and download the installation script.

`wget https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/setupMaster.sh`

It also needs to be executable.

`chmod +x setupMaster.sh`

Now run the installer. The installer will guide you through the steps.

`./setupMaster.sh`

Once it's finished, run the master daemon once to it generates keys (as the installer says).

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

You're done! You should now be able to start the slave (if everything is correctly configured).
`service nafsdm-slave start`

Replace start with stop or restart if you would like to do that later on (or status to check if it's running)

If anything fails, you can check the log.
`cat /home/slave-nafsdm/log.log`
