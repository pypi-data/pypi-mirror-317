from ldsi.predict.aggregation import majority
from ldsi.predict.chain_of_thought import ChainOfThought
from ldsi.predict.chain_of_thought_with_hint import ChainOfThoughtWithHint
from ldsi.predict.knn import KNN
from ldsi.predict.multi_chain_comparison import MultiChainComparison
from ldsi.predict.predict import Predict
from ldsi.predict.program_of_thought import ProgramOfThought
from ldsi.predict.react import ReAct, Tool
from ldsi.predict.parallel import Parallel

__all__ = [
    "majority",
    "ChainOfThought",
    "ChainOfThoughtWithHint",
    "KNN",
    "MultiChainComparison",
    "Predict",
    "ProgramOfThought",
    "ReAct",
    "Tool",
    "Parallel",
]
