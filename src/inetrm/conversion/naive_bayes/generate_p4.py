import os

from ..datatypes import get_datatype, get_source_from_type, translate_name
from ..renderer import render_template


def generate_p4(n_classes: int, features: list, output_path: str) -> None:
    raise NotImplementedError("TODO generate p4 for naive bayes")
    context = {
        "n_classes": n_classes,
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
    template_file = "naive_bayes.p4.j2"

    render_template(
        template_dir,
        template_file,
        context,
        output_path,
    )
