# This is graphite info directory

Calamari carbon-cache collects ceph metrics with whisper to dir: /var/lib/graphite

To install and configure graphite-web with grafana follow this steps:
vagrant up
```sh
yum install https://grafanarel.s3.amazonaws.com/builds/grafana-2.6.0-1.x86_64.rpm
```
```sh
systemctl enable grafana-server.service
```
```sh
reboot
```
```sh
yum install graphite-web -y
```
```sh 
change in /etc/graphite-web/local-settings.py to STORAGE_DIR = '/var/lib/graphite'
```
```sh
systemctl restart httpd
```
```sh
cd /var/lib/graphite; django-admin syncdb --settings graphite.settings
```

