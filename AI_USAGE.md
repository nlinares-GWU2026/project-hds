## 09/01/2026 ##
- I asked Claude what kind of `bioconda` package that I would need instead of `samtools` for my project idea. My project goal is to work with AADR data which uses `eigensoft` to work with and analyze the data:
" Do I need to have the "::eigensoft" at the end of bioconda?" Which Claude said yes because AADR uses eigensoft to analyze the data.

- I also asked Claude when setting up my Dockerfile how I should copy the scripts into the environment because the week 2 informtion had the example of `analyze.py` where I would be using my own scripts for the project: " CMD ["conda", "run", "--no-capture-output", "-n", "aadr-project", "pyton", "src/"] I do not have a script yet, can i just input it like this?" I created a placeholder script with the suggestion of Claude to test the environments and to create the Dockerfile so there wasn't an issue with just directing it to an empty folder. 
