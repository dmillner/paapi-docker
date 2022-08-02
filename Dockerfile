


FROM python:3.9 

# Download the static build of Litestream directly into the path & make it executable.
# This is done in the builder and copied as the chmod doubles the size.
ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.8/litestream-v0.3.8-linux-amd64-static.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN mkdir /code
COPY ./litestream.yml /etc/litestream.yml

COPY ./ /code
RUN chmod -R 777 /code
WORKDIR /code



ENTRYPOINT ["/bin/sh", "-c" , "exec litestream replicate -exec 'uvicorn main:app --host 0.0.0.0 --port 80' " ]