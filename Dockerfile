FROM text2sql-env:1.0
WORKDIR /app
COPY . .
EXPOSE 5892
#CMD ["chainlit", "run", "/app/chainlit_odr/odr.py", "--port", "5892","--host","0.0.0.0","--headless", "--debug"]

CMD ["chainlit", "run", "/app/chainlit_odr/odr.py", "--port", "5892","--host","0.0.0.0","--headless", "--debug"]