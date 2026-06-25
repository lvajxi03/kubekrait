#!/usr/bin/env python3

"""
Core kubernetes module
"""


from kubernetes import client, config


class Krait:
    """
    Main krait client class
    """
    def __init__(self):
        """
        Default Krait constructor
        """
        self.api = None
        self.core = None
        self.apps = None

    def connect(self):
        """
        Connect to the Kubernetes cluster
        """
        try:
            config.load_incluster_config()
        except config.ConfigException:
            try:
                config.load_kube_config()
            except config.ConfigException as ce:
                raise ValueError("Failed to load Kubernetes configuration") from ce

        self.api = client.ApiClient()
        self.core = client.CoreV1Api(self.api)
        self.apps = client.AppsV1Api(self.api)

    def get_nodes(self):
        """
        Get all nodes in the cluster
        """
        return self.core.list_node().items

    def get_namespaces(self):
        """
        Get all namespaces in the cluster
        """
        return self.core.list_namespace().items

    def get_pods(self, namespace):
        """
        Get all pods in a given namespace
        """
        return self.core.list_namespaced_pod(namespace).items

    def get_pods_all(self):
        """
        Get all pods in the cluster
        """
        return self.core.list_pod_for_all_namespaces().items

    def get_configmaps(self, namespace):
        """
        Get all configmaps in a given namespace
        """
        return self.core.list_namespaced_config_map(namespace).items
