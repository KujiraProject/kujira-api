[![ZenHub] (https://raw.githubusercontent.com/ZenHubIO/support/master/zenhub-badge.png)] (https://zenhub.io)
[![Code Health](https://landscape.io/github/KujiraProject/kujira-api/develop/landscape.svg?style=flat)](https://landscape.io/github/KujiraProject/kujira-api/develop)
[![Coverage Status](https://coveralls.io/repos/github/KujiraProject/kujira-api/badge.svg?branch=master)](https://coveralls.io/github/KujiraProject/kujira-api?branch=master)


# kujira-api
API service for Kujira written in Flask and Python.

Websocket dependencies:
   pip install eventlet
   pip install Flask
   pip install flask-socketio

How to run server:
   sudo python kujira-api/server.py

The server starts at the address: localhost:5000. 
To change the address of the host you have to edit
   kujira-api/config.py

## Kujira parser
Kujira parser is a python script intended to run as daemon on machine with Salt Mater server on it. It's purpose is to handle kujira related events fetched from salt event bus. Right now it pushes json reprezentation of example events into redis queue.

Logs are saved to /var/log/kujira/event_parser.log
### Prerequisities
Kujira parser python script depends on kujira.store python package. Therefore, said package must be present on the machine. Also redis server should be up and running.
### Installing
For kujira parser deamon to work you must prepare systemctl service script:

Copy kujira-parser.service into /usr/lib/systemd/system/

Open kujira-parser.service in text editor

Modify line:
```sh
ExecStart=/usr/bin/python /srv/salt/scripts/kujira_parser.py
```
so it points to kujira_parser.py

Modify
```sh
PYTHONPATH=/vagrant/linked/kujira_python_path
```
so that PYTHONPATH points to directory that contains kujira.store python package

### Usage
Before first usage you must reload systemd, scanning for new or changed units:
```sh
$ systemctl daemon-reload
```
After that you can start daemon:
```sh
$ systemctl start kujira-parser
```
stop daemon:
```sh
$ systemctl stop kujira-parser
```
restart daemon:
```sh
$ systemctl restart kujira-parser
```
or  configure service to be automatically started at boot time:
```sh
$ systemctl enable kujira-parser
```
You can find more information about systemctl at [systemctl man page](https://www.freedesktop.org/software/systemd/man/systemctl.html)
