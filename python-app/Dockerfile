FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN echo '#!/bin/bash\n\
env | grep -E "^(AWS_|DYNAMODB_)" > .env\n\
exec python app.py' > /entrypoint.sh && chmod +x /entrypoint.sh
EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]