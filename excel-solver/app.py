import solver

solver.solve(
    problem_type="max",
    objective_function=[16, 20.5, 14],
    constraints_left=[
        [4, 6, 2],
        [3, 8, 6],
        [9, 6, 4],
        [30, 40, 25],
    ],
    constraints_right=[
        2000,
        2000,
        1440,
        9600,
    ],
    constraints_signs=[
        "<=",
        "<=",
        "<=",
        "<=",
    ],
)
