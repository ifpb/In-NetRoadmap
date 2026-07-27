from debian:trixie

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    procps \
    net-tools \
    iputils-ping \
    iproute2 \
    bash \
    curl \
    vlc \
    iperf3 \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i 's/geteuid/getppid/' /usr/bin/vlc

RUN mkdir -p /scripts
COPY m-system.sh /scripts/m-system.sh
COPY system /scripts/system

CMD /bin/bash
