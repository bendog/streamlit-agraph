import json
import os
from typing import Annotated, Any, Literal, TypedDict

import streamlit as st


class StabilizationConfig(TypedDict, total=False):
    enabled: bool
    fit: bool


class PysicsConfig(TypedDict, total=False):
    enabled: bool
    solver: str
    minVelocity: int
    maxVelocity: int
    stabilization: StabilizationConfig
    timestep: float


class HierarchicalConfig(TypedDict, total=False):
    enabled: bool
    levelSeparation: int
    nodeSpacing: int
    treeSpacing: int
    blockShifting: bool
    edgeMinimization: bool
    parentCentralization: bool
    direction: Annotated[str, Literal["UD", "DU", "LR", "RL"]]  # UD, DU, LR, RL
    sortMethod: Annotated[str, Literal["hubsize", "directed"]]  # hubsize, directed
    shakeTowards: Annotated[str, Literal["roots", "leaves"]]  # roots, leaves


class LayoutConfig(TypedDict, total=False):
    hierarchical: HierarchicalConfig


class Config:
    """Configuration class for the agraph component."""

    @classmethod
    def from_json(cls, path: str):
        """Create a Config instance from a JSON file."""
        with open(path, "r") as f:
            config_dict = json.load(f)
        return cls(**config_dict)

    def __init__(
        self,
        height: int = 750,
        width: int = 750,
        directed: bool = True,
        physics: PysicsConfig | bool = True,
        layout: LayoutConfig | None = None,
        hierarchical: bool = False,
        from_json: dict[str, Any] | None = None,
        **kwargs,
    ):
        if from_json:
            raise DeprecationWarning(
                "from_json is deprecated, use Config.from_json(path) at instance creation instead."
            )

        self.height: str = f"{height}px"
        self.width: str = f"{width}px"
        if not directed:
            self.edges: dict[str, Any] = {"arrows": "none"}

        # https://visjs.github.io/vis-network/docs/network/physics.html#
        if isinstance(physics, dict):
            # if physics is a dict, use it directly
            self.physics: PysicsConfig = PysicsConfig(**physics)
        else:
            # this is legacy functionality, convert to dict
            self.physics: PysicsConfig = {
                "enabled": physics,
                "solver": kwargs.pop("solver", "barnesHut"),
                "minVelocity": kwargs.pop("minVelocity", 1),
                "maxVelocity": kwargs.pop("maxVelocity", 100),
                "stabilization": {
                    "enabled": kwargs.pop("stabilization", True),
                    "fit": kwargs.pop("fit", True),
                },
                "timestep": kwargs.pop("timestep", 0.5),
            }
        # https://visjs.github.io/vis-network/docs/network/layout.html
        if isinstance(layout, dict):
            # if layout is a dict, use it directly
            self.layout: LayoutConfig = LayoutConfig(**layout)
        else:
            self.layout: LayoutConfig = {
                "hierarchical": {
                    "enabled": hierarchical,
                    "levelSeparation": kwargs.pop("levelSeparation", 150),
                    "nodeSpacing": kwargs.pop("nodeSpacing", 100),
                    "treeSpacing": kwargs.pop("treeSpacing", 200),
                    "blockShifting": kwargs.pop("blockShifting", True),
                    "edgeMinimization": kwargs.pop("edgeMinimization", True),
                    "parentCentralization": kwargs.pop("parentCentralization", True),
                    "direction": kwargs.pop("direction", "UD"),  # UD, DU, LR, RL
                    "sortMethod": kwargs.pop("sortMethod", "hubsize"),  # hubsize, directed
                    "shakeTowards": kwargs.pop("shakeTowards", "roots"),  # roots, leaves
                }
            }
        self.groups = kwargs.pop("groups", None)

        # set the remaining kwargs as attributes
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return self.__dict__

    def save(self, path):
        config_json = json.dumps(self.to_dict(), indent=2)
        if os.path.isabs(path):
            save_path = path
        else:
            directory = os.getcwd()
            save_path = os.path.join(directory, path)
        with open(save_path, "w") as file:
            file.write(config_json)


class ConfigBuilder(object):
    def __init__(self, nodes=None, edges=None, **kwargs):
        self.kwargs: dict[str, Any] = kwargs
        self.nodes = nodes
        st.sidebar.write("Agraph Configurations")
        # TODO: I am not sure what the below lines do, it looks like they would destroy themselves on run?
        self.basic_widget = self.basic_widget()
        self.physics_widget = self.physics_widget()
        self.hierarchical_widget = self.hierarchical_widget()
        self.groups = self.group_widget()

    def basic_widget(self):
        basic_expander = st.sidebar.expander("Basic Config", expanded=True)
        with basic_expander:
            basic_expander.number_input(
                "height", value=self.kwargs.get("height", 750), key="height"
            )
            basic_expander.number_input("width", value=self.kwargs.get("width", 750), key="width")
            basic_expander.checkbox(
                "directed", value=self.kwargs.get("directed", True), key="directed"
            )
            self.kwargs["height"] = st.session_state.height
            self.kwargs["width"] = st.session_state.width
            self.kwargs["directed"] = st.session_state.directed

    def physics_widget(self):
        physics_expander = st.sidebar.expander("Physics Config", expanded=False)
        with physics_expander:
            physics_expander.checkbox(
                "physics", value=self.kwargs.get("physics", True), key="physics"
            )
            solvers = ["barnesHut", "forceAtlas2Based", "hierarchicalRepulsion", "repulsion"]
            physics_expander.selectbox(
                "Solver", options=solvers, index=self._get_index(solvers, "solver"), key="solver"
            )
            physics_expander.number_input(
                "minVelocity", value=self.kwargs.get("minVelocity", 1), key="minVelocity"
            )
            physics_expander.number_input(
                "maxVelocity", value=self.kwargs.get("maxVelocity", 100), key="maxVelocity"
            )
            physics_expander.checkbox(
                "stabilize", value=self.kwargs.get("stabilization", True), key="stabilize"
            )
            physics_expander.checkbox("fit", value=self.kwargs.get("fit", True), key="fit")
            physics_expander.number_input(
                "timestep", value=self.kwargs.get("timestep", 0.5), key="timestep"
            )

            self.kwargs["physics"] = st.session_state.physics
            self.kwargs["minVelocity"] = st.session_state.minVelocity
            self.kwargs["maxVelocity"] = st.session_state.maxVelocity
            self.kwargs["stabilization"] = st.session_state.stabilize
            self.kwargs["fit"] = st.session_state.fit
            self.kwargs["timestep"] = st.session_state.timestep
            self.kwargs["solver"] = st.session_state.solver

    def hierarchical_widget(self):
        hierarchical_expander = st.sidebar.expander("Hierarchical Config", expanded=False)
        with hierarchical_expander:

            def set_physics_off():
                if st.session_state.hierarchical:
                    st.session_state.physics = False

            hierarchical_expander.checkbox(
                "hierarchical",
                value=self.kwargs.get("hierarchical", False),
                key="hierarchical",
                on_change=set_physics_off,
            )
            hierarchical_expander.number_input(
                "levelSeparation",
                value=self.kwargs.get("levelSeparation", 150),
                key="levelSeparation",
            )
            hierarchical_expander.number_input(
                "nodeSpacing", value=self.kwargs.get("nodeSpacing", 100), key="nodeSpacing"
            )
            hierarchical_expander.number_input(
                "treeSpacing", value=self.kwargs.get("treeSpacing", 200), key="treeSpacing"
            )
            hierarchical_expander.checkbox(
                "blockShifting", value=self.kwargs.get("blockShifting", True), key="blockShifting"
            )
            hierarchical_expander.checkbox(
                "edgeMinimization",
                value=self.kwargs.get("edgeMinimization", True),
                key="edgeMinimization",
            )
            hierarchical_expander.checkbox(
                "parentCentralization",
                value=self.kwargs.get("parentCentralization", True),
                key="parentCentralization",
            )
            directions = ["UD", "DU", "LR", "RL"]
            hierarchical_expander.selectbox(
                "direction",
                options=directions,
                index=self._get_index(directions, "direction"),
                key="direction",
            )
            sortmethods = ["hubsize", "directed"]
            hierarchical_expander.selectbox(
                "sortMethod",
                options=sortmethods,
                index=self._get_index(sortmethods, "sortMethod"),
                key="sortMethod",
            )
            shaketowards = ["roots", "leaves"]
            hierarchical_expander.selectbox(
                "shakeTowards",
                options=shaketowards,
                index=self._get_index(shaketowards, "shakeTowards"),
                key="shakeTowards",
            )
            self.kwargs.update(
                {
                    "hierarchical": st.session_state.hierarchical,
                    "levelSeparation": st.session_state.levelSeparation,
                    "nodeSpacing": st.session_state.nodeSpacing,
                    "treeSpacing": st.session_state.treeSpacing,
                    "blockShifting": st.session_state.blockShifting,
                    "edgeMinimization": st.session_state.edgeMinimization,
                    "parentCentralization": st.session_state.parentCentralization,
                    "direction": st.session_state.direction,
                    "sortMethod": st.session_state.sortMethod,
                    "shakeTowards": st.session_state.shakeTowards,
                }
            )

    def group_widget(self):
        group_expander = st.sidebar.expander("Group Config", expanded=False)
        group_expander.checkbox("groups", value=self.kwargs.get("groups", False), key="groups")
        if st.session_state.groups:
            if self.nodes:
                groups = list({node.__dict__.get("group", None) for node in self.nodes})
                if None in groups:
                    groups.remove(None)
                with group_expander:
                    groups_dict = {}
                    for group in groups:
                        st.write(f"Group: {group}")
                        group_expander.text_input(
                            "Color (hex)", value=" #fe8a71", key=f"group_{group}"
                        )
                        groups_dict[group] = {"color": st.session_state[f"group_{group}"]}
                    self.kwargs.update({"groups": groups_dict})

    def build(self, dictify=False) -> Config | dict[str, Any]:
        # self.physics_widget()
        # self.hierarchical_widget()
        if dictify:
            return self.kwargs
        return Config(**self.kwargs)

    def _get_index(self, options, target):
        val = self.kwargs.get(target, None)
        if val is None:
            return 0
        try:
            index = options.index(val)
        except ValueError:
            index = 0
        return index
