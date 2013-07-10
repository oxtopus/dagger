Dagger
======

What is Dagger?
---------------

Collection of utilities to support a git-based workflow for tracking
dependencies and interoperability between projects.

High-level goals
----------------

1. Generic set of command-line utilities to record tested combinations
of commits for a project and its dependencies
2. Apply principles described in this document into Continuous
Integration (CI) build and testing workflow

Principles
----------

0. There exists a branch in every project that is designated to be
stable.  For our purposes, we'll call it the CI branch, although, in
practice it may have a different name (for example, "stable",
"release", or even "master").

1. Project dependencies are well documented (explicitly by repository
url + commitish) in a file that exists in the root of the project in
the CI branch.

2. There is an inherently one-directional dependency graph across all
projects (no circular references).

For example:

  - grokengine (trunk) depends on nupic
  - grok-api-server depends on grokengine
  - cluster-gateway depends on grok-api-server and grokengine

3. Everything a project needs to test itself along with its
dependencies are tracked in the CI branch.  Tests are invoked in a
common way across all projects.  Each project-specific testing scenario
is comprehensive and sets up itself, as well as its dependencies.


Project setup
-------------

If no CI branch exists, one will be created as an oprhan commit
establishing depenciencies.

  `git checkout --orphan CI`
  `git rm -rf .`
  `git rev-list -n 1 ...`
  `git add dependencies.txt`
  `git commit --amend`

Process
-------

- Checkout CI branch and pull latest

  `git checkout CI`
  `git pull origin CI`

- Record commit

- Merge tracked branch (most-likely master) into CI branch

  `git fetch origin`
  `git merge --no-ff origin/master`

- Run tests

  At this point, CI branch is at the same state as master, and the
  documented dependencies are left untouched.  In setting up the test
  environment, the specific versions of the documented dependencies are
  used.

  * If tests pass, push to remote CI branch:

  `git push origin CI`

  * If tests fail, update dependencies.

  Update dependencies file with results of `git rev-list -n 1 ...` and
  commit the change, ammending the previous commit.

  `git add dependencies.txt`
  `git commit --amend`

  Build and test again with the updated dependencies.

  * If tests pass, push to remote CI branch:

  `git push origin CI`

  * If tests fail, raise an exception, notify the appropriate parties

- Additional validation

  Test against deployed versions for backward compatibility or
  additional regression testing.

Releases
--------

Release candidates are identified by traversing the CI branch and the
documented dependencies.  When a particular project is released, the
specific commit is tagged accordingly.
