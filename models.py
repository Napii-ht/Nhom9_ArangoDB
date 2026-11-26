from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

Graph = Dict[str, List[Tuple[str, float]]]
@dataclass
class PlantedPatterns:
    cycles: List[List[str]] = field(default_factory=list)
    shell_chains: List[List[str]] = field(default_factory=list)
    hidden_links: List[Tuple[str, str]] = field(default_factory=list)
    shell_nodes: Set[str] = field(default_factory=set)
