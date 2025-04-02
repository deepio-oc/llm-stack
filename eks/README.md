1. bring up cluster in EKS: `eksctl create cluster -f cluster.yaml`
2. follow ../README.md to install infra and app components.
3. shutdown node(s) when done using: `eksctl delete nodegroup --approve -f cluster.yaml`
4. create nodes when needed: `eksctl create nodegroup  -f cluster.yaml` (no need to reinstall llm-stack)