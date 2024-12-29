from typing import Any


def load_ipython_extension(ip: Any) -> None:  # pragma: no cover
    # prevent circular import
    from .pretty import install
    from .traceback import install as tr_install

    install()
    tr_install()
