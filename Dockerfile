FROM text2sql-env:1.0
WORKDIR /app
COPY . .
ENV UV_SYSTEM_PYTHON=1
EXPOSE 5892
EXPOSE 5891
RUN /bin/bash -c "source .venv/bin/activate"
RUN uv sync --extra cpu
CMD ["uv","run","--extra","cpu","chainlit", "run", "chainlit_odr/odr.py", "--port", "5892","--host","0.0.0.0","--headless", "--debug"]
#CMD ["uv","run","--extra","cpu","dify/api.py" ]