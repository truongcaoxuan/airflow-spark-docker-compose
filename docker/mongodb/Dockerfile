FROM ubuntu:20.04

#------------------------------------------------
# Install MongoDB Community Edition on Ubuntu
# https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
#------------------------------------------------

# 1. Import the public key used by the package management system
RUN apt-get update && apt-get install -y wget gnupg curl

RUN curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
    sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
     --dearmor

# 2. Create a list file for MongoDB
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# 3. Reload local package database
RUN apt-get update 

# 4. Install the MongoDB packages
# 4.1 To install the latest stable version, issue the following
RUN apt-get install -y mongodb-org && apt-get clean

# 4.2 Install a specific release of MongoDB
# RUN sudo apt-get install -y mongodb-org=7.0 mongodb-org-database=7.0 mongodb-org-server=7.0 mongodb-mongosh=7.0 mongodb-org-mongos=7.0 mongodb-org-tools=7.0

RUN mkdir -p /data/db

EXPOSE 27017

ENTRYPOINT ["/usr/bin/mongod", "--bind_ip_all"]
