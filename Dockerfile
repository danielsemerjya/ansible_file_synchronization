# FROM centos:latest
FROM python:3.9-alpine
# TODO: create minimialic image for tests by using alpine distribution
RUN   apk update && \
      apk add --no-cache \
      openssh-keygen \
      rsync \
      openssh \
      openssh-server \
      nano \
      openrc

ENV PYTHONUNBUFFERED=1
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install pexpect

WORKDIR /
RUN "rc-status"
RUN touch /run/openrc/softlevel
RUN ["rc-update", "add", "sshd"]
RUN "rc-status"
RUN ["/etc/init.d/sshd", "start"]
RUN ["/etc/init.d/sshd", "restart"]
RUN ["rsync", "--daemon"]
RUN echo "root:root" | chpasswd

EXPOSE 22
# EXPOSE 873

# rsync -avzh root@172.17.0.3:/tmp/foo /tmp/foo

# rsync -avzh root@172.17.0.2:/tmp/foo /tmp/foo


