FROM docker:17.06.0-ce-dind
RUN apk --update add py-pip bash curl tar docker git && \
   pip install awscli
WORKDIR /srv/
RUN cd $WORKDIR
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY entrypoint.py /usr/local/bin/
COPY entrypoint.sh /usr/local/bin/
COPY supervisord.conf /etc/
RUN mkdir -p /lib/modules && \
    mkdir -p /var/log/supervisord/
# COPY Dockerfile-test .
ENTRYPOINT ["/usr/local/bin/entrypoint.py"]