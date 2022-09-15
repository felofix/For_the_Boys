//
//  utilities.cpp
//  project2
//
//  Created by Felix Aarekol Forseth on 14/09/2022.
//

#include "utilities.hpp"

arma::mat tridiagonal(double a, double b, double c, int N){
    arma::mat A = arma::mat(N, N).fill(0.);
    
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            if (i == j){
                A(i,j) = b;
            }
            if (i == j + 1){
                A(i, j) = c;
            }
            if (j == i + 1){
                A(i, j) = a;
            }
        }
    }
    return A;
}

arma::vec analeigenval(double a, double d, int N){
    arma::vec eigvalues(N, fill::zeros);
    
    for (int i = 0; i < N; i++){
        eigvalues(i) = d + 2*a*cos((i+1)*M_PI/(N + 1));
    }
    return eigvalues;
}

arma::vec analeigenvec(int N, int i){
    arma::vec eigvectors(N, fill::zeros);
    
    for (int j = 0; j < N; j++){
        eigvectors(j) = sin((j+1)*i*M_PI/(N + 1));
    }
    return eigvectors;
}


double maxoffvalue(arma::mat A, int& k, int& l, int N){
    double maxval = 0;
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            if (j != i and abs(A(i, j)) > 0){
                maxval = A(i, j);
                k = i;
                l = j;
            }
        }
    }
    return maxval;
}

bool checkequaleig(arma::vec A, arma::vec B, double error){
    
    if (arma::size(A) != arma::size(B)){    // checking if equal length.
        std::cout << "These vectors are not of equal length!" << std::endl;
    }
    
    bool same = arma::approx_equal(A, B, "absdiff", error);
    return same;
}

bool checkequalmatrix(arma::mat A, arma::mat B, double error){ // Checking if vectors are equal.
    if (arma::size(A) != arma::size(B)){    // checking if equal length.
        std::cout << "These vectors are not of equal length!" << std::endl;
    }
    
    bool same = arma::approx_equal(A, B, "absdiff", error);
    return same;
}

