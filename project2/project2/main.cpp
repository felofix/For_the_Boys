//
//  main.cpp
//  project2
//
//  Created by Felix Aarekol Forseth on 14/09/2022.
//

#include <iostream>
#include "utilities.hpp"

int main(int argc, const char * argv[]){
    /*
    // Problem 2.
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
    arma::vec aeigvalues = analeigenval(a, d, N);
    arma::mat aeigvectors(N, N, fill::zeros);
    for (int i = 0; i < N; i++){
        aeigvectors.col(i) = analeigenvec(N, i + 1);
    }
    
    // Checking if they have similar eigenvalues and eigenvectors.
    bool sameval = checkequaleig(eigval, aeigvalues, error);
    bool samevec = checkequalmatrix(abs(arma::normalise(eigvec)), abs(arma::normalise(aeigvectors)), error);
    if (samevec == true and sameval == true){
        std::cout << "Armadillo and analytical are equal and good friends." << std::endl;
    }
    */
    
    
    /*// Problem 3.
    int N = 4;
    int k = 0;
    int l = 0;
    arma::mat A(N, N, fill::zeros);
    arma::mat R(N, N, fill::zeros);
    A(0, 0) = A(1, 1) = A(2, 2) = A(3, 3) = 1;
    A(3, 0) = A(0, 3) = 0.5;
    A(1, 2) = A(2, 1) = -0.7;
    double maxval = maxoffvalue(A, k, l, N);
    std::cout << maxval << " " << k << " " << l << std::endl;
    */
    
    
    /* // Problem 4.
    double n = 10;
    double h = 1/n;
    double a = -1/pow(h, 2);
    double d = 2/pow(h, 2);
    double error = 0.002;
    
    int N = 6;
    double eps = 0.01;
    arma::vec eigenvalues(N, fill::zeros);
    arma::mat eigenvectors(N, N, fill::zeros);
    arma::mat A = tridiagonal(a, d, a, N);
    arma::vec eigval;
    arma::mat eigvec;
    arma::eig_sym(eigval, eigvec, A);
    int maxiter = 10e3;
    int iterations = 0;
    bool converged = true;
    
    jacobi_eigensolver(A, eps, eigenvalues, eigenvectors, maxiter, iterations, converged, N);
    
    
    // Checking if similar.
    arma::uvec sort = arma::sort_index(eigenvalues, "ascend");
    bool sameval = true;
    bool samevec = true;
    
    for (int i = 0; i < N; i ++){
        if (sameval == false && samevec == false){
            std::cout << "They were not similar :(" << std::endl;
        }
        if (eigenvalues(sort(i)) == eigval(i)){
            sameval = true;
        }
        else{
            sameval = false;
        }
        samevec = checkequaleig(eigenvectors.col(sort(i)), eigvec.col(i), error);
    }
    if (sameval == samevec == true){
        std::cout << "Jacobi and analytical are equal and good friends." << std::endl;
    }
    */
    
    return 0;
}
