//
//  utilities.hpp
//  project2
//
//  Created by Felix Aarekol Forseth on 14/09/2022.
//

#ifndef utilities_hpp
#define utilities_hpp

#include <stdio.h>
#include <vector>
#include <armadillo>
#include <math.h>
using namespace arma;

arma::mat tridiagonal(double a, double b, double c, int N); // Creating a tridaigonal matrix.
arma::vec analeigenval(double a, double d, int N); // Creating analytical eigenvalues.
arma::vec analeigenvec(int N, int i); // Creating analytical eigenvectors.
bool checkequaleig(arma::vec A, arma::vec B, double error); // Checking if vectors are equal.
bool checkequalmatrix(arma::mat A, arma::mat B, double error); // Checking if vectors are equal.
double maxoffvalue(arma::mat A, int& k, int& l, int N); // Finding largest off-diagonal value. 

#endif /* utilities_hpp */
