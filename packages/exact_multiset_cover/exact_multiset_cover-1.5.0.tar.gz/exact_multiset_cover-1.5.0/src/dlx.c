#include "dlx.h"


/*
 * This program uses Donald Knuth's Algorithm X to find exact covers
 * of sets.  For details on Algorithm X please see either
 * <https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X>
 * or
 * <http://arxiv.org/pdf/cs/0011047v1>.
 *
 * Specifically, we use the Knuth/Hitotsumatsu/Noshita method of
 * Dancing Links for efficient backtracking.  Please see Knuth's
 * paper above for details.
 */


int search(list sparse_matrix, int k, int max, int *solution, list last_col, int last_row_num) {
    list col, row, next;
    int result = 0;
    int row_num;

    // Base cases:
    // 1. There are no columns left; we've found a solution.
    if (get_right(sparse_matrix) == sparse_matrix) return k;
    // 2. There's a column with only zeros. This branch of the search
    //    tree has no solutions and we need to backtrack.
    if (last_col != 0) {
        // current column is not completely covered
        col = last_col;
    }
    else {
        col = choose_column_with_min_data(sparse_matrix, max);
    }
    if (get_data(col)->counter == 0) return 0;

    // Main algorithm:
    for (row = col; (row = get_down(row)) != col; ) {
        row_num = get_data(row)->counter;
        if (row_num < last_row_num) {
            // already processed, skip it
            continue;
        }
        cover_column(col, row);
        solution[k] = row_num;
        for (next = row; (next = get_right(next)) != row; )
            cover_column(get_data(next)->list_data, next);
        if (get_data(col)->multiplicity == 0) {
            result = search(sparse_matrix, k+1, max, solution, 0, 0);
        }
        else {
            result = search(sparse_matrix, k+1, max, solution, col, row_num);
        }
        // If result > 0 we're done, but we should still clean up.
        for (next = row; (next = get_left(next)) != row; )
            uncover_column(get_data(next)->list_data, next);
        uncover_column(col, row);
        if (result > 0) break;
    }
    return result;
}

int count(list sparse_matrix, int k, int max, int *solution, list last_col, int last_row_num) {
    list col, row, next;
    int result = 0;
    int c = 0;
    int row_num;

    // Base cases:
    // 1. There are no columns left; we've found a solution.
    if (get_right(sparse_matrix) == sparse_matrix) return 1;
    // 2. There's a column with only zeros. This branch of the search
    //    tree has no solutions and we need to backtrack.
    if (last_col != 0) {
        // current column is not completely covered
        col = last_col;
    }
    else {
        col = choose_column_with_min_data(sparse_matrix, max);
    }
    if (get_data(col)->counter == 0) return 0;

    // Main algorithm:
    for (row = col; (row = get_down(row)) != col; ) {
        row_num = get_data(row)->counter;
        if (row_num < last_row_num) {
            // already processed, skip it
            continue;
        }
        cover_column(col, row);
        solution[k] = row_num;
        for (next = row; (next = get_right(next)) != row; )
            cover_column(get_data(next)->list_data, next);
        if (get_data(col)->multiplicity == 0) {
            result = count(sparse_matrix, k+1, max, solution, 0, 0);
        }
        else {
            result = count(sparse_matrix, k+1, max, solution, col, row_num);
        }
        c += result;
        // If result > 0 we're done, but we should still clean up.
        for (next = row; (next = get_left(next)) != row; )
            uncover_column(get_data(next)->list_data, next);
        uncover_column(col, row);
    }
    return c;
}

int dlx_get_exact_cover(int rows, int cols, char matrix[], char target[], int *solution) {
    list sparse_matrix;
    int solution_length;

    sparse_matrix = create_sparse(rows, cols, matrix, target);
    solution_length = search(sparse_matrix, 0, rows, solution, 0, 0);
    destroy_entire_grid(sparse_matrix);

    while (rows > solution_length) {
        solution[--rows] = 0;  // Zero out everything above position i.  Caller
                               // can use this to determine if there is a solution.
    };

    return solution_length;
}

int dlx_get_solution_count(int rows, int cols, char matrix[], char target[]) {
    list sparse_matrix;
    // int solution_length;
    int solution_count = 0;
    int *solution = malloc(rows * sizeof(*solution));

    sparse_matrix = create_sparse(rows, cols, matrix, target);
    solution_count = count(sparse_matrix, 0, rows, solution, 0, 0);
    destroy_entire_grid(sparse_matrix);

    free(solution);
    return solution_count;
}

int enumerate(list sparse_matrix, int k, int max, int *solution, int *solutions, int solution_size, list last_col, int last_row_num) {
    list col, row, next;
    int result = 0;
    int c = 0;
    int row_num;

    // Base cases:
    // 0. we have run out of space
    if (max < 1) {
        return 0;
    }
    // 1. There are no columns left; we've found a solution.
    if (get_right(sparse_matrix) == sparse_matrix) {
	for (int i=0; i < k; i++) {
            solutions[i] = solution[i];
	}
	for (int i=k; i < solution_size; i++) {
	    solutions[i] = 0;
	}
	return 1;
    }
    // 2. There's a column with only zeros. This branch of the search
    //    tree has no solutions and we need to backtrack.
    if (last_col != 0) {
        // current column is not completely covered
        col = last_col;
    }
    else {
        col = choose_column_with_min_data(sparse_matrix, solution_size);
    }
    if (get_data(col)->counter == 0) return 0;

    // Main algorithm:
    for (row = col; (row = get_down(row)) != col; ) {
        row_num = get_data(row)->counter;
        if (row_num < last_row_num) {
            // already processed, skip it
            continue;
        }
        cover_column(col, row);
        solution[k] = row_num;
        for (next = row; (next = get_right(next)) != row; )
            cover_column(get_data(next)->list_data, next);
        if (get_data(col)->multiplicity == 0) {
            result = enumerate(sparse_matrix, k+1, max - c, solution, solutions + c * solution_size, solution_size, 0, 0);
        }
        else {
            result = enumerate(sparse_matrix, k+1, max - c, solution, solutions + c * solution_size, solution_size, col, row_num);
        }
        c += result;
        for (next = row; (next = get_left(next)) != row; )
            uncover_column(get_data(next)->list_data, next);
        uncover_column(col, row);
    }
    return c;
}

int dlx_get_all_solutions(int rows, int cols, char matrix[], char target[], int max_count, int* solutions) {
    list sparse_matrix;
    int solution_count = 0;
    int *solution = malloc(rows * sizeof(*solution));

    sparse_matrix = create_sparse(rows, cols, matrix, target);

    int count = enumerate(sparse_matrix, 0, max_count, solution, solutions, rows, 0, 0);

    destroy_entire_grid(sparse_matrix);

    free(solution);
    return count;

}
