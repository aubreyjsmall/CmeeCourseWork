# Assignment 1 feedback - Aubrey Small

**Formative feedback | Rubric 2026.2**

The README's expected/observed tests are useful, particularly the empty-field, spaced-filename, repeat-run and input-preservation checks. All five FASTA answers matched the independent checks, and their explanations identify what the commands count.

The missing inputs need attention first. Your own TSV and all four temperature files are absent from the required paths, even though the local test account describes converter runs. Include them in the repository so a fresh checkout can reproduce the assessed work. The supplied-data conversions were not run with replacement inputs.

In the converters, correct the ../results assumption for repository-root execution. Also change the capitalised Echo in tabtocsv.sh: shell command names are case-sensitive, so it produces a command-not-found error even if later operations continue. Keep the useful argument/readability and conversion-status checks.

Four generated test outputs are still tracked. Untrack those, simplify the repeated ignore entries and add a results rule. Then repeat the documented tests from the corrected checkout, not only against disposable files in a local sandbox. Add dependencies and any help account, and preserve the useful explanations. The aim is to make the repository itself support the testing story already in the README.

---

## Project structure

Relevant tracked layout (simplified; missing required paths are marked):

```text
README.md
.gitignore
code/  unixPrac1.txt, tabtocsv.sh, csvtospace.sh
data/fasta/  3 required files present
data/temperatures/  missing here: 1800.csv, 1801.csv, 1802.csv, 1803.csv
data/tab-example.tsv [missing]
results/  4 files tracked
sandbox/  no files tracked; optional
```

The root README, ignore file, assessed code and FASTA inputs are present. The own TSV and all four temperature inputs are missing. Four generated test outputs are tracked under results/; sandbox is ignored, with repeated entries in the ignore file.

Supply the missing input data, untrack generated test outputs and add one clear results rule. Simplify duplicate ignore entries without removing useful protection. A fresh checkout should contain the inputs needed for the README's test account, not just the output files from an earlier local run.

**Assessed snapshot:** `b3d2f78eeb42e017c7f891ac840433d1a466a0f9`
