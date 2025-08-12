import csv
import json
import os
from operator import itemgetter

import streamlit as st
import streamlit.components.v1 as components
from streamlit.components.v1.custom_component import CustomComponent

from streamlit_agraph import data
from streamlit_agraph.config import Config, ConfigBuilder
from streamlit_agraph.edge import Edge
from streamlit_agraph.node import Node
from streamlit_agraph.triple import Triple
from streamlit_agraph.triplestore import TripleStore

_RELEASE: bool = True

if _RELEASE:
    parent_dir: str = os.path.dirname(os.path.abspath(__file__))
    build_dir: str = os.path.join(parent_dir, "frontend/build")
    _agraph: CustomComponent = components.declare_component("agraph", path=build_dir)
else:
    _agraph: CustomComponent = components.declare_component(
        "agraph",
        url="http://localhost:3001",
    )


def agraph(nodes: list[Node], edges: list[Edge], config: Config):
    node_ids = [node.id for node in nodes]
    if len(node_ids) > len(set(node_ids)):
        st.warning("Duplicated node IDs exist.")
    nodes_data = [node.to_dict() for node in nodes]
    edges_data = [edge.to_dict() for edge in edges]
    config_json = json.dumps(config.__dict__)
    data = {"nodes": nodes_data, "edges": edges_data}
    data_json = json.dumps(data)
    component_value = _agraph(data=data_json, config=config_json)
    return component_value


if not _RELEASE:
    st.set_page_config(layout="wide")  # layout="wide"

    st.title("Streamlit Agraph 2.0")

    nodes, edges = data.load_graph_data()

    # Build the configs and save them to a file copy&paste dict to config directly.
    config_builder = ConfigBuilder(nodes)
    config = config_builder.build()
    # config.save("config.json")

    # config = Config(from_json="config.json")

    # config = Config(width=st.session_state.width,
    #                 height=st.session_state.height,
    #                 directed=st.session_state.directed,
    #                 physics=st.session_state.physics,
    #                 hierarchical=st.session_state.hierarchical,
    #                 **kwargs,
    #                 )

    return_value = agraph(nodes, edges, config=config)

    st.write(return_value)
