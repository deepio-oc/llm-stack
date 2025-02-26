### Install helmfile
1. Download and install helmfile from https://github.com/helmfile/helmfile/releases/tag/v0.171.0
2. Download and install helm from https://github.com/helm/helm/releases/tag/v3.17.1
3. Install helm diff plugin: `helm plugin install https://github.com/databus23/helm-diff`

### Deploy LLM stack in kubernetes
1. `export CF_API_TOKEN=<cloudflare_api_token>`
2. `cd infra && helmfile apply`
3. `cd apps && helmfile -n dev apply`