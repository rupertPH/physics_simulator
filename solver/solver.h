#ifndef SOLVER_H
#define SOLVER_H

void rhs(double t,
         const double y[],
         double dydt[],
         const double params[]);

#endif