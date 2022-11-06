//
//  montecarlo.hpp
//  ising
//
//  Created by Felix Aarekol Forseth on 28/10/2022.
//

#ifndef montecarlo_hpp
#define montecarlo_hpp

#include <stdio.h>
#include <map>
#include <armadillo>
#include "Ising.hpp"
#include <stdlib.h>     /* srand, rand */
#include <vector>
#include <time.h>       /* time */

class MonteCarlo{
public:
    int steps; // Steps of MC.
    double T; // Temperature.
    std::string filename; // filename.
    double kb = 1.3806505e-23; // Boltzmann constant.
    double B; // Coldness.
    double J = 1; 
    
    // Declaration function.
    MonteCarlo(int steps, double T, std::string filename);
    
    // Map.
    std::map<int, double> dE;
    
    // Find dE from matrix and return probability.
    double prob(Isingmodel &im, int i, int j);
    
    // Metropolis step.
    bool metropolis(Isingmodel &im,  int i, int j);
    
    // A Monte Carlo cycle. 
    void mccycle(Isingmodel &im);
    
    // Solving montecarlo with given steps. 
    void solver(Isingmodel im, bool dataswitch , bool energiesswitch, bool magnetizationswitch);
    
    // Returning energy.
    double energy(Isingmodel im);
    
    // Returning magnetization.
    double magnetization(Isingmodel im);
    
    // Mean epsilon
    double mean_epsilon(arma::vec energies, int N);
    
    // Mean epsilon
    double mean_m(arma::vec magnetizations, int N);
    
    // Heat cap
    double hc(arma::vec energies, int N);
    
    double sus(arma::vec energies, int N);
    
    // Writing vector values to file.
    void writevaluestofile(arma::vec vector, std::string direc);
    
    // Write to file.
    void writematrixtofile(Isingmodel im, std::string direc);
};

#endif /* montecarlo_hpp */

