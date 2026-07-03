#include <math.h>

void rhs(double t, const double y[], double dydt[], const double params[])
{
    dydt[0] = y[1];
    dydt[1] = -1.0*params[1]*y[0]/params[0];
}
