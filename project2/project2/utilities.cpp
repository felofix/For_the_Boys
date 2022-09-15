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


double maxoffvalue(const arma::mat& A, int& k, int& l, int N){
    double maxval = 0;
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            if (j != i && abs(A(i, j)) > maxval){
                maxval = abs(A(i, j));
                l = i;
                k = j;
            }
        }
    }
    return abs(maxval);
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
        std::cout << "These matrixes are not of equal size!" << std::endl;
    }
    bool same = arma::approx_equal(A, B, "absdiff", error);
    return same;
}

void jacobi_eigensolver(arma::mat& A, double eps, arma::vec& eigenvalues, arma::mat& eigenvectors,
                        const int maxiter, int& iterations, bool& converged, int N){
    int k, l;
    double maximoff = maxoffvalue(A, k, l, N);
    arma::mat R(N, N, fill::eye);
    
    while (maximoff > eps && iterations < maxiter){
        maximoff = maxoffvalue(A, k, l, N);
        jacobi_rotate(A, R, k, l, N);
        iterations++;
    }
    
    for (int i = 0; i < N; i++){
        eigenvalues(i) = A(i,i);
        eigenvectors.col(i) = R.col(i);
    }
}

double jacobi_rotate(arma::mat& A, arma::mat& R, int& k, int& l, int N){
    double t, c, s;
    arma::mat S(N, N, fill::eye);
    if (A(k, l) != 0.0){
        double tau = (A(l,l) - A(k,k))/(2*A(k,l));
        if (tau > 0 ) {
            t = 1.0/(tau + sqrt(1.0 + tau*tau));
        }
        else {
            t = -1.0/( -tau + sqrt(1.0 + tau*tau));
        }
        c = 1/sqrt(1 + t*t);
        s = c*t;
    }
    else{
        c = 1.0;
        s = 0.0;
    }
    
    // Redefining our S.
    S(l,l) = S(k,k) = c;
    S(k,l) = s;
    S(l,k) = -s;
    A = trans(S)*A*S;
    R = R*S;
    
    return t;
}
