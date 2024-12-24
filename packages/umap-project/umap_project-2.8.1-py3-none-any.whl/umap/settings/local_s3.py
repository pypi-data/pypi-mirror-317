from umap.settings.local import *

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "umaps3",
    }
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": "OScTD3CClCcO54Ax2DLz",
            "secret_key": "eK9tfPRHoFh0nKLkZpJJoC4RJS1ptGfko3iBBd5k",
            "bucket_name": "umap-default",
            "region_name": "eu",
            "endpoint_url": "http://127.0.0.1:9000",
        },
    },
    "data": {
        "BACKEND": "umap.storage.s3.S3DataStorage",
        "OPTIONS": {
            "access_key": "OScTD3CClCcO54Ax2DLz",
            "secret_key": "eK9tfPRHoFh0nKLkZpJJoC4RJS1ptGfko3iBBd5k",
            "bucket_name": "umap",
            "region_name": "eu",
            "endpoint_url": "http://127.0.0.1:9000",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": "OScTD3CClCcO54Ax2DLz",
            "secret_key": "eK9tfPRHoFh0nKLkZpJJoC4RJS1ptGfko3iBBd5k",
            "bucket_name": "umap-staticfiles",
            "region_name": "eu",
            "endpoint_url": "http://127.0.0.1:9000",
            "default_acl": "public-read",
            # "querystring_auth": False,
        },
    },
}

# STATIC_URL = "http://127.0.0.1:9000/umap-staticfiles/"
