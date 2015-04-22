#!/bin/sh -e

apt-get install -y python-pip python-dev build-essential

# install more packages
apt-get install -y libffi-dev libxml2-dev libxslt1-dev

# install docker
wget -qO- https://get.docker.com/ | sh

# setup a virutal environment
pip install virtualenv
virtualenv DEV
. DEV/bin/activate

# install developpment tools
pip install scrapy
pip install scrapyjs
pip install selenium
pip install sqlalchemy
pip install scales

# IPython for scrapy shell
pip install --upgrade ipython[all]
pip install jinja2

# install splash Docker image
docker pull scrapinghub/splash
docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash

# install elasticsearch https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-on-an-ubuntu-vps
# pipe scrapy to elasticsearch http://blog.florian-hopf.de/2014/07/scrapy-and-elasticsearch.html
