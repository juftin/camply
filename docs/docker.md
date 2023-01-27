# Running in Docker

Here's an example of a detached container searching in the background (notice the `-d` flag, the
container will run detached).

```commandline
docker run -d \
  --name camply-detached-example \
  --env PUSHOVER_PUSH_TOKEN=${PUSHOVER_PUSH_TOKEN} \
  --env PUSHOVER_PUSH_USER=${PUSHOVER_PUSH_USER} \
  --env TZ="America/Denver" \
  juftin/camply \
  camply campsites \
      --rec-area 2991 \
      --start-date 2023-08-01 \
      --end-date 2023-09-01 \
      --continuous \
      --notifications pushover
```

The docker image accepts the following environment variables:

-   Pushover Notifications
    -   `PUSHOVER_PUSH_USER`
-   Email Notifications
    -   `EMAIL_TO_ADDRESS`
    -   `EMAIL_USERNAME`
    -   `EMAIL_PASSWORD`
    -   `EMAIL_FROM_ADDRESS` (defaults to "camply@juftin.com")
    -   `EMAIL_SUBJECT_LINE` (defaults to "camply Notification")
    -   `EMAIL_SMTP_SERVER` (defaults to "smtp.gmail.com")
    -   `EMAIL_SMTP_PORT` (defaults to 465)
-   Optional Environment Variables
    -   `LOG_LEVEL` (sets logging level, defaults to "INFO")
    -   `PUSHOVER_PUSH_TOKEN` (Personal Pushover App Token)
    -   `RIDB_API_KEY` (Personal API Key
        for [Recreation.gov API](https://ridb.recreation.gov/profile))
    -   `TZ` ([TZ Database Name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for
        logging, defaults to UTC)

Alternatively, if you have already run `camply configure` locally, you can share
your [`.camply`](examples/example.camply) file inside the docker container.

```commandline
docker run \
  --name camply-file-share-example \
  --env TZ="America/Denver" \
  --volume ${HOME}/.camply:/home/camply/.camply \
  juftin/camply \
  camply campsites \
      --provider yellowstone \
      --start-date 2023-07-22 \
      --end-date 2023-07-27 \
      --continuous \
      --notifications email
```

To manage multiple searches (with different notification preferences) I like to use YAML
configuration files:

```commandline
docker run -d \
  --name camply-email-example \
  --env TZ="America/Denver" \
  --env EMAIL_TO_ADDRESS=${EMAIL_TO_ADDRESS} \
  --env EMAIL_USERNAME=${EMAIL_USERNAME} \
  --env EMAIL_PASSWORD=${EMAIL_PASSWORD} \
  --volume example_search.yaml:/home/camply/example_search.yaml \
  juftin/camply:latest \
  camply campsites \
      --yaml-config /home/camply/example_search.yaml
```

A [docker-compose example](examples/docker-compose.yaml) of the above YAML Config is also
available.
