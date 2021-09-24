FROM ghcr.io/projectcaluma/caluma:latest@sha256:63b09d2e2457b5d2aaadf712b8020ffd611e77c4895e005e2f7def54431542a9

ENV PATH="${HOME}/.local/bin:${PATH}"

COPY extensions /app/caluma/extensions
COPY ci/test.sh /app/caluma/ci/test.sh
COPY data /app/caluma/data
COPY requirements.txt /app/sagw-requirements.txt
RUN pip install --upgrade --no-cache-dir --requirement /app/sagw-requirements.txt  --disable-pip-version-check
