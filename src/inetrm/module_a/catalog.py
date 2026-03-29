class Model:
    MODEL_CATALOG = ['decision_tree']
    FEATURE_CATALOG = ['sport', 'dport']
    JUPYTER_MAPPING = {"decision_tree": "train_DT.ipynb"}

    def __init__(self, model:str, features:list):
        assert model in Model.MODEL_CATALOG, f"Model {model} not supported."
        for feature in features: assert feature in Model.FEATURE_CATALOG, f"Feature {feature} not supported"

        self.model = model
        self.features = features
