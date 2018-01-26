# nafsdm-webinterface

This is a experimental webinterface for the nafsdm-master.

It runs on Flask and Gunicorn as webserver.

# Activation
Run the "enableInterface.sh" file. It will install the systemd service.

Start it as any other systemd service: "service nafsdm-webinterface start" or "systemctl start nafsdm-webinterface".

# Recommendations
We HIGHLY recommend running it behind a proxy such as nginx, with HTTPS. Just running the webinterface itself is NOT secure and should not be done in a production environment. We also recommend changing the HTTP auth password.

# Changing HTTP auth password
Open up the file named "interfacePassword.txt" using your edit of choice (i.e nano) and change the password to something else.

For the changes to take affect, restart the webinterface. "service nafsdm-webinterface restart".
