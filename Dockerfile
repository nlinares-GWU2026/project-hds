FROM condaforge/miniforge3:latest
WORKDIR /workspace
COPY environment.yml .
RUN mamba env create -f environment.yml && mamba clean -afy
COPY src/ src/
SHELL ["conda", "run", "-n", "aadr-project", "/bin/bash", "-c"]
CMD ["conda", "run", "--no-capture-output", "-n", "aadr-project", "python", "src/placeholder.py"]
