//
//  main.cpp
//  Prosjekt_1
//
//  Created by Felix Aarekol Forseth on 24/08/2022.
//

#include <iostream>
#include <vector>
#include "utilities.hpp"

int main(int argc, const char * argv[]) {
    string direc = "/Users/Felix/desktop/poisson.txt";
    vector<double> vec = linspace(0, 1, 100);
    vector<double> ux  = poissonvec(vec);
    writetofile(vec, ux, direc, 3);
}


