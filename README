# Steps to philosophy

Inspiration: https://xkcd.com/903/

Write up with more details: https://ryanelmquist.com/steps-to-philosophy

## Running locally

Use dev_appserver.py which is installed wherever google-cloud-sdk was
installed. This was
`/usr/local/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/bin/dev_appserver.py`
for me.

```sh
dev_appserver.py app.yaml
```

## Deploying

Install `gcloud`

```sh
# Don't do this step from tmux otherwise you'll confuse things
$ gcloud auth login

# From https://console.cloud.google.com/home/dashboard
$ gcloud config set project [PROJECT ID]

$ gcloud app deploy
```
