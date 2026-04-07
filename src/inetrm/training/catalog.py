class Model:
    MODEL_CATALOG = {"decision_tree",
                     "naive_bayes",
                     }
    FEATURE_CATALOG = {
        "sport",
        "dport",
        "tos",
        "length",
        "id",
        "ttl",
        "chksum",
        "seq",
        "ack",
        "window",
        "frame_size",
        "ipi",
        "flags",
        "frag",
        "ihl",
        "proto",
        "dataofs",
        "urgptr",
        "reserved",
        "tcp_chk",
        "urg",
        "ece",
        "cwr",
        "payload_length",
    }
    JUPYTER_MAPPING = {"decision_tree": "train_DT.ipynb",
                       "naive_bayes": "train_NB.ipynb",
                       }

    def __init__(self, model: str, features: list):
        if model not in self.MODEL_CATALOG:
            raise ValueError(
                f"Model '{model}' not supported. Allowed models are: {self.MODEL_CATALOG}"
            )

        for feature in features:
            if feature not in self.FEATURE_CATALOG:
                raise ValueError(
                    f"Feature '{feature}' not supported. Allowed features are: {self.FEATURE_CATALOG}"
                )

        self.model = model
        self.features = features
