The ITD Tool aims to support the formulation, validation and (re)orientation of documentary production ideas
and estimate how appealing these content creation ideas will be to potential audiences.
The ITD tool integrates existing tools for monitoring search trends, keyword research,
social media analytics.


Python dependencies extracted by pip freeze
alabaster==0.7.8
amqp==2.1.4
anyjson==0.3.3
appdirs==1.4.3
argh==0.26.1
Babel==2.1.1
backports-abc==0.4
backports.ssl-match-hostname==3.4.0.2
beautifulsoup4==4.5.3
billiard==3.5.0.2
celery==4.0.2
certifi==2015.11.20
cffi==1.5.2
colorama==0.3.6
contextlib2==0.5.1
cryptography==1.3.1
decorator==4.0.9
Django==1.8.5
django-cors-headers==1.1.0
djangorestframework==3.3.1
docutils==0.12
ecdsa==0.13
enum34==1.1.2
flower==0.8.3
funcsigs==0.4
future==0.15.2
futures==3.0.3
httpclient==0.0.2
idna==2.1
imagesize==0.7.1
ipaddress==1.0.16
Jinja2==2.8
junos-eznc==1.2.3
kombu==4.0.2
livereload==2.4.1
lxml==3.4.4
MarkupSafe==0.23
mock==1.3.0
mysqlclient==1.3.7
ncclient==0.5.3
netaddr==0.7.18
numpy==1.12.1
oauthlib==2.0.2
packaging==16.8
pandas==0.19.2
paramiko==1.16.0
passlib==1.6.5
Paste==2.0.3
pathtools==0.1.2
pbr==1.8.1
port-for==0.3.1
py==1.4.31
pyasn1==0.1.9
pycparser==2.14
pycrypto==2.6.1
pycryptodomex==3.4.2
Pygments==2.1.3
pyOpenSSL==16.0.0
pyparsing==2.2.0
pytest==2.8.7
python-dateutil==2.5.1
python-memcached==1.48
python-rest-client==0.3
pytrends==4.1.1
pytz==2017.2
PyYAML==3.11
raven==5.10.2
redis==2.10.5
repoze.who==2.2
requests==2.9.1
requests-oauthlib==0.8.0
scp==0.10.2
singledispatch==3.4.0.3
six==1.10.0
snowballstemmer==1.2.1
Sphinx==1.4.1
sphinx-autobuild==0.6.0
tornado==4.3
tweepy==3.5.0
vine==1.1.3
watchdog==0.8.3
WebOb==1.6.0
xmltodict==0.9.2
zope.interface==4.4.0



Steps to start the ITD service

1. Start redis
:/usr/local/sbin$ redis-server

2. Start rabbitmq
:/usr/local/sbin$ ./rabbitmq-server

3. Start Celery
~/PycharmProjects/itd_tool$ celery -A itdtool worker -l info

4. Start django
~/PycharmProjects/itd_tool$ python manage.py runserver

