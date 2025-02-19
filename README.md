### Deploy LLM stack in kubernetes
1. `cd infra && helmfile apply`
2. `cd apps && helmfile -n dev apply`