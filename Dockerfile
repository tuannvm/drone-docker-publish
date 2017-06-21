FROM alpine:3.6
RUN apk --update add py-pip bash curl tar && \
   pip install awscli
ADD entrypoint
ENTRYPOINT ['./entrypoint.py']