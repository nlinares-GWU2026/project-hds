FROM condaforge/miniforge3@sha256:006e761a6dcdb6e19e885c54616cad054c960a1191ce92fdf6fbbb9b34e9a279

WORKDIR /workspace

# environment.yml installs aadrkit itself (pip: -e .), so the package
# source must be in the image before the environment is created.
COPY environment.yml pyproject.toml ./
COPY src/ src/
RUN mamba env create -f environment.yml && mamba clean -afy

COPY tests/ tests/

# Run aadrkit by default; with no arguments, show its help.
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "aadr-project", "aadrkit"]
CMD ["--help"]