from .nodeinfo import NodeInfo


def test_nodeinfo():
    result = NodeInfo(software={"name": "bovine", "version": "0.0.0"}).model_dump()

    assert result["version"] == "2.0"
