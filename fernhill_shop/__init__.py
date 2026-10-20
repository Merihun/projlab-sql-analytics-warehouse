"""The Fernhill shop database export and a small runner for your SQL files.

Everything here is synthetic and generated from a fixed seed, so every learner gets the same data and the
row counts in the project's steps match. You do not need to change this package.

    python -m fernhill_shop load                    create fernhill.db with the six raw tables
    python -m fernhill_shop run FILE [FILE ...]     run SQL files; prints the last result
    python -m fernhill_shop query "SELECT ..."      run one statement
    python -m fernhill_shop build                   load, then run profiling/ and models/ in order
"""
