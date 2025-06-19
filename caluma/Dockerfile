FROM ghcr.io/projectcaluma/caluma:11.3.0

ENV PATH="${HOME}/.local/bin:${PATH}"

COPY extensions /app/caluma/extensions
COPY ci/test.sh /app/caluma/ci/test.sh
COPY data /app/caluma/data
COPY requirements.txt /app/sagw-requirements.txt

USER root
RUN apt-get -y update && apt-get -y upgrade

USER caluma
ARG INSTALL_DEV="false"
RUN if [ "$INSTALL_DEV" = "true" ] ; then poetry install --no-root; fi \
  && poetry run pip install -r /app/sagw-requirements.txt
