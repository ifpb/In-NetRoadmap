import os

from ..datatypes import get_datatype, get_source_from_type, translate_name
from ..renderer import render_template


def generate_p4(n_classes: int, features: list, output_path: str) -> None:
    # O template Jinja2 espera uma lista de identificadores de classes (ex: [0, 1])
    # para poder iterar na criação das variáveis (score_class0, score_class1, etc)
    context = {
        "classes": list(range(n_classes)),
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
