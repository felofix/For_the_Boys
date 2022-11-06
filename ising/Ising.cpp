//
//  Ising.cpp
//  ising
//
//  Created by Felix Aarekol Forseth on 28/10/2022.
//

#include "Ising.hpp"

Isingmodel::Isingmodel(int Li){
    L = Li;
    boundary();
}

// Creating matrix.
void Isingmodel::initialize_model(){
    arma::arma_rng::set_seed_random(); // Initilizing randomness.
    isingmatrix = 2 * (arma::floor(2 * isingmatrix.randu(L,L))) - 1;
}

void Isingmodel::initilize_ordered(){
    isingmatrix = arma::mat(L, L, arma::fill::ones);
}

// Create boundary conditions
void Isingmodel::boundary(){
    for (int i = 0; i < L; i++){
        if (i < L){
            r.insert({i, i});
        }
    }
    r.insert({L, 0});
    r.insert({-1, L - 1});
}
