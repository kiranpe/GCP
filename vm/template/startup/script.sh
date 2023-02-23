#!/bin/bash

sudo apt-get update && sudo apt-get autoclean

sudo apt-get install nginx -y && sudo systemctl start nginx

cat <<EOF > /var/www/html/index.html
<html>
<body>
<h1>Hello from $(hostname) $(hostname -I)</h1>
</body>
</html>
