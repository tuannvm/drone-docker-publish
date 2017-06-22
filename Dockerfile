FROM docker:17.05.0-ce-dind
RUN apk --update add py-pip bash curl tar docker git && \
   pip install awscli
WORKDIR /srv/
RUN cd $WORKDIR
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY entrypoint.py /usr/local/bin/
# COPY Dockerfile-test .
ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh", "/usr/local/bin/entrypoint.py"]