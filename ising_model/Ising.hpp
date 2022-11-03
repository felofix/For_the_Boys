//
//  Ising.hpp
//  ising
//
//  Created by Felix Aarekol Forseth on 28/10/2022.
//

#ifndef Ising_hpp
#define Ising_hpp

#include <stdio.h>
#include <armadillo>
#include <vector>

class Isingmodel{
public:
    int L; // Size of ising model.
    double E; // Energy
    double M; // magnetization
    double deltaE = 0; // Change of energy.
    double deltaM = 0; // Change of magnetization.
    arma::mat isingmatrix; // Matrix containing spins.
    std::map<int, int> r;
    
    // Declaration function.
    Isingmodel(int L);
    
    // Creating matrix.
    void initialize_model();
    
    void boundary();
    
};

#endif /* Ising_hpp */
