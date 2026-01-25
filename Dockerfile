FROM python:3.9

WORKDIR /main

COPY . /main

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit","run","main.py"]