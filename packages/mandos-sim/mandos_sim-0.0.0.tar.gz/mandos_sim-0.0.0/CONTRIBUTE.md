# Contributions to MANDOS

In Mandos, the default branch is **main** and is protected. Every contribution to the default branch must come from a merge request and will be reviewed by Mandos maintainers.

**main** branch history is linear and merge request must be rebased on top of the main branch to keep the history clean. All MRs are merged as fast forward merges.

# LICENSE
Mandos is under the MIT license.
Any contribution to Mandos must be signed, accepting the conditions of the LICENSE

## Automatic tools

In Mandos, we use several tools to automatically ensure the quality of the contributed code.

* _clang-format_ and _cmake-format_ to ensure code style consistency.
* _clang-tidy_ to ensure best coding practices.
* ASAN builds to enure correct memory management
* UBSAN builds to ensure there is not undefined behavior

We recommend using _clang_format_ and _cmake-format_ before pushing code, to ensure the CI job will succeed. You can configure several IDEs to perform automatic formatting on save. 

## Unit testing

To ensure code works as expected, each MR must provide tests for the contributed code. We use Catch2 (<https://github.com/catchorg/Catch2>) as testing framework.

## CI

We use a CI workflow to ensure all the merge requests meet our code quality criteria.

* Precheck stage
  * Formatting check
  * Fast forward check
* x86_64 Release
  * Build x86_64 CI presets for different compilers
  * Test x86_64 CI presets
* Quality check
  * _clang-tidy_ checks
* x86_64 Debug
  * Build x86_64-asan presets for different compilers
  * Test x86_64-asan builds
  * Build x86_64-ubsan presets for different compilers
  * Test x86_64-ubsan builds

Testing is done in a docker context. We provide a Dockerfile under `<src>/ci` if you want to develop under the same context.

## Code review

All the contributions will be reviewed by Mandos maintainers. To simplify the review process we strongly suggest to make a MR for each feature you want to support.

Each MR may consist on several commits, and it won't be squashed when merging into the main branch. However, during the review process, is it probable that the reviewer will ask to do some changes. We encourage to add those changes into _fixup_ commits so they can be squashed correctly and we can keep the main history branch clean.

<https://about.gitlab.com/blog/2019/02/07/start-using-git/>

If you prefer, you can _amend_ commits in a MR and force push to the MR branch.
