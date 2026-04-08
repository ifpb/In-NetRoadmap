import os

from ..datatypes import get_datatype, get_source_from_type, translate_name
from ..renderer import render_template


def generate_p4(features: list, output_path: str) -> None:
    context = {
        "features": [],
    }

    for i, feature in enumerate(features, 1):
        context["features"].append(
            {
                "index": i,
                "name": translate_name(feature),
                "datatype": get_datatype(feature),
                "source": get_source_from_type(feature),
                "is_ipi": feature == "ipi",
            }
        )

    template_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = "decision_tree.p4.j2"

    render_template(
        template_dir,
        template_file,
        context,
        output_path,
    )
