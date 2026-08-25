import os

from ..datatypes import get_datatype, get_source_from_type, translate_name
from ..renderer import render_template

def generate_p4(features: list, regras_dict: dict, output_path: str) -> None:
    context = {
        "features": [],
        "trees": [],
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

    for idx, (tree_name, regras_list) in enumerate(regras_dict.items()):
        features_used = [f["index"] for f in context["features"]]
        
        context["trees"].append({
            "index": idx,
            "name": tree_name,
            "features_used": features_used
        })

    template_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = "xgboost_binary.p4.j2" 

    render_template(
        template_dir,
        template_file,
        context,
        output_path,
    )
