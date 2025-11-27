FROM python:3.13

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 5000

CMD ["uv", "run", "flask", "run", "--host=0.0.0.0"]

