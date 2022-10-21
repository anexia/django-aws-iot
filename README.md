# Django AWS IoT

A django module that allows to connect and publish messages to AWS IoT

# Installation

Install using pip:

```shell
pip install git+https://github.com/anexia/django-aws-iot@main
```

Extend django settings:

```python
AWS_IOT_ENABLED = True
AWS_IOT_SERVER = "server.amazonaws.com"
AWS_IOT_CLIENT_ID = "Thing-Name"
AWS_IOT_CERT_PATH = "/certificates/8a6a6cfdf1-certificate.pem.crt"
AWS_IOT_KEY_PATH = "/certificates/8a6a6cfdf1-private.pem.key"
AWS_IOT_ROOT_CERT_PATH = "/certificates/AmazonRootCA1.pem"
```

# Usage

Currently the library only supports publishing messages to AWS IoT:


```python
from django_aws_iot.aws_iot import mqtt_publish


mqtt_publish(
    'topic/123',
    {
        'foo': 'bar'
    }
)
```
