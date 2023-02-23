#!/bin/bash

sudo apt-get update && sudo apt-get autoclean

sudo apt-get install nginx -y && sudo systemctl start nginx

cat <<EOF > /var/www/html/index.html
<html>
<body>
<h1>Hello from $(curl  -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/name")</h1>
</body>
</html>
