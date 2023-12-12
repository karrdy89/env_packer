FROM condaforge/miniforge3:23.3.1-1
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install nano
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install python3.11 -y
RUN apt-get install python3-pip -y
RUN apt-get install python-is-python3 -y
RUN conda create -n python3.11 python=3.11 -y
WORKDIR /app/
RUN mkdir cert
RUN mkdir logs
RUN mkdir config
RUN mkdir tmp
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3", "start_server.py"]