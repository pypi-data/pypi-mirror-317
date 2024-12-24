import os

import gdsfactory as gf
import yaml
from fastapi import Body
from fastapi.responses import PlainTextResponse, Response
from natsort import natsorted

from ..core.cli.tree import get_args
from ..core.generate_svg import generate_svg
from ..core.shared import activate_pdk_by_name
from ..settings import SETTINGS as s
from .app import PDK, PROJECT_DIR, app
from .yaml import _get_allowed_instance_settings


@app.get("/load")
def load(path: str):
    if not path.endswith(".pic.yml"):
        return PlainTextResponse(f"{path!r} is not a .pic.yml file.", status_code=422)
    schematic_path = f"{path[:-8]}.scm.yml"
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    if os.path.exists(path):
        netlist = yaml.safe_load(open(path))
    else:
        netlist = {}
    if not isinstance(netlist, dict):
        netlist = {}
    if os.path.exists(schematic_path):
        schematic = yaml.safe_load(open(schematic_path))
    else:
        schematic = {}
    if not isinstance(schematic, dict):
        schematic = {}
    ret = {
        "netlist": netlist,
        "schematic": schematic,
    }
    return ret


@app.post("/save")
def save_post(body: str = Body(...), *, path: str):
    if not path.endswith(".pic.yml"):
        return PlainTextResponse(f"{path!r} is not a .pic.yml file.", status_code=422)
    try:
        netlist_and_schematic = yaml.safe_load(body)
    except Exception:
        netlist_and_schematic = {}
    if not isinstance(netlist_and_schematic, dict):
        netlist_and_schematic = {}
    netlist = netlist_and_schematic.get("netlist", {})
    schematic = netlist_and_schematic.get("schematic", {})
    schematic_path = f"{path[:-8]}.scm.yml"
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    repo_dir = PROJECT_DIR
    schema_dir = os.path.join(repo_dir, "build", "schemas")
    pics_dir = os.path.join(repo_dir, s.name)
    schema_path = os.path.relpath(
        os.path.join(schema_dir, os.path.relpath(f"{path[:-8]}.json", pics_dir)),
        pics_dir,
    )
    with open(schematic_path, "w") as file:
        yaml.safe_dump(schematic, file, sort_keys=False)
    yaml_str = yaml.safe_dump(netlist, sort_keys=False)
    yaml_str = f"# yaml-language-server: $schema={schema_path}\n{yaml_str}".strip()
    with open(path, "r") as file:
        present_yaml_str = file.read().strip()
    if yaml_str != present_yaml_str:
        with open(path, "w") as file:
            file.write(yaml_str)
    return PlainTextResponse(f"netlist saved to {path}.")


@app.get("/save")
def save_get(body: str, path: str):
    return save_post(body=body, path=path)


@app.get("/settings")
def settings(components: str):
    pdk = activate_pdk_by_name(PDK)
    component_names = natsorted(set(components.split(",")))
    refs = {}
    component_settings = {}
    for component in component_names:
        component_settings[component] = {}
        try:
            types = _get_allowed_instance_settings(pdk.cells[component])
            defaults = get_args(pdk.cells[component])
        except KeyError:
            types, defaults = {}, {}
        for key, tp in types.items():
            component_settings[component][key] = {
                "default": None,
                "type": tp,
            }
            if key in defaults:
                component_settings[component][key]["default"] = defaults[key]
                if defaults[key] in pdk.cells:
                    if not "@component" in refs:
                        refs["@component"] = list(pdk.cells)
                    component_settings[component][key]["type"] = "@component"
                if defaults[key] in pdk.cross_sections:
                    if not "@cross_section" in refs:
                        refs["@cross_section"] = [
                            xs for xs in pdk.cross_sections if xs != "cross_section"
                        ]
                    component_settings[component][key]["type"] = "@cross_section"
    ret = {
        "components": component_settings,
        "refs": refs,
    }
    return ret


@app.get("/routing-strategies")
def routing_strategies():
    pdk = activate_pdk_by_name(PDK)
    refs = {}
    ret = {}
    for k, v in (pdk.routing_strategies or {}).items():
        if "bundle" in k:
            args = _get_types_and_defaults_for_routing(v)
            refs.update(args.pop("@refs"))
            ret[k] = args
    return {"strategies": ret, "refs": refs}


@app.get("/svg/{component}.svg")
def svg(component: str, width: int = 80, height: int = 80):
    pdk = activate_pdk_by_name(PDK)
    try:
        comp = pdk.get_component(component)
    except Exception:
        comp = gf.Component()
    assert isinstance(comp, gf.Component)
    svg = generate_svg(comp, width, height)
    return Response(svg, media_type="image/svg+xml")


def _get_types_and_defaults_for_routing(func):
    pdk = gf.get_active_pdk()
    defaults = get_args(func)
    types = _get_allowed_instance_settings(func)
    refs = {}
    ret = {}
    for k in natsorted(set(types) | set(defaults)):
        default = defaults.get(k, None)
        tpe = types.get(k, None)

        if k == "waypoints":
            tpe = "Waypoints"
        elif k == "port_type":
            tpe = "@port_type"
            refs["@port_type"] = ["optical", "electrical"]
            default = "optical"
        if k in ["component", "port1", "port2", "ports1", "ports2"]:
            continue

        if default is None:
            if tpe == "str":
                default = ""
            elif tpe == "bool":
                default = False
        if tpe is None:
            tpe = "str"
        elif tpe == "float | list[float]":
            tpe = "float"
        elif tpe == "Iterable":
            tpe = "list"
        elif isinstance(tpe, list) and len(tpe) > 0:
            if tpe[0] in pdk.cells:
                refs["@component"] = tpe
                tpe = "@component"
            elif tpe[0] in pdk.cross_sections:
                refs["@cross_section"] = tpe
                tpe = "@cross_section"
        elif tpe == "NoneType":
            tpe = "str"

        if isinstance(tpe, str):
            tpe = tpe.replace(" ", "").replace("|None", "").replace("None|", "").strip()
            if default is None:
                tpe = f"{tpe}?"

        ret[k] = {
            "default": default,
            "type": tpe,
        }
    if "component" in ret:
        ret = {"component": ret.pop("component"), **ret}
    return {**ret, "@refs": refs}
