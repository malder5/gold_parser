FROM python

WORKDIR /app

COPY main.py .
COPY requirements.txt .
COPY sqlite.py .
RUN pip install -r requirements.txt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
CMD python3 main.py