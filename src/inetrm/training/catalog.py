class Model:
    MODEL_CATALOG = {"decision_tree"}
    FEATURE_CATALOG = {"sport", "dport"}
    JUPYTER_MAPPING = {"decision_tree": "train_DT.ipynb"}

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
