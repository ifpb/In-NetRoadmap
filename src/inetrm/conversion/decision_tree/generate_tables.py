from ..datatypes import get_datatype


def _max_value(feature_name):
    """Valor máximo representável no campo P4 da feature."""
    bits = get_datatype(feature_name)
    return (2 ** bits) - 1 if bits else (2 ** 48) - 1


def generate_tables(regras, features, output_path):
    """
    Gera uma entrada por regra no formato:
      table_add decision_tree set_result <lo->hi> ... => <class> <priority>
    As regras de uma decision tree são disjuntas, então a prioridade
    é apenas defensiva (maior = avaliada primeiro em caso de overlap).
    """
    n = len(regras)

    with open(output_path, "w") as f:
        for i, regra in enumerate(regras):
            ranges = []
            for fea in features:
                lo = regra["bounds"][fea]["lo"]
                hi = regra["bounds"][fea]["hi"]
                if hi is None:
                    hi = _max_value(fea)
                ranges.append((lo, hi))

            priority = n - i  # decrescente; irrelevante se disjunto
            range_str = " ".join(f"{lo}->{hi}" for lo, hi in ranges)
            f.write(
                f"table_add decision_tree set_result "
                f"{range_str} => {regra['class']} {priority}\n"
            )
