#ifndef RK4_H
#define RK4_H

void rk4_step(
    double t,
    double dt,
    double y[],
    int n,
    const double params[]
);

#endif