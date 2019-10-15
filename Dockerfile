# Pole Star Dockerfile.

# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath.
FROM python:3.7.4-alpine

# Set an environment variable with the directory
# where we'll be running the app.
ENV APP /app

# Create the directory and instruct Docker to operate
# from there from now on.
RUN mkdir $APP
WORKDIR $APP

# Expose the port gunicorn will listen on.
EXPOSE 8000

# Copy the requirements file in order to install
# Python dependencies.
COPY conf/requirements.txt conf/

# Install sys deps, perform clean up.
RUN apk add --no-cache --virtual .build-deps \
  build-base postgresql-dev libffi-dev \
    && pip install -r conf/requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

# We copy the rest of the codebase into the image.
COPY . .

# Run docker start command.
CMD [ "/bin/sh", "./conf/start-cmd.sh" ]
