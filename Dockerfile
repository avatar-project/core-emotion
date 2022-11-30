FROM python:3.9 as build-image

ARG PLATFORM_PIP_EXTRA_INDEX_URL
ARG CORE_PIP_EXTRA_INDEX_URL

WORKDIR /service
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# COPY requirements requirements/
COPY ./requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check --requirement requirements.txt --extra-index-url ${PLATFORM_PIP_EXTRA_INDEX_URL}



FROM python:3.9 as runtime-image
RUN adduser service
USER service
COPY --chown=service:service --from=build-image /opt/venv /opt/venv
COPY --chown=service:service . /service
WORKDIR /service
ARG AVATAR_VERSION
ARG AVATAR_TITLE
ENV AVATAR_VERSION $AVATAR_VERSION
ENV AVATAR_TITLE $AVATAR_TITLE
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=

ENTRYPOINT ["python", "-m", "app"]
