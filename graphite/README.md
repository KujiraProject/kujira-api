Graphite configuration directory.

Calamari carbon-cache collects ceph metrics with whisper to dir: /var/lib/graphite

To install and configure graphite-web with grafana follow this steps:
vagrant up
1. yum install https://grafanarel.s3.amazonaws.com/builds/grafana-2.6.0-1.x86_64.rpm
2. systemctl enable grafana-server.service
3. reboot
4. yum install graphite-web -y
5. change in /etc/graphite-web/local-settings.py to STORAGE_DIR = '/var/lib/graphite'
	systemctl restart httpd
6. cd /var/lib/graphite; django-admin syncdb --settings graphite.settings

