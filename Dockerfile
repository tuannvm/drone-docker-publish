FROM alpine:3.6
RUN apk --update add py-pip bash curl tar && \
   pip install awscli
WORKDIR /srv/
ADD entrypoint.py $WORKDIR/
ENTRYPOINT ['/srv/entrypoint.py']