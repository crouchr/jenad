# https://linuxize.com/post/how-to-install-opencv-on-debian-10/
# based on Debian Buster
FROM python:3.8.5-buster
LABEL author="Richard Crouch"
LABEL description="Jenad Daemon"

# generate logs in unbuffered mode
ENV PYTHONUNBUFFERED=1

RUN apt -y update
#RUN apt -y upgrade
#RUN apt -y install joe nmap

# Install Python dependencies
RUN pip3 install pipenv
COPY Pipfile* ./
RUN pipenv install --system --deploy

# Copy application and files
RUN mkdir /app
COPY app/*.py /app/
WORKDIR /app

# Run Python unbuffered so the logs are flushed
CMD ["python3", "-u", "jenad.py"]
