FROM adoptopenjdk/openjdk11:alpine 
RUN apk add curl
ADD ping.sh /ping.sh
CMD [ "/bin/sh", "/ping.sh" ]
