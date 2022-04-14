FROM ghcr.io/projectcaluma/caluma:8.0.0-beta.4

ENV PATH="${HOME}/.local/bin:${PATH}"

COPY extensions /app/caluma/extensions
COPY ci/test.sh /app/caluma/ci/test.sh
COPY data /app/caluma/data
COPY requirements.txt /app/sagw-requirements.txt

USER root
RUN cat /app/sagw-requirements.txt | xargs poetry add --lock && \
    poetry install --no-dev --no-root
USER caluma
