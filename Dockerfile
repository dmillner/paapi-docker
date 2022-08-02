# 
FROM python:3.9



# 
COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# 
RUN mkdir /code
COPY ./ /code
RUN chmod -R 777 /code
WORKDIR /code

## litestream stage
FROM litestream/litestream
COPY ./litestream.yml /etc/litestream.yml

ENTRYPOINT ["/bin/sh", "-c" , "uvicorn main:app --host 0.0.0.0 --port 80 && replicate"]