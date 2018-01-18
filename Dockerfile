FROM python
COPY *.py /src
CMD [“python”, “/src/parse_statements.py”]
