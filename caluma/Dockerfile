FROM ghcr.io/projectcaluma/caluma:7.15.2

ENV PATH="${HOME}/.local/bin:${PATH}"

COPY extensions /app/caluma/extensions
COPY ci/test.sh /app/caluma/ci/test.sh
COPY data /app/caluma/data
COPY requirements.txt /app/sagw-requirements.txt
RUN pip install --upgrade --no-cache-dir --requirement /app/sagw-requirements.txt  --disable-pip-version-check
