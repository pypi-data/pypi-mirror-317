FROM leplusorg/latex:main
WORKDIR /tmp
USER root
RUN apt-get update && apt-get install -y python3 python3-pip python3-pytest
RUN pip3 download hw2_fedaniil==0.1.0 --no-binary :all:
RUN tar -xzf hw2_fedaniil-0.1.0.tar.gz
RUN pip3 install hw2_fedaniil --break-system-packages
CMD ["pytest", "-v", "hw2_fedaniil-0.1.0/tests"]

