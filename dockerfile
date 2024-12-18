FROM public.ecr.aws/lambda/python:3.13

# WORKDIR /usr/src/app

COPY main.py ${LAMBDA_TASK_ROOT}
COPY app placeholders.json ./
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

COPY . ${LAMBDA_TASK_ROOT}

CMD ["main.handler"]