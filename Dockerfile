FROM python
COPY *.py /src/
ENTRYPOINT ["sh", "-c", "python /src/parse_statements.py --path /statements"]

