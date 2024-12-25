# AI Network DAG SDK

A Python SDK for interacting with AI Network's DAG-based storage and communication services.

## Installation

```bash
pip install ai-network-dag-sdk

```proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./AINetworkDagSdk/proto/ai-network-dag.proto


```publish
python setup.py sdist bdist_wheel
twine upload dist/*