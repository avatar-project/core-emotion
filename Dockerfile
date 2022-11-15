FROM python:3.9 as build-image
ARG PIP_EXTRA_INDEX_URL
WORKDIR /service
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# COPY requirements requirements/
COPY ./requirements.txt .
COPY ./require_install.sh .
RUN python -m pip install --upgrade pip
RUN sh require_install.sh
# RUN pip install --no-cache-dir --disable-pip-version-check --requirement requirements.txt


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
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "-m", "app"]
