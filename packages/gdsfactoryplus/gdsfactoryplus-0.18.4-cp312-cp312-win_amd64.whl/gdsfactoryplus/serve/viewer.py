import os
import pathlib
import tempfile
from typing import Literal

from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse

from ..core.shared import get_active_pdk, merge_rdb_strings
from .app import PDK, PROJECT_DIR, app

try:
    from doweb.api.viewer import FileView, file_view_static  # type: ignore
except ImportError:
    from kweb.api.viewer import FileView, file_view_static  # type: ignore


@app.get("/view2")
async def view2(
    request: Request,
    file: str,
    cell: str = "",
    rdb: str = "",
    theme: Literal["light", "dark"] = "dark",
    regen_lyp: bool = False,
):
    if rdb:
        rdbs = rdb.split(",")
        rdb = os.path.join("build", "lyrdb", os.path.basename(rdbs[0]))
        xmls = [open(xml).read() for xml in rdbs]
        xml = merge_rdb_strings(*xmls)
        open(rdb, "w").write(xml)

    assert PROJECT_DIR is not None
    layer_props = os.path.join(PROJECT_DIR, "build", "lyp", f"{PDK}.lyp")
    if regen_lyp or not os.path.exists(layer_props):
        _pdk = get_active_pdk()
        layer_views = _pdk.layer_views
        assert layer_views is not None
        layer_views.to_lyp(filepath=layer_props)

    try:
        fv = FileView(
            file=pathlib.Path(file),
            cell=cell or None,
            layer_props=layer_props,
            rdb=rdb or None,
        )
        resp = await file_view_static(request, fv)  # type: ignore
    except HTTPException:
        color = "#f5f5f5" if theme == "light" else "#121317"
        return HTMLResponse(f'<body style="background-color: {color}"></body>')
    body = resp.body.decode()  # type: ignore
    body = modify_body(resp.body.decode(), theme, file)  # type: ignore
    return HTMLResponse(body)


def modify_body(body, theme, file):
    if theme == "light":
        body = body.replace('data-bs-theme="dark"', 'data-bs-theme="light"')
    body = body.replace(
        "</head>",
        """<style>
     [data-bs-theme=light] {
       --bs-body-bg: #f5f5f5;
     }
     [data-bs-theme=dark] {
       --bs-body-bg: #121317;
     }
   </style>
   </head>""",
    )
    body = body.replace(
        "</body>",
        """<script>
            window.addEventListener("message", (event) => {
              const message = JSON.parse(event.data);

              let reload = message.reload;
              if (reload) {
                document.getElementById("reload").click();
                return
              }

              let category = message.category;
              let cell = message.cell;
              let itemIdxs = message.itemIdxs;

              document.getElementById("rdb-tab").click();
              console.log("IFRAME: ", message);
              document.getElementById("rdb-tab").click();
              //const event = new Event('change');
              let categoryOptionsEl = document.getElementById("rdbCategoryOptions");
              let cellOptionsEl = document.getElementById("rdbCellOptions");
              let rdbItemsEl = document.getElementById("rdbItems");
              let categoryOptions = Array.from(categoryOptionsEl.children)
                .map((c)=>[c.innerHTML, c.value])
                .reduce((acc, [key, value]) => {acc[key] = value; return acc;}, {});
              let cellOptions = Array.from(cellOptionsEl.children)
                .map((c)=>[c.innerHTML, c.value])
                .reduce((acc, [key, value]) => {acc[key] = value; return acc;}, {});
              console.log(categoryOptions)
              console.log(cellOptions)
              let cellIndex = cellOptions[cell];
              let categoryIndex = categoryOptions[category];
              console.log(`cellIndex: ${cellIndex}`);
              console.log(`categoryIndex: ${categoryIndex}`);
              categoryOptionsEl.value = categoryIndex;
              cellOptionsEl.value = cellIndex;
              let ev = new Event("change");
              categoryOptionsEl.dispatchEvent(ev);
              cellOptionsEl.dispatchEvent(ev);
              setTimeout(() => {
                for (itemIndex of itemIdxs) {
                    let idx = `${itemIndex}`;
                    let o = rdbItemsEl.options[idx];
                    if (o) {
                        o.selected = true;
                    }
                    requestItemDrawings();
                }
              }, 200);
            });
        </script>
        </body>
        """.replace(
            "%path%", file.replace("\\", "\\\\")
        ),
    )
    body = body.replace(" shadow ", " shadow-none ")
    return body
