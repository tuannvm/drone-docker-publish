FROM docker:17.06.0-ce-dind
RUN apk --update add py-pip bash curl tar docker git && \
   pip install awscli
WORKDIR /srv/
RUN cd $WORKDIR
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY entrypoint.py /usr/local/bin/
RUN mkdir -p /lib/modules
# COPY Dockerfile-test .
ENTRYPOINT ["/usr/local/bin/entrypoint.py"]