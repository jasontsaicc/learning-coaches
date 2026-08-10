# AI Infra Capstone(placeholder,~2027 Q1 起跑)

Self-hosted LLM inference on EKS/kind:autoscaling + observability + cost dashboard。
規劃見 `docs/plans/2026-08-11-module-roadmap.md`;起跑條件:k8s/sd 第一輪走完。

預計結構(待補):`terraform/`(EKS + GPU node group)、`manifests/`(inference server + HPA)、
`observability/`(SLO + GPU metrics)、`notes/`(英文 design notes)。
