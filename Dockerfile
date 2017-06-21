FROM alpine:3.6
RUN apk --update add py-pip bash curl tar && \
   pip install awscli
WORKDIR /srv/
cd $WORKDIR
ADD entrypoint.py .
ENTRYPOINT ['/srv/entrypoint.py']