FROM ghcr.io/projectcaluma/caluma:12.3.4

ENV PATH="${HOME}/.local/bin:${PATH}"
ENV PYTHONPATH="/app"

USER root
COPY requirements.txt /app/sagw-requirements.txt
RUN pip install --no-cache-dir -r /app/sagw-requirements.txt

USER caluma
COPY extensions /app/caluma_extensions
COPY ci/test.sh /app/caluma/ci/test.sh
COPY data /app/caluma/data
