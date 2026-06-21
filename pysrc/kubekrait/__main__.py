#!/usr/bin/env python3

"""
KubeKrait main module
"""


import argparse
import sys
import json
import yaml
from kubekrait.core.krait import Krait


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KubeKrait - Ultimate Kubernetes Client")
    parser.add_argument("--json", "-j", help="Print cluster data as JSON", action="store_true")
    parser.add_argument("--yaml", "-y", help="Print cluster data as YAML", action="store_true")

    args = parser.parse_args()
    if args.json and args.yaml:
        print("Cannot specify both --json and --yaml")
        sys.exit(1)

    krait = Krait()
    krait.connect()

    namespaces = krait.get_namespaces()
    clusterdata = {}
    for ns in namespaces:
        clusterdata[ns.metadata.name] = []

    pods = krait.get_pods_all()
    for pod in pods:
        if pod.metadata.namespace in clusterdata:
            clusterdata[pod.metadata.namespace].append(pod.metadata.name)

    if args.json:
        print(json.dumps(clusterdata, indent=2))
    elif args.yaml:
        print(yaml.dump(clusterdata, default_flow_style=False))
    else:
        for ns, pods in clusterdata.items():
            print(f"Namespace: {ns}")
            for pod in pods:
                print(f"  - {pod}")
