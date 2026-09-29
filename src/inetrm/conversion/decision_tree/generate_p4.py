import os

from ..datatypes import get_datatype, get_source_from_type, translate_name
from ..renderer import render_template

import math


def generate_p4(features, output_path, n_rules, n_classes):
    context = {
        "features": [],
        "result_width": max(1, math.ceil(math.log2(max(2, n_classes)))),
        "table_size": 2 ** max(3, math.ceil(math.log2(max(1, n_rules)))),
        "n_classes": n_classes,
    }

    for i, feature in enumerate(features, 1):
        context["features"].append({
            "index": i,
            "name": translate_name(feature),
            "datatype": get_datatype(feature),
            "source": get_source_from_type(feature),
            "is_ipi": feature == "ipi",
        })

    template_dir = os.path.dirname(os.path.abspath(__file__))
    render_template(template_dir, "decision_tree.p4.j2", context, output_path)
