# snapshotalyzer-30000

Demo project to manage AWS EC2 instance snapshots

Also contains **sacraments/** — a parish sacramental records application
for the Orthodox Church in America (baptisms/chrismations, receptions,
marriages, funerals) with printable certificates and register pages.
See [sacraments/README.md](sacraments/README.md).

## About

This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring

shotty uses the configuration file created by the AWS cli. e.g.

'aws configure --profile shotty'

## Running

'pipenv shell'
'cd code\snapshotalyzer-30000\shotty'
'python shotty.py'
