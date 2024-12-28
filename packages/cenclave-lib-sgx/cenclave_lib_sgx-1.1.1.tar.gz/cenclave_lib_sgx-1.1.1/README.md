# Cosmian Enclave Lib SGX

## Overview

Cosmian Enclave lib SGX bootstraps the execution of an encrypted ASGI/WSGI Python web application for [Gramine](https://gramine.readthedocs.io/).

The library is responsible for:

- Configuring the SSL certificates with either:
  - *RA-TLS*, a self-signed certificate including the Intel SGX quote in an X.509 v3 extension
  - *Custom*, the private key and full keychain is provided by the application owner
  - *No SSL*, the secure channel may be managed elsewhere by an SSL proxy
- Decrypting Python modules encrypted with XSala20-Poly1305 AE
- Running the ASGI/WSGI Python web application with [hypercorn](https://pgjones.gitlab.io/hypercorn/)

## Technical details

The flow to run an encrypted Python web application is the following:

1. A first self-signed HTTPS server using RA-TLS is launched waiting to receive a JSON payload with:
   - UUID, a unique application identifier provided to `cenclave-bootstrap` as an argument
   - the decryption key of the code
   - Optionally the private key corresponding to the certificate provided to `cenclave-bootstrap` (for *Custom* certificate)
2. If the UUID and decryption key are the expected one, the configuration server is stopped, the code is decrypted and finally run as a new server


## Installation 

```console
$ pip install cenclave-lib-sgx
```

## Usage

```console
$ cenclave-bootstrap --help
usage: cenclave-bootstrap [-h] [--host HOST] [--client-certificate CLIENT_CERTIFICATE] [--port PORT]
                          [--subject SUBJECT] [--san SAN] --app-dir APP_DIR --id ID [--timeout TIMEOUT]
                          [--version] [--debug]
                          (--ratls EXPIRATION_DATE | --no-ssl | --certificate CERTIFICATE_PATH)
                          application

Bootstrap ASGI/WSGI Python web application for Gramine

positional arguments:
  application           ASGI application path (as module:app)

options:
  -h, --help            show this help message and exit
  --host HOST           hostname of the server
  --client-certificate CLIENT_CERTIFICATE
                        For client certificate authentication (PEM encoded)
  --port PORT           port of the server
  --subject SUBJECT     Subject as RFC 4514 string for the RA-TLS certificate
  --san SAN             Subject Alternative Name in the RA-TLS certificate
  --app-dir APP_DIR     path of the python web application
  --id ID               identifier of the application as UUID in RFC 4122
  --timeout TIMEOUT     seconds before closing the configuration server
  --version             show program's version number and exit
  --debug               debug mode with more logging
  --ratls EXPIRATION_DATE
                        generate a self-signed certificate for RA-TLS with a specific expiration date (Unix time)
  --no-ssl              use HTTP without SSL
  --certificate CERTIFICATE_PATH
                        custom certificate used for the SSL connection, private key must be sent through the
                        configuration server
```
