FROM ghcr.io/projectcaluma/caluma:10.1.1

ENV PATH="${HOME}/.local/bin:${PATH}"

COPY extensions /app/caluma/extensions
COPY ci/test.sh /app/caluma/ci/test.sh
COPY data /app/caluma/data
COPY requirements.txt /app/sagw-requirements.txt

# TODO: install dependencies as caluma user. Needs:
# https://github.com/projectcaluma/caluma/pull/2219/commits/962310774681c32845fb8c17b4eeadbdc686ae0d
# in a release
USER root
ARG INSTALL_DEV="false"

RUN if [ "$INSTALL_DEV" = "true" ] ; then poetry install --no-root; fi \
&& poetry run pip install -r /app/sagw-requirements.txt

USER caluma
