FROM python:3

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /tmp

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY ../* ./terraform/

CMD ["python","main.py"]

# docker build ./ -t tf_review
# docker run tf_review
