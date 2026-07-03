#include <math.h>
#include "solver.h"

void rk4_step(double t, double dt, double y[], int n, const double params[])
{

    double k1[n], k2[n], k3[n], k4[n];
    double y_temp[n]; 

    // k1
    rhs(t, y, k1, params);

    for (int i = 0; i < n; i++) {
        k1[i] *= dt;
        y_temp[i] = y[i] + 0.5 * k1[i];
    }

    //k2
    rhs(t + 0.5 * dt, y_temp, k2, params);

    for (int i = 0; i < n; i++) {
        k2[i] *= dt;
        y_temp[i] = y[i] + 0.5 * k2[i];
    }

    //k3
    rhs(t + 0.5 * dt, y_temp, k3, params);

    for (int i = 0; i < n; i++) {
        k3[i] *= dt;
        y_temp[i] = y[i] + k3[i];
    }

    //k4
    rhs(t + dt, y_temp, k4, params);

    //combine
    for (int i = 0; i < n; i++) {
        k4[i] *= dt;
        y[i] += (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6;
    }


}
