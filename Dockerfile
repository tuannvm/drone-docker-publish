FROM docker:17.05.0-ce-dind
RUN apk --update add py-pip bash curl tar docker && \
   pip install awscli
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /srv/
RUN cd $WORKDIR
COPY entrypoint.py .
# COPY Dockerfile-test .
ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh", "/srv/entrypoint.py"]