FROM projectcaluma/caluma:version-7.10.0

ENV PATH="${HOME}/.local/bin:${PATH}"

COPY extensions /app/caluma/extensions
COPY ci/test.sh /app/caluma/ci/test.sh
COPY data /app/caluma/data
