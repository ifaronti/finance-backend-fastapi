FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ${LAMBDA_TASK_ROOT}/app
COPY venv ${LAMBDA_TASK_ROOT}/venv
COPY main.py ${LAMBDA_TASK_ROOT}
COPY placeholders.json ${LAMBDA_TASK_ROOT}
COPY .env ${LAMBDA_TASK_ROOT}
# RUN uvicorn main:app

CMD ["main.handler"]