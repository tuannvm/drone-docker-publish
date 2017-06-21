FROM alpine:3.6
RUN apk --update add py-pip bash curl tar docker && \
   pip install awscli
WORKDIR /srv/
RUN cd $WORKDIR
COPY entrypoint.py .
ENTRYPOINT ["/srv/entrypoint.py"]