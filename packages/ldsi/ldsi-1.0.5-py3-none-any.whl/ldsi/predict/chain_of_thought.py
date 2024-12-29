import ldsi
from ldsi.primitives.program import Module
from ldsi.signatures.signature import ensure_signature


class ChainOfThought(Module):
    def __init__(self, signature, rationale_type=None, **config):
        super().__init__()

        signature = ensure_signature(signature)

        prefix = "Reasoning: Let's think step by step in order to"
        desc = "${reasoning}"
        rationale_type = rationale_type or ldsi.OutputField(prefix=prefix, desc=desc)
        extended_signature = signature.prepend("reasoning", rationale_type, type_=str)
        
        self.predict = ldsi.Predict(extended_signature, **config)

    def forward(self, **kwargs):
        return self.predict(**kwargs)
