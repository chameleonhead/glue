FROM buildpack-deps:bullseye

# Install OpenJDK 8, Python zip
RUN wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add - \
    && echo "deb https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ bullseye main" >> /etc/apt/sources.list \
    && apt-get update \ 
    && apt-get install -y adoptopenjdk-8-hotspot python3 python3-pip zip \
    && apt-get clean \
    && rm -rf /var/tmp/* /tmp/* /var/lib/apt/lists/*

# Install python libs
RUN python3 -m pip install pyspark==3.1.1 boto3 pytest

# Install aws-cli
RUN wget -q -P /tmp https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip \
    && unzip -d /tmp /tmp/awscli-exe-linux-x86_64.zip \
    && /tmp/aws/install -i /usr/local/aws-cli -b /usr/bin \
    && rm -f /tmp/awscli-exe-linux-x86_64.zip

# Install maven
RUN wget -q -P /tmp https://aws-glue-etl-artifacts.s3.amazonaws.com/glue-common/apache-maven-3.6.0-bin.tar.gz \
    && mkdir /usr/share/maven \
    && tar -xzf /tmp/apache-maven-3.6.0-bin.tar.gz -C /usr/share/maven --strip-components=1 \
    && rm -f /tmp/apache-maven-3.6.0-bin.tar.gz \
    && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn
ENV MAVEN_HOME=/usr/share/maven M2_HOME=/usr/share/maven MAVEN_CONFIG=/home/.m2

# Install spark
RUN wget -q -P /tmp https://aws-glue-etl-artifacts.s3.amazonaws.com/glue-3.0/spark-3.1.1-amzn-0-bin-3.2.1-amzn-3.tgz \
    && mkdir /opt/spark \
    && tar -xf /tmp/spark-3.1.1-amzn-0-bin-3.2.1-amzn-3.tgz -C /opt/spark --strip-components=1 \
    && rm -f /tmp/spark-3.1.1-amzn-0-bin-3.2.1-amzn-3.tgz
ENV SPARK_HOME /opt/spark

# Install Glue
RUN wget -q -o /tmp/master.zip https://github.com/awslabs/aws-glue-libs/archive/refs/heads/master.zip \
    && unzip -d /tmp master.zip \
    && mv /tmp/aws-glue-libs-master /home/aws-glue-libs \
    && rm -f /tmp/master.zip \
    && chmod u+x /home/aws-glue-libs/bin/glue-setup.sh \
    && /home/aws-glue-libs/bin/glue-setup.sh
