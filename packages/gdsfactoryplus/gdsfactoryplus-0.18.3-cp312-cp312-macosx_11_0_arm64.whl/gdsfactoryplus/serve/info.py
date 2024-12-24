import json
from typing import Literal

from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from natsort import natsorted

from ..core.cli.tree import _tree
from ..core.cli.tree_item import _tree_item
from ..core.shared import (
    activate_pdk_by_name,
    get_custom_cell_names,
    get_pdk_cell_names,
)
from ..settings import SETTINGS as s
from .app import PDK, PROJECT_DIR, app


@app.get("/pdk")
def pdk():
    return PlainTextResponse(PDK)


@app.get("/dir")
def project_dir():
    return PlainTextResponse(PROJECT_DIR)


@app.get("/pdk/list")
def list_custom():
    pdk = activate_pdk_by_name(PDK)
    resp = {
        "custom": get_custom_cell_names(pdk),
        "pdk": get_pdk_cell_names(pdk),
        "all": natsorted(pdk.cells),
    }
    return resp


@app.get("/tree")
def tree(
    path: str = s.name,
    by: Literal["cell", "file", "flat"] = "cell",
    key: str = "",
    format: str = "yaml",
):
    activate_pdk_by_name(PDK)
    tree = _tree(path, by, key, format)
    if str(format).strip().lower() == "json":
        return JSONResponse(json.loads(tree))
    else:
        return PlainTextResponse(tree)


@app.get("/tree-item")
def tree_item(
    name: str,
    path: str = s.name,
    key: str = "",
    format: str = "yaml",
):
    activate_pdk_by_name(PDK)
    try:
        tree = _tree_item(name, path, key, format)
    except KeyError:
        tree = "{}"
    if str(format).strip().lower() == "json":
        return JSONResponse(json.loads(tree))
    else:
        return PlainTextResponse(tree)


@app.get("/")
def redirect():
    return RedirectResponse("/code/")


@app.get("/code")
def code():
    return "gfp server is running."
