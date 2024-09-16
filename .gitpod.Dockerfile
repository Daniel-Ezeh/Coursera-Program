# .gitpod.Dockerfile
FROM gitpod/workspace-full

# Install Docker Compose
RUN sudo apt-get update && \
    sudo apt-get install -y docker-compose