# Assignment 3 formative feedback

This feedback is organised using the [Computing Bootcamp rubric](https://mulquabio.github.io/MQB/rubrics/Computing_Bootcamp_Rubric.html). It does not award a mark; use it to decide what to revise and check before final submission.

## Criterion 1: Repository organisation & workflow discipline

Before final submission, check that the required scripts are under `code/`, supplied inputs are under `data/`, and generated files remain outside Git.

## Criterion 2: Code completeness & functional correctness

- The fixed tree-height script ran and generated `results/TreeHts.csv`; the output check confirmed the required columns and values. Your code and README also include an independent trigonometric check of one height, providing a useful way to connect measurements to results.
- Before final submission, **Complete and test the generalised tree-height route separately.** The required `code/run_get_TreeHeight.sh` is missing, so the normal generalised route was not validated and its output content was not collected. Test this programme separately from the fixed script. Add the wrapper, then check that it passes the input path correctly to the R script. Your code also shows `_treeheight.csv`, whereas the required output for `trees.csv` is `results/trees_treeheights.csv`: compare the filename actually created with the required spelling.

## Criterion 3: Code quality & style

As you revise, keep names descriptive, use comments to explain decisions rather than restating code, and avoid repeating the same calculation in several places.

## Criterion 4: Documentation

- Before final submission, **Make the README describe the two routes accurately.** Its fixed-script command conflicts with descriptions of accepting an argument and constructing an output filename; it also mixes `results/` and `../results/`. This makes reproduction unnecessarily uncertain. Give separate fixed and generalised usage examples, with exact inputs and outputs. Explain that these commands run from the directory containing `code/`, `data/` and the root `README.md`. Fill blank test observations only after running the checks.

## Criterion 5: Version-control practice

- When I opened the figure, I found readable figure axes and plot-level points. The repository also keeps generated results out of Git, and your Git history includes descriptive code and documentation commits.

## Criterion 8: Basic error-handling & input validation

- Before final submission, **Check that validation rejects the intended problem, not a different one.** The invalid-input tests expected stopping/no-output behaviour, with numeric and finite-number errors. Add the targeted validation check below. Both tree scripts compare the column class with `"numeric"`, which can reject valid integer-valued numeric columns. Try a small valid CSV containing whole-number measurements and use a numeric-type check that accepts these. Then change just one value to an invalid value and inspect the error and output behaviour.

## Criterion 9: Problem-solving approach & method implementation

- The Pound Hill script ran, and `results/pound_hill_plot_richness.csv` had the expected rows, plot identifiers and richness values. Your code shows the route from species presence to quadrat richness and then mean richness within plots. Your interpretation acknowledges plot-to-plot variation and avoids claiming causation from the figure alone.
- Before final submission, **Make overlapping figure points easier to interpret.** I found that equal or near-equal values can hide individual plots. Consider a small horizontal displacement or another simple display adjustment that preserves richness values. Compare the revised PDF with the CSV to confirm that all plots are represented; retain your cautious biological interpretation.

## Criterion 10: Learning progression demonstration

Use this feedback as a revision checklist. Make the changes in small, descriptive commits, then add a short README note explaining what you changed and how you checked it. This will make your development from this formative checkpoint visible in the final portfolio.

## Priorities before final submission

- After revising, rerun one ordinary and one invalid case for each tree-height route from the project root. Check filenames, headers, row counts, one independently calculated height, and that invalid input produces a useful error without writing a new result. Open the regenerated Pound Hill PDF rather than checking only that it exists, then update the README and commit the changes descriptively.
