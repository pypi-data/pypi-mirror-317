#ifndef _DLX_H_
#define _DLX_H_

#include "quad_linked_list.h"
#include "sparse_matrix.h"

int search(list, int, int, int *, list, int);
int dlx_get_exact_cover(int, int, char [], char [], int*);
int dlx_get_solution_count(int, int, char [], char []);
int dlx_get_all_solutions(int, int, char [], char [], int, int*);

#endif
