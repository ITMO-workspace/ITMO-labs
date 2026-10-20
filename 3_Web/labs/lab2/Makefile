# HTTP_CONF=~/httpd-root/conf/httpd.conf
HTTP_CONF=~/Code/ITMO-labs/3_Web/labs/lab2/httpd-root/conf/httpd.conf

FCGI_PORT=2201

SERVER_PORT=24000

JAR=server/target/server.jar

FCGI_LIB = server/lib/fastcgi-lib.jar

all: run

install_fastcgi:
	mvn install:install-file \
  -Dfile=$(FCGI_LIB) \
  -DgroupId=com.example \
  -DartifactId=fastcgi-lib \
  -Dversion=1.0.0 \
  -Dpackaging=jar

build: install_fastcgi
	mvn -f server/pom.xml clean package

run:
	httpd -f $(HTTP_CONF) -k start
	
	java -DFCGI_PORT=$(FCGI_PORT) -jar $(JAR)

stop:
	httpd -f $(HTTP_CONF) -k stop

test:
	curl -i "http://localhost:$(SERVER_PORT)/fcgi-bin/server.jar?x=1&y=2&r=3"