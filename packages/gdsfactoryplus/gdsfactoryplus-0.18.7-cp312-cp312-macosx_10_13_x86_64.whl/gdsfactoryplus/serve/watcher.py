import json
import os
import sys
import traceback

import gdsfactory as gf
import yaml
from loguru import logger
from pydantic import BaseModel, Field

from ..core.netlist import try_get_ports
from ..core.schema import get_netlist_schema
from ..core.shared import (
    activate_pdk_by_name,
    clear_cells_from_cache,
    get_python_cells,
    get_yaml_cell_name,
)
from ..settings import SETTINGS as s
from .app import PDK, PROJECT_DIR, app

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="{time:HH:mm:ss} | <level>{level: <8}</level> | <level>{message}</level>",
)


@app.get("/watch/on-created")
def on_created(path: str):
    result = save_gds(path)
    logger.info(f"created {path}.")
    return result.model_dump()


@app.get("/watch/on-modified")
def on_modified(path: str):
    result = save_gds(path)
    logger.info(f"modified {path}.")
    return result.model_dump()


@app.get("/watch/on-deleted")
def on_deleted(path: str):
    result = Result(errors=["No on-deleted callback implemented."])
    logger.info(f"did not delete {path}. (not implemented)")
    return result.model_dump()


class Result(BaseModel):
    log: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


def save_gds(path) -> Result:
    logger.info(f"saving {path}...")
    result = Result()
    pdk = activate_pdk_by_name(PDK)
    pdk = gf.get_active_pdk()
    path = os.path.abspath(path)
    dir = os.path.dirname(path)
    dir_repo = os.path.abspath(PROJECT_DIR)
    dir_pics = os.path.join(dir_repo, s.name)

    if not os.path.commonpath([path, dir_pics]) == dir_pics:
        result.errors.append(f"path {path!r} is not a subpath of {dir_pics!r}.")
        return result

    dir_gds = os.path.abspath(
        os.path.join(dir_repo, "build", "gds", os.path.relpath(dir, dir_pics))
    )
    os.makedirs(dir_gds, exist_ok=True)
    logger.info(f"{dir_gds=}")

    dir_ports = os.path.join(dir_gds, "ports")
    os.makedirs(dir_ports, exist_ok=True)
    logger.info(f"{dir_ports=}")

    dir_log = os.path.abspath(
        os.path.join(dir_repo, "build", "log", os.path.relpath(dir, dir_pics))
    )
    os.makedirs(dir_log, exist_ok=True)
    logger.info(f"{dir_log=}")

    dir_schema = os.path.abspath(
        os.path.join(dir_repo, "build", "schemas", os.path.relpath(dir, dir_pics))
    )
    os.makedirs(dir_schema, exist_ok=True)
    logger.info(f"{dir_schema=}")

    if path.endswith(".pic.yml"):
        generate_schema = True
        names = [get_yaml_cell_name(path)]
    elif path.endswith(".py"):
        generate_schema = False
        names = list(get_python_cells(dir_pics, [path]))
    else:
        result.errors.append(f"path {path!r} is not a .pic.yml of a .py file.")
        return result
    logger.info(f"{names=}")
    result.log.append(f"cells: {names}.")

    clear_cells_from_cache(pdk, *names)

    for name in names:
        if name not in pdk.cells:
            result.errors.append(f"{name} not found in PDK!")

    if result.errors:
        return result
    logger.info(f"{result=}")

    busy_paths = []
    for cell_name in names:
        path_log_busy = os.path.join(dir_log, f"{cell_name}.busy.log")
        with open(path_log_busy, "w") as file:
            file.write("")
        busy_paths.append(path_log_busy)

    for cell_name in names:
        logger.info(f"{cell_name=}")
        path_gds = os.path.join(dir_gds, f"{cell_name}.gds")
        path_ports = os.path.join(dir_ports, f"{cell_name}.json")
        path_log = os.path.join(dir_log, f"{cell_name}.log")
        path_log_busy = os.path.join(dir_log, f"{cell_name}.busy.log")
        path_schema = os.path.join(dir_schema, f"{cell_name}.json")

        exc = None
        comp = None
        file = open(path_log_busy, "w")
        old_stdout, sys.stdout = sys.stdout, file
        old_stderr, sys.stderr = sys.stderr, file
        try:
            func = pdk.cells[cell_name]
            comp = func()
            logger.success(f"SUCCESS: Succesfully built '{cell_name}.gds'.")
            file.write(f"SUCCESS: Succesfully built '{cell_name}.gds'.")
        except Exception as e:
            exc = e
            logger.error(f"ERROR building {cell_name}.")
            file.write(f"ERROR building {cell_name}.\n")
            traceback.print_exc(file=file)
        finally:
            file.close()
            os.rename(path_log_busy, path_log)
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        if exc is not None:
            logger.error(
                f"Could not build {cell_name!r} [{exc.__class__.__name__}]. Please check logs."
            )
            result.errors.append(
                f"Could not build {cell_name!r} [{exc.__class__.__name__}]. Please check logs."
            )
            continue

        if comp is None:  # this should actually never happen
            logger.error(
                f"Could not build {cell_name!r} [Unknown Exception]. Please check logs."
            )
            result.errors.append(
                f"Could not build {cell_name!r} [Unknown Exception]. Please check logs."
            )
            continue

        result.log.append(f"SUCCESS. -> {path_gds}")

        if generate_schema:
            try:
                netlist = yaml.safe_load(open(path))
                schema = get_netlist_schema(netlist)
                with open(path_schema, "w") as file:
                    file.write(json.dumps(schema, indent=2))
                logger.success(f"{cell_name}: schema generation succeeded.")
                result.log.append(f"{cell_name}: schema generation succeeded.")
            except Exception as e:
                logger.error(f"{cell_name}: schema generation failed.")
                result.errors.append(f"{cell_name}: schema generation failed.")

        with open(path_log, "a") as file:
            old_stdout, sys.stdout = sys.stdout, file
            old_stderr, sys.stderr = sys.stderr, file
            try:
                comp.write_gds(path_gds)
                ports = try_get_ports(comp)
                with open(path_ports, "w") as file:
                    json.dump(ports, file)
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

        logger.success(f"{cell_name}: saved.")

    for busy_path in busy_paths:
        if os.path.exists(busy_path):
            os.remove(busy_path)

    return result
