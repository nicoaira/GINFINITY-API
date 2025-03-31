FROM continuumio/miniconda3

ENV PYTHONUNBUFFERED=1

# Copy your environment file into the container.
COPY environment.yml /tmp/environment.yml

# Create the conda environment from the environment file and clean up
RUN conda env create -f /tmp/environment.yml && conda clean -afy

# Set the working directory inside the container
WORKDIR /app

# Declare /app as a volume so you can mount your project directory at runtime
VOLUME ["/app"]

# Expose the port that uvicorn will use
EXPOSE 8000

# Ensure Python outputs logs immediately
ENV PYTHONUNBUFFERED=1

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN apt-get update && apt-get install -y dos2unix
RUN dos2unix /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script to start the app
ENTRYPOINT ["/entrypoint.sh"]


