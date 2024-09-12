FROM python:3.11

WORKDIR /code

COPY src/samdul05food/main.py /code/

# 모델 서빙만 하겠다. 의존성은 위 base 이미지에서 모두 설치 했다)
RUN pip install --no-cache-dir --upgrade  git+https://github.com/GITSangWoo/samdul05food@main

#모델 서빙을 위해 API 구동을 위한 FastAPI RUN
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
