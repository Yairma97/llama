FROM text2sql-env:1.0
WORKDIR /app
COPY . .
ENV UV_SYSTEM_PYTHON=1
ENV VIRTUAL_ENV=/opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"
EXPOSE 5892
EXPOSE 5891
#CMD ["chainlit", "run", "chainlit_odr/odr.py", "--port", "5892","--host","0.0.0.0","--headless", "--debug"]
CMD ["uv","run","dify/api.py" ]