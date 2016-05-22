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
