"""Convert a ComfyUI UI-format workflow JSON into API-format using the live server's
/object_info as the source of truth for each node class's input order.
Usage: python graph_to_prompt.py workflow.json > prompt.json
"""
import json
import sys
import urllib.request

SERVER = "http://127.0.0.1:8188"


def get_object_info(class_type):
    with urllib.request.urlopen(f"{SERVER}/object_info/{class_type}") as r:
        d = json.load(r)
    return list(d.values())[0]


PRIMITIVE_TYPES = {"INT", "FLOAT", "STRING", "BOOLEAN", "COMBO"}


def is_widget_type(spec):
    # spec is like ["INT", {...}] or [["opt1","opt2"], {...}] or just a bare type string
    t = spec[0] if isinstance(spec, list) else spec
    if isinstance(t, list):
        return True  # combo/dropdown -> widget
    return t in PRIMITIVE_TYPES


def convert(workflow_path):
    with open(workflow_path) as f:
        wf = json.load(f)

    nodes = wf["nodes"]
    link_src = {}
    for link in wf["links"]:
        link_id, src_node, src_slot = link[0], link[1], link[2]
        link_src[link_id] = (src_node, src_slot)

    prompt = {}
    info_cache = {}

    for n in nodes:
        if n["type"] in ("Note", "Reroute", "MarkdownNote"):
            continue
        if n["type"] not in info_cache:
            try:
                info_cache[n["type"]] = get_object_info(n["type"])
            except Exception as e:
                print(f"FAILED for node {n['id']} type {n['type']!r}: {e}", file=sys.stderr)
                raise
        info = info_cache[n["type"]]
        req = info["input"].get("required", {})
        opt = info["input"].get("optional", {})
        all_items = list(req.items()) + list(opt.items())

        # widget-eligible keys, in INPUT_TYPES order (widgets_values only has a slot
        # for these -- primitive/combo types -- never for socket types like IMAGE/VAE/MODEL)
        widget_keys = [k for k, spec in all_items if is_widget_type(spec)]

        inputs = {}
        wv = n.get("widgets_values", [])
        if isinstance(wv, dict):
            for k, v in wv.items():
                if k in widget_keys:
                    inputs[k] = v
        else:
            for k, v in zip(widget_keys, wv):
                inputs[k] = v

        # links override whatever was zipped in from widgets_values (stale slot)
        for i in n.get("inputs", []):
            if i.get("link") is not None:
                link_id = i["link"]
                if link_id in link_src:
                    src_node, src_slot = link_src[link_id]
                    inputs[i["name"]] = [str(src_node), src_slot]

        prompt[str(n["id"])] = {"class_type": n["type"], "inputs": inputs}

    return prompt


if __name__ == "__main__":
    result = convert(sys.argv[1])
    print(json.dumps(result, indent=2))
