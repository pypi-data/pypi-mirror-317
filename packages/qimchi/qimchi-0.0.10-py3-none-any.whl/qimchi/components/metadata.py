import json
from datetime import datetime

from dash import Input, Output, callback, html

# Local imports
from qimchi.components.utils import parse_data as parse
from qimchi.state import _state
from qimchi.logger import logger


def metadata_viewer() -> html.Div:
    """
    Metadata viewer

    Returns:
        dash.html.Div: Div element, displaying all the metadata relevant to the uploaded data

    """
    return html.Div(
        [
            html.Div(
                [
                    html.H5(
                        html.B("Metadata"), className="is-size-5 is-4 is-pulled-left"
                    ),
                    # Toggle button to show/hide metadata
                    html.Button(
                        html.I(className="fa-solid fa-eye-slash"),
                        id="hide-metadata",
                        className="button is-info is-pulled-right",
                    ),
                ],
                className="column is-full mt-0",
                style={
                    "minHeight": "4rem",
                },
            ),
            # Metadata viewer
            html.P(
                "",
                className="column is-full mt-0",
                id="metadata-viewer",
            ),
        ],
        className="has-background-light",
    )


def _render_tree(data: dict) -> html.Ul | html.Span:
    """
    Recursive function to render collapsible items

    """
    if isinstance(data, dict):
        return html.Ul(
            [
                html.Li(
                    # If the value is an empty list, empty string, empty dict, or None, render as "key: value" without a collapsible arrow
                    (
                        html.Span(
                            [
                                html.Strong(f"{key}", style={"color": "black"}),
                                f": {value}",
                            ]
                        )
                        if value in [None, [], "", {}]
                        else (
                            html.Span(
                                [
                                    html.Strong(f"{key}", style={"color": "black"}),
                                    f": {value}",
                                ]
                            )
                            if not isinstance(value, dict)
                            # Otherwise, make it collapsible, if it's a dictionary
                            else html.Details(
                                [
                                    html.Summary(
                                        html.Strong(key, style={"color": "black"}),
                                        style={"cursor": "pointer"},
                                    ),
                                    _render_tree(
                                        value
                                    ),  # NOTE: Recursively render nested dicts
                                ]
                            )
                        )
                    ),
                    style={
                        "listStyleType": "none",
                        "marginLeft": "20px",
                    },  # No bullets, indented
                )
                for key, value in data.items()
            ],
            style={"paddingLeft": "0px"},
        )
    else:
        # Render non-dict values directly as strings in a span
        return html.Span(str(data))


@callback(
    Output("metadata-viewer", "children"),
    Input("upload-data", "data"),
)
def update_metadata_viewer(contents: dict) -> list:
    """
    Callback to update metadata viewer

    Args:
        contents (dict): Dict representation of xarray.Dataset

    Returns:
        list: Metadata list to be displayed in the metadata viewer

    """
    if contents is None:
        logger.warning("update_metadata_viewer | No data uploaded")
        return "No Data Uploaded"

    data = parse(contents)
    metadata = data.attrs
    dt = datetime.fromisoformat(metadata["Timestamp"])
    meta = []
    meta_expandable = []

    keys_order = [
        "Timestamp",
        "Cryostat",
        "Wafer ID",
        "Device Type",
        "Sample Name",
        "Experiment Name",
        "Measurement ID",
        "Extra Metadata",
        "Instruments Snapshot",
        "Parameters Snapshot",
        "Sweeps",
    ]
    # Sort keys in the order defined above
    metadata = {k: metadata[k] for k in keys_order if k in metadata}

    json_keys = [
        "Extra Metadata",
        "Instruments Snapshot",
        "Parameters Snapshot",
        "Sweeps",
    ]

    # Store "Parameters Snapshot" in _state
    if "Parameters Snapshot" in metadata:
        _state.parameters_snapshot = metadata["Parameters Snapshot"]
        _state.save_state()

    for key in metadata:
        if key == "Timestamp":
            meta.append(html.B(f"{key}: "))
            meta.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
            meta.append(html.Br())

        elif key == "Cryostat":
            meta.append(html.B(f"{key}: "))
            data = metadata[key].capitalize()
            meta.append(data)
            meta.append(html.Br())

        elif key in json_keys:
            meta_expandable.append(html.B(f"{key}: "))
            try:
                data: str = metadata[key]
                data: dict = json.loads(data)
            except Exception as err:
                logger.error(f"update_metadata_viewer | Error: {err}", exc_info=True)
                raise err

            for k, v in data.items():  # key: str | val: dict
                meta_expandable.append(
                    html.Details(
                        [
                            html.Summary(
                                html.Strong(f"{k.upper()}", style={"color": "black"}),
                                style={"cursor": "pointer"},
                            ),
                            _render_tree(v),
                        ],
                        className="ml-4",
                    ),
                )

        else:
            meta.append(html.B(f"{key}: "))
            meta.append(metadata[key])
            meta.append(html.Br())

    # Non-collaspible stuff to the left & collapsible stuff to the right
    meta = html.Div(
        [
            html.Div(meta, style={"float": "left", "width": "50%"}),
            html.Div(meta_expandable, style={"float": "right", "width": "50%"}),
        ]
    )

    return meta


@callback(
    Output("metadata-viewer", "className"),
    Output("hide-metadata", "children"),
    Input("hide-metadata", "n_clicks"),
)
def show_hide_metadata(n_clicks: int) -> tuple:
    """
    Callback to show or hide the metadata viewer

    Args:
        n_clicks (int): Number of times the button has been clicked

    Returns:
        tuple: className to display the metadata viewer and the updated button icon

    """
    if n_clicks is None or n_clicks % 2 == 0:
        return "column is-full mt-0", html.I(className="fa-solid fa-eye-slash")
    else:
        return "column is-hidden mt-0", html.I(className="fa-solid fa-eye")
