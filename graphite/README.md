# This is graphite info directory

Calamari carbon-cache collects ceph metrics with whisper to dir: /var/lib/graphite

To install and configure graphite-web with grafana follow this steps:
vagrant up
1. 
```sh
yum install https://grafanarel.s3.amazonaws.com/builds/grafana-2.6.0-1.x86_64.rpm
```
2. 
```sh
systemctl enable grafana-server.service
```
3. 
```sh
reboot
```
4. 
```sh
yum install graphite-web -y
```
5. 
```sh 
change in /etc/graphite-web/local-settings.py to STORAGE_DIR = '/var/lib/graphite'
```
6. 
```sh
systemctl restart httpd
```
7. 
```sh
cd /var/lib/graphite; django-admin syncdb --settings graphite.settings
```
