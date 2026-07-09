## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Learning or practicing k8s / Kubernetes concepts → invoke k8s-coach
- Preparing for DevOps / SRE interviews → invoke k8s-coach
- k8s troubleshooting, debugging, or fault drill → invoke k8s-coach
- Studying EKS, CNI, Service, Ingress, scheduling, autoscaling, 高並發/high-concurrency, observability/可觀測性 → invoke k8s-coach
- CKA / CKAD prep or k8s hands-on lab → invoke k8s-coach
