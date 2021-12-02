FROM ghcr.io/projectcaluma/caluma:dev@sha256:28cf5465cb0bafba38d0de5058afa38d27db8770682a1b00c7d51f5467d6ad95

ENV PATH="${HOME}/.local/bin:${PATH}"

COPY extensions /app/caluma/extensions
COPY ci/test.sh /app/caluma/ci/test.sh
COPY data /app/caluma/data
COPY requirements.txt /app/sagw-requirements.txt
RUN pip install --upgrade --no-cache-dir --requirement /app/sagw-requirements.txt  --disable-pip-version-check
