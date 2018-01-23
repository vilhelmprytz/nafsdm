# nafsdm-webinterface

This is a experimental webinterface for the nafsdm-master.

It runs on Flask and Gunicorn as webserver.

# Activation
Run the "enableInterface.sh" file. It will install the systemd service.

Start it as any other systemd service: "service nafsdm-webinterface start" or "systemctl start nafsdm-webinterface".

# Recommendations
We HIGHLY recommend running it behind a proxy such as nginx, with HTTPS. Just running the webinterface itself is NOT secure and should not be done in a production environment.
