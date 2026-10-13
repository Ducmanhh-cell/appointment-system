FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN groupadd --system appuser && useradd --system --gid appuser --home-dir /home/appuser appuser
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY --chown=appuser:appuser . /app
RUN mkdir -p /vol/web/static /var/log/appointment \
    && chown -R appuser:appuser /app /vol/web /var/log/appointment
COPY --chmod=755 entrypoint.sh /entrypoint.sh
USER appuser
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
