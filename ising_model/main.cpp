//
//  main.cpp
//  ising
//
//  Created by Felix Aarekol Forseth on 27/10/2022.
//


#include <iostream>
#include <armadillo>
#include "Ising.hpp"
#include "montecarlo.hpp"

int main(int argc, const char * argv[]) {
    // constants
    int L = 40;
    double T = 1;
    int steps = 10000;
    Isingmodel A(L);
    A.initialize_model();
    MonteCarlo M(steps, T, "T1.txt");
    M.solver(A, false, false, true);
}
