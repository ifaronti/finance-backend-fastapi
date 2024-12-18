FROM public.ecr.aws/lambda/python:3.13

# WORKDIR /usr/src/app

COPY main.py ./
COPY app placeholders.json ./
COPY requirements.txt ./
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

COPY . ./

CMD ["main.handler"]