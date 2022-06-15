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

