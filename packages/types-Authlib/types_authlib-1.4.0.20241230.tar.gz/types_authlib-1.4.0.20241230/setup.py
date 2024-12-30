from setuptools import setup

name = "types-Authlib"
description = "Typing stubs for Authlib"
long_description = '''
## Typing stubs for Authlib

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Authlib`](https://github.com/lepture/authlib) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `Authlib`. This version of
`types-Authlib` aims to provide accurate annotations for
`Authlib==1.4.*`.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/Authlib`](https://github.com/python/typeshed/tree/main/stubs/Authlib)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`d634fc2f52b1f35e3bc664c7635859debbfe5e5d`](https://github.com/python/typeshed/commit/d634fc2f52b1f35e3bc664c7635859debbfe5e5d).
'''.lstrip()

setup(name=name,
      version="1.4.0.20241230",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Authlib.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['cryptography'],
      packages=['authlib-stubs'],
      package_data={'authlib-stubs': ['__init__.pyi', 'common/__init__.pyi', 'common/encoding.pyi', 'common/errors.pyi', 'common/security.pyi', 'common/urls.pyi', 'consts.pyi', 'deprecate.pyi', 'integrations/__init__.pyi', 'integrations/base_client/__init__.pyi', 'integrations/base_client/async_app.pyi', 'integrations/base_client/async_openid.pyi', 'integrations/base_client/errors.pyi', 'integrations/base_client/framework_integration.pyi', 'integrations/base_client/registry.pyi', 'integrations/base_client/sync_app.pyi', 'integrations/base_client/sync_openid.pyi', 'jose/__init__.pyi', 'jose/drafts/__init__.pyi', 'jose/drafts/_jwe_algorithms.pyi', 'jose/drafts/_jwe_enc_cryptodome.pyi', 'jose/drafts/_jwe_enc_cryptography.pyi', 'jose/errors.pyi', 'jose/jwk.pyi', 'jose/rfc7515/__init__.pyi', 'jose/rfc7515/jws.pyi', 'jose/rfc7515/models.pyi', 'jose/rfc7516/__init__.pyi', 'jose/rfc7516/jwe.pyi', 'jose/rfc7516/models.pyi', 'jose/rfc7517/__init__.pyi', 'jose/rfc7517/_cryptography_key.pyi', 'jose/rfc7517/asymmetric_key.pyi', 'jose/rfc7517/base_key.pyi', 'jose/rfc7517/jwk.pyi', 'jose/rfc7517/key_set.pyi', 'jose/rfc7518/__init__.pyi', 'jose/rfc7518/ec_key.pyi', 'jose/rfc7518/jwe_algs.pyi', 'jose/rfc7518/jwe_encs.pyi', 'jose/rfc7518/jwe_zips.pyi', 'jose/rfc7518/jws_algs.pyi', 'jose/rfc7518/oct_key.pyi', 'jose/rfc7518/rsa_key.pyi', 'jose/rfc7518/util.pyi', 'jose/rfc7519/__init__.pyi', 'jose/rfc7519/claims.pyi', 'jose/rfc7519/jwt.pyi', 'jose/rfc8037/__init__.pyi', 'jose/rfc8037/jws_eddsa.pyi', 'jose/rfc8037/okp_key.pyi', 'jose/util.pyi', 'oauth1/__init__.pyi', 'oauth1/client.pyi', 'oauth1/errors.pyi', 'oauth1/rfc5849/__init__.pyi', 'oauth1/rfc5849/authorization_server.pyi', 'oauth1/rfc5849/base_server.pyi', 'oauth1/rfc5849/client_auth.pyi', 'oauth1/rfc5849/errors.pyi', 'oauth1/rfc5849/models.pyi', 'oauth1/rfc5849/parameters.pyi', 'oauth1/rfc5849/resource_protector.pyi', 'oauth1/rfc5849/rsa.pyi', 'oauth1/rfc5849/signature.pyi', 'oauth1/rfc5849/util.pyi', 'oauth1/rfc5849/wrapper.pyi', 'oauth2/__init__.pyi', 'oauth2/auth.pyi', 'oauth2/base.pyi', 'oauth2/client.pyi', 'oauth2/rfc6749/__init__.pyi', 'oauth2/rfc6749/authenticate_client.pyi', 'oauth2/rfc6749/authorization_server.pyi', 'oauth2/rfc6749/errors.pyi', 'oauth2/rfc6749/grants/__init__.pyi', 'oauth2/rfc6749/grants/authorization_code.pyi', 'oauth2/rfc6749/grants/base.pyi', 'oauth2/rfc6749/grants/client_credentials.pyi', 'oauth2/rfc6749/grants/implicit.pyi', 'oauth2/rfc6749/grants/refresh_token.pyi', 'oauth2/rfc6749/grants/resource_owner_password_credentials.pyi', 'oauth2/rfc6749/models.pyi', 'oauth2/rfc6749/parameters.pyi', 'oauth2/rfc6749/requests.pyi', 'oauth2/rfc6749/resource_protector.pyi', 'oauth2/rfc6749/token_endpoint.pyi', 'oauth2/rfc6749/util.pyi', 'oauth2/rfc6749/wrappers.pyi', 'oauth2/rfc6750/__init__.pyi', 'oauth2/rfc6750/errors.pyi', 'oauth2/rfc6750/parameters.pyi', 'oauth2/rfc6750/token.pyi', 'oauth2/rfc6750/validator.pyi', 'oauth2/rfc7009/__init__.pyi', 'oauth2/rfc7009/parameters.pyi', 'oauth2/rfc7009/revocation.pyi', 'oauth2/rfc7521/__init__.pyi', 'oauth2/rfc7521/client.pyi', 'oauth2/rfc7523/__init__.pyi', 'oauth2/rfc7523/assertion.pyi', 'oauth2/rfc7523/auth.pyi', 'oauth2/rfc7523/client.pyi', 'oauth2/rfc7523/jwt_bearer.pyi', 'oauth2/rfc7523/token.pyi', 'oauth2/rfc7523/validator.pyi', 'oauth2/rfc7591/__init__.pyi', 'oauth2/rfc7591/claims.pyi', 'oauth2/rfc7591/endpoint.pyi', 'oauth2/rfc7591/errors.pyi', 'oauth2/rfc7592/__init__.pyi', 'oauth2/rfc7592/endpoint.pyi', 'oauth2/rfc7636/__init__.pyi', 'oauth2/rfc7636/challenge.pyi', 'oauth2/rfc7662/__init__.pyi', 'oauth2/rfc7662/introspection.pyi', 'oauth2/rfc7662/models.pyi', 'oauth2/rfc7662/token_validator.pyi', 'oauth2/rfc8414/__init__.pyi', 'oauth2/rfc8414/models.pyi', 'oauth2/rfc8414/well_known.pyi', 'oauth2/rfc8628/__init__.pyi', 'oauth2/rfc8628/device_code.pyi', 'oauth2/rfc8628/endpoint.pyi', 'oauth2/rfc8628/errors.pyi', 'oauth2/rfc8628/models.pyi', 'oauth2/rfc8693/__init__.pyi', 'oauth2/rfc9068/__init__.pyi', 'oauth2/rfc9068/claims.pyi', 'oauth2/rfc9068/introspection.pyi', 'oauth2/rfc9068/revocation.pyi', 'oauth2/rfc9068/token.pyi', 'oauth2/rfc9068/token_validator.pyi', 'oidc/__init__.pyi', 'oidc/core/__init__.pyi', 'oidc/core/claims.pyi', 'oidc/core/errors.pyi', 'oidc/core/grants/__init__.pyi', 'oidc/core/grants/code.pyi', 'oidc/core/grants/hybrid.pyi', 'oidc/core/grants/implicit.pyi', 'oidc/core/grants/util.pyi', 'oidc/core/models.pyi', 'oidc/core/util.pyi', 'oidc/discovery/__init__.pyi', 'oidc/discovery/models.pyi', 'oidc/discovery/well_known.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
