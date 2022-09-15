//
//  main.cpp
//  project2
//
//  Created by Felix Aarekol Forseth on 14/09/2022.
//

#include <iostream>
#include "utilities.hpp"

int main(int argc, const char * argv[]){
    
    /* // Task 2.
    // Stupid constants.
    double n = 10;
    double h = 1/n;
    double a = -1/pow(h, 2);
    double d = 2/pow(h, 2);
    int N = 6;
    double error = 0.002;
    
    // Armadillo eigenvalues and eigenvectors.
    arma::vec eigval;
    arma::mat eigvec;
    arma::mat A = tridiagonal(a, d, a, N);
    arma::eig_sym(eigval, eigvec, A);
    
    // Analytical eigenvalues and eigenvectors.
    // checking if they have similar eigenvalues.
    arma::vec aeigvalues = analeigenval(a, d, N);
    bool sameval = checkequaleig(eigval, aeigvalues, error);
    
    // checking if they have similar eigenvectors.
    bool samevec = true;
    for (int i = 0; i < N; i++){
        arma::vec eigenvectors = analeigenvec(N, i + 1);
        if (samevec == false){
            std::cout << "They are not similar." << std::endl;
        }
        samevec = checkequaleig(abs(arma::normalise(eigenvectors)), abs(arma::normalise(eigvec.col(i))), error);
    }
    if (samevec == true and sameval == true){
        std::cout << "Armadillo and analytical are equal and good friends." << std::endl;
    }
    */
    
    /* Problem 3.
    int N = 4;
    int k = 0;
    int l = 0;
    arma::mat A(N, N, fill::zeros);
    A(0, 0) = A(1, 1) = A(2, 2) = A(3, 3) = 1;
    A(3, 0) = A(0, 3) = 0.5;
    A(2, 3) = A(3, 2) = -0.7;
    double maxval = maxoffvalue(A, k, l, N);
    std::cout << maxval << " " << k << " " << l << std::endl;
    */
    
    
    return 0;
}
