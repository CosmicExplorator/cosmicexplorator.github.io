FROM python:3.13-alpine3.22

ARG BUILD_ARCH
ARG BUILD_VERSION

LABEL \
  io.hass.name="Huawei HiLink SMS" \
  io.hass.description="SMS inbox for Huawei HiLink modems" \
  io.hass.type="app" \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.arch="${BUILD_ARCH}"

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
COPY static ./static
COPY templates ./templates
COPY run.sh /run.sh
RUN chmod 755 /run.sh

EXPOSE 8099
CMD ["/run.sh"]

