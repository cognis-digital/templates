import * as docker from "@pulumi/docker";
const img = new docker.RemoteImage("app", { name: "ghcr.io/cognis-digital/app:latest" });
new docker.Container("app", { image: img.repoDigest, ports: [{ internal: 8000, external: 8000 }] });
