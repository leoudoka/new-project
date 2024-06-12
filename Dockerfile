FROM python:3.10-slim

ENV FLASK_APP main.py
ENV FLASK_ENV production

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY api api
COPY migrations migrations
COPY alembic.ini alembic.ini
COPY main.py config.py boot.sh ./

EXPOSE 4000
CMD ./boot.sh