FROM ubuntu:18.04
MAINTAINER Eugene Kim <conankunioi@gmail.com>

RUN apt update
RUN apt install -y sudo

# Install dependencies
RUN apt install -y apt-transport-https

RUN apt install -y ca-certificates
RUN apt install -y gnupg
RUN apt install -y curl

# Install python3
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y python3-distutils

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

# Install NodeJS
RUN curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
RUN apt install -y nodejs

# Install Bazel
RUN curl https://bazel.build/bazel-release.pub.gpg | apt-key add - 
RUN echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list

RUN apt update
RUN apt install -y bazel=3.0.0

# Use alias blaze for bazel
RUN update-alternatives --install /usr/bin/blaze blaze /usr/bin/bazel 10

# Install git
RUN apt install -y git

# Store all files under "/app" in host OS.
VOLUME ["/app"]

# Expose 80, 443, and 3000 to host OS.
EXPOSE 80
EXPOSE 443
EXPOSE 3000

# Use "docker build --tag dev:${ver} ." to build an image.
# Use "docker container run -i -t -v /Users/eugenekim/workspace/scorpion:/app --name devenv dev:${ver}" to create a new container