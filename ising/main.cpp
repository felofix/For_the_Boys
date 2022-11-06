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
    // Constants
    double T1 = 1;
    double T24 = 2.4;
    int steps = 2000000;
    
    
    /*// 2x2 simulation.
    int L2 = 2;
    Isingmodel I1(L2);
    I1.initialize_model();
    MonteCarlo M1(steps, T1, "T1.txt");
    M1.solver(I1, true, true, true);
    */
    
    /*// 20x20 simulation, shorter sim to illustrate burn-in-time.
    int L2 = 20;
    int steps20x = 200000;
    
    // unordered.
    Isingmodel I2T1U(L2);   // 20x20, unordered, T1
    Isingmodel I2T24U(L2);   // 20x20, unordered, T24
    I2T1U.initialize_model();
    I2T24U.initialize_model();
    MonteCarlo MT1U(steps20x, T1, "20x20_T1_UOrdered.txt");
    MonteCarlo MI2T24U(steps20x, T24, "20x20_T24_UOrdered.txt");
    MT1U.solver(I2T1U, false, true, true);
    MI2T24U.solver(I2T24U, false, true, true);
     
    // ordered.
    Isingmodel I2T1O(L2);   // 20x20, unordered, T1
    Isingmodel I2T24O(L2);   // 20x20, unordered, T24
    I2T1O.initilize_ordered();
    I2T24O.initilize_ordered();
    MonteCarlo MT1O(steps20x, T1, "20x20_T1_Ordered.txt");
    MonteCarlo MI2T24O(steps20x, T24, "20x20_T24_Ordered.txt");
    MT1O.solver(I2T1O, false, true, true);
    MI2T24O.solver(I2T24O, false, true, true);
    */
    
    /*// 20x20 simulation, estimate energy functions.
    int L2 = 20;
    int steps20x = 2000000;
    Isingmodel I4T1(L2);   // 20x20, unordered, T1
    Isingmodel I4T24(L2);   // 20x20, unordered, T24
    I4T1.initialize_model();
    I4T24.initialize_model();
    MonteCarlo M4T1(steps20x, T1, "20x20_T1.txt");
    MonteCarlo M4T24(steps20x, T24, "20x20_T24.txt");
    M4T1.solver(I4T1, false, true, false);
    M4T24.solver(I4T24, false, true, false);
    */
    
    //#pragma omp parallel for
    std::vector<int> Ls = {40, 60, 80, 100};
    arma::vec Ts = arma::linspace(2.1, 2.4, 50);
    int L2 = 100;
    
    for (int j = 0; j < Ts.n_elem/5; j++){
        std::cout << j << std::endl;
        #pragma omp parallel for
        for (int i = j*5; i < j*5+5; i++){
            Isingmodel I(L2);
            I.initialize_model();
            MonteCarlo M(2000000, Ts(i), std::to_string(L2) + ".txt");
            M.solver(I, true, false, false);
        }
    }
}
