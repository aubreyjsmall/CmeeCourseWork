# Assignment 2 formative feedback

This feedback is organised by the relevant computing bootcamp criteria. Use it to decide what is already working, what you need to investigate, and what to revise before the cumulative submission.

The full criteria are in the [Computing Bootcamp assessment rubric](https://github.com/MulQuaBio/MQB/blob/main/content/rubrics/Computing_Bootcamp_Rubric.md).

## 1. Repository organisation and workflow discipline

- Your root README, `.gitignore`, cleaning script, test script and supplied data files are in the expected locations. The supplied CSV and metadata are unchanged, giving you a reproducible starting point.

## 2. Code completeness and functional correctness

- The cleaning script completed and produced the three output files. Separately, output checks found that the clean records, issues and oak summary tables satisfied the required output format and contents in both test runs. Those files are correct for the checked input; before final submission, test a few important edge cases.
- Re-run the separate tests and cleaning script after changes; inspect all three outputs, not just the exit status.

## 3. Code quality and style

- Your `main()` function gives the program a clear overall structure by connecting loading, processing, summarising and writing. Keep these stages distinct as you revise; use descriptive names and add short comments where the reason for a validation check or data-cleaning step is not obvious.

## 4. Documentation

- Your root README is in place. Make it useful to someone opening the repository for the first time: explain what the cleaner does, how to run the script and tests from the repository root, and which three files it creates. Test the instructions in a newly cloned copy of your repository (a separate folder created with `git clone`): enter that folder and run each README command exactly as written. If something fails, correct the command or add the missing step.

## 5. Version-control practice

- Since the previous formative feedback was added, the saved history contains 7 non-merge commits. Messages such as `Add tree survey data, metadata and starter program`, `Complete tree-survey cleaner, tests and README`, and `Fix converters, add input data, untrack results, tidy ignore` show a sequence of meaningful, working changes rather than one final upload.
- Keep this pattern for the final revisions. Before each commit, use `git diff --staged` to check that it contains one coherent, working change, then write a concise message that names that change and, where it is not obvious, why it was needed.

## 8. Basic error handling and input validation

- The supplied raw CSV and metadata remain unchanged. Your separate test file is present, contains 16 top-level assertion-style checks covering record validation, and completed successfully in the test run.
- **Check test coverage beyond individual validation decisions.** Your tests provide useful validation checks, but a successful run does not tell you whether every important part of the workflow is tested. Review whether they also check the flow of data into the accepted and rejected collections, oak summary and written outputs. Where needed, add a small example whose expected behaviour you can explain independently.
- Add the valid/invalid-record check above to `code/test_silwood_trees.py` as an assertion-based end-to-end test, keeping your existing function structure where it works.

## 9. Problem-solving approach and method implementation

- Your program follows this route: `main()` calls `load_records()` to read the supplied CSV, then `process_records()` uses `validate_record()` and returns `(clean_records, issues)`. The cleaned collection feeds `summarise_oaks()`, and three `write_csv()` calls produce the results. The route from input to outputs is clear.
- Before final submission, make this check visible in your repository. In `code/test_silwood_trees.py`, add or refine a small assertion-based test with one valid and one invalid record. Check that `process_records()` places them in the cleaned and issues collections respectively. Then pass the returned cleaned collection to `summarise_oaks()` and check that the invalid record does not contribute. Briefly explain this flow in your root README.
