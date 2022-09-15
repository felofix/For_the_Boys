//
//  utilities.hpp
//  Prosjekt_1
//
//  Created by Felix Aarekol Forseth on 24/08/2022.
//

#ifndef utilities_hpp
#define utilities_hpp

#include <stdio.h>
#include <vector>
#include <cmath>
#include <iostream>
#include <string>
#include <fstream>
#include <iomanip> 

using namespace std;

#endif /* utilities_hpp */

vector<double> poissonvec(vector<double> xvalues); // Solves the poisson for all x.
double u(double x);  // Solves for the u.
vector<double> linspace(double s, double e, int n); // bootleg linspace in c++.
void writetofile(vector<double> xvalues, vector<double> ux, string direc, int decimals); // writing to a file
