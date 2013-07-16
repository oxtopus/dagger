Dagger
======

What is Dagger?
---------------

Collection of utilities to support a git-based workflow for tracking
interoperability between dependent projects.

### High-level goals

...

Principles
----------

0 - There exists a branch in every project that is designated to be
stable.  For our purposes, we'll call it the CI branch, although, in
practice it may have a different name (for example, "stable" or
"release").

1 - There exists a branch in every project that is designated to be the
development branch.  Typically, this will be "master".

2 - Project dependencies are well documented (explicitly by repository
url + tish) in a file that exists in the root of the project in
the CI branch.

3 - There is an inherently one-directional dependency graph across all
projects (no circular references).

  For example:

  - grokengine (trunk) depends on nupic
  - grok-api-server depends on grokengine
  - cluster-gateway depends on grok-api-server and grokengine

4 - Everything a project needs to test itself are tracked in the CI
branch.  Tests are invoked in a common way across all projects.  Each
project-specific testing scenario is comprehensive and sets up itself,
as well as its dependencies in isolation.

Project setup
-------------

### Dagger configuration

Every dagger project must have a dagger configuration consisting of a file at
the root of the project, resolvable from the CI branch.  The configuration
file should be easily identifiable (for example, `dagger.cfg`), and in a
format that is easily human-readable and human-editable.  At a minimum, the
configuration must identify the development branch and a validation command.

### Bootstrapping a dagger project

If no CI branch exists, one will be created as an oprhan commit
establishing an initial dagger configuration:

  ```
  git checkout --orphan CI
  git rm -rf .
  ```

  ... create dagger configuration ...


  ```
  git add dagger.cfg
  git commit
  ```

Initializing a project requires:

- Target repository (assumed to be .)
- Target CI branch (default: CI)
- List of dependencies (optional), each consisting of:
  - Repository URL
  - Initial revision
  - Stable branch

Dagger Process
--------------

There must be a single entry point for executing the dagger process for a
given project.  The dagger entry point is responsible for executing the
following steps and returning meaningful return codes non-zero in the event of
an error, or otherwise failed execution.

### Checkout CI branch and pull latest

    git fetch origin
    git checkout CI
    git merge origin/CI

### Merge development branch into CI branch

    git fetch origin
    git merge --no-ff origin/master

### Run tests

  At this point, CI branch is at the same state as master, and the
  documented dependencies are left untouched.  In setting up the test
  environment, the specific versions of the documented dependencies are
  used.

  Execute validation command.

  * If validation command passes (returns zero), push to remote CI branch:

    `git push origin CI`

  * If tests fail, update dependencies.

    Update dependencies file with results of `git rev-list -n 1 ...` and
    commit the change, ammending the previous commit.

    ```
    git add dependencies.txt
    git commit --amend
    ```

    Run validation command again with the updated dependencies.

  * If validation command passes, push to remote CI branch:

    `git push origin CI`

  * If validation command fails, raise an exception, notify the appropriate
  parties

### Additional validation

  Test against deployed versions for backward compatibility or
  additional regression testing.

Releases
--------

Release candidates are identified by traversing the CI branch and the
documented dependencies.  When a particular project is released, the
specific revision is tagged accordingly.