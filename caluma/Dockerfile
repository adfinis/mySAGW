FROM ghcr.io/projectcaluma/caluma:8.0.0-beta.27

ENV PATH="${HOME}/.local/bin:${PATH}"

COPY extensions /app/caluma/extensions
COPY ci/test.sh /app/caluma/ci/test.sh
COPY data /app/caluma/data
COPY requirements.txt /app/sagw-requirements.txt

USER root
ARG INSTALL_DEV="false"

RUN if [ "$INSTALL_DEV" = "true" ] ; then poetry install --no-root; fi \
&& poetry run pip install -r /app/sagw-requirements.txt

USER caluma
