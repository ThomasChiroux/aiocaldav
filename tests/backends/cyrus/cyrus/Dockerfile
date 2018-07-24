FROM debian:latest
MAINTAINER Cyrus Works <docker@cyrus.works>

RUN echo "CyrusWorksManualCacheInvalidationString000006"

RUN apt-get update && apt-get -y install \
    autoconf \
    automake \
    autotools-dev \
    bash-completion \
    bison \
    build-essential \
    clang \
    cmake \
    comerr-dev \
    doxygen \
    debhelper \
    flex \
    g++ \
    git \
    gperf \
    graphviz \
    groff \
    texi2html \
    texinfo \
    heimdal-dev \
    help2man \
    libanyevent-perl \
    libbsd-dev \
    libbsd-resource-perl \
    libclone-perl \
    libconfig-inifiles-perl \
    libcunit1-dev \
    libdatetime-perl \
    libdb-dev \
    libdigest-sha-perl \
    libencode-imaputf7-perl \
    libfile-chdir-perl \
    libfile-slurp-perl \
    libglib2.0-dev \
    libical-dev \
    libicu-dev \
    libio-socket-inet6-perl \
    libio-stringy-perl \
    libjansson-dev \
    libjson-perl \
    libjson-xs-perl \
    libldap2-dev \
    libmagic-dev \
    libmilter-dev \
    default-libmysqlclient-dev \
    libnet-server-perl \
    libnews-nntpclient-perl \
    libnghttp2-dev \
    libpath-tiny-perl \
    libpam0g-dev \
    libpcre3-dev \
    libsasl2-dev \
    libsasl2-modules \
    libsasl2-modules-gssapi-mit \
    libsnmp-dev \
    libsqlite3-dev \
    libssl1.0-dev \
    # libssl-dev \
    libstring-crc32-perl \
    libtest-deep-perl \
    libtest-deep-type-perl \
    libtest-most-perl \
    libtest-unit-perl \
    libtool \
    libunix-syslog-perl \
    liburi-perl \
    libxml-generator-perl \
    libxml-xpath-perl \
    libxml2-dev \
    libwrap0-dev \
    libxapian-dev \
    libzephyr-dev \
    libmariadb-dev \
    liblmdb-dev \
    libperl-dev \
    lsb-base \
    net-tools \
    pandoc \
    perl \
    php-cli \
    php-curl \
    pkg-config \
    po-debconf \
    python-docutils \
    sasl2-bin \
    # ssl-cert-dev \
    sudo \
    tcl-dev \
    # tcp-wrappers \
    transfig \
    uuid-dev \
    valgrind \
    vim \
    wamerican \
    wget \
    xutils-dev \
    zlib1g-dev \
    rsyslog

RUN apt-get install "cmake" -y

RUN dpkg -l

RUN sed -r -i \
    -e 's/^"([^ ]|\s{2})(.*)$/\1\2/g' \
    -e 's/^set background=dark/"set background=dark/g' \
    /etc/vim/vimrc

RUN groupadd -r sasl ; \
    groupadd -r mail ; \
    useradd -c "Cyrus IMAP Server" -d /var/lib/imap \
    -g mail -G sasl -s /bin/bash -r cyrus

WORKDIR /srv
RUN git config --global http.sslverify false && \
    git clone https://github.com/cyrusimap/cyrus-imapd.git \
    cyrus-imapd.git

RUN git config --global http.sslverify false && \
    git clone https://github.com/cyrusimap/cyruslibs.git \
    cyruslibs.git

RUN git config --global http.sslverify false && \
    git clone https://github.com/ThomasChiroux/python-cyrus.git \
    python-cyrus.git

RUN cpan Term::ReadLine

RUN cpan Math::Int64

RUN cpan -l

WORKDIR /srv/cyruslibs.git
RUN git fetch
RUN git checkout origin/master
RUN git submodule init
RUN git submodule update
RUN ./build.sh

WORKDIR /srv/cyrus-imapd.git
RUN git fetch
RUN git checkout origin/master
RUN git checkout cyrus-imapd-3.0.7 
RUN autoreconf -i -s
RUN ./configure CFLAGS="-W -Wno-unused-parameter -g -O0 -Wall -Wextra -Werror -fPIC" \
    --enable-autocreate --enable-http --enable-calalarmd --prefix=/usr/cyrus
RUN make lex-fix
RUN make
RUN make install

COPY imapd.conf /etc/
COPY cyrus.conf /etc/
COPY saslauthd /etc/default/
COPY initdirs /
COPY entrypoint.sh /
# Copy the create mailbox script in python-cyrus dir
COPY create_mailbox.py /srv/python-cyrus.git/source


RUN mkdir -p /var/lib/cyrus /var/spool/cyrus /var/spool/sieve /run/cyrus /run/cyrus/socket
RUN chown -R cyrus:mail /var/lib/cyrus /var/spool/cyrus /var/spool/sieve /run/cyrus
RUN chmod 750 /var/lib/cyrus /var/spool/cyrus /var/spool/sieve /run/cyrus
RUN dpkg-statoverride --add cyrus mail 755 /run/cyrus
RUN dpkg-statoverride --add cyrus mail 755 /run/cyrus/socket

# create a test user
RUN /etc/init.d/saslauthd start
RUN echo 'test' | saslpasswd2 -p -c test
RUN echo 'cyrus' | saslpasswd2 -p -c cyrus

EXPOSE 80
#WORKDIR /root
#ENV IMAGE jessie
#ADD https://raw.githubusercontent.com/cyrusimap/cyrus-docker/master/.bashrc /root/.bashrc
#ADD https://raw.githubusercontent.com/cyrusimap/cyrus-docker/master/.vimrc /root/.vimrc

# TODO: copy config files

# TODO: change this to a proper startup
WORKDIR /
#ADD https://raw.githubusercontent.com/cyrusimap/cyrus-docker/master/entrypoint.sh /
#ADD https://raw.githubusercontent.com/cyrusimap/cyrus-docker/master/functions.sh /
#RUN chmod 755 /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]