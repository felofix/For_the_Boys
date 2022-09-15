//
//  utilities.cpp
//  Prosjekt_1
//
//  Created by Felix Aarekol Forseth on 24/08/2022.
//

#include "utilities.hpp"

vector<double> poissonvec(vector<double> xvalues){
    
    vector<double> ux(xvalues.size(), 0);
    for (int i = 0; i < xvalues.size(); i ++){
        ux[i] = u(xvalues[i]);
    }
    return ux;
}

double u(double x){ 
    x = 1 - (1 - exp(-10))*x - exp(-10*x);
    return x; 
}

vector<double> linspace(double s, double e, int n){ // creates a linspace.
    vector<double> linspace;
    double T = (e - s)/(n-1);
    
    for (int i = 0; i < n; i++){
        linspace.push_back(s + T*i);
    }
    return linspace;
}

void writetofile(vector<double> xvalues, vector<double> ux, string direc, int decimals){
    ofstream fw(direc, std::ofstream::out);
    if (fw.is_open())
    {
      //store array contents to text file
      for (int i = 0; i < xvalues.size(); i++) {
        fw << setprecision(decimals+1) << xvalues[i] << " " << ux[i]  << "\n";         // setprecision isnt accurate for over 1*10 because it sets number of digits, not decimals.
      }
      fw.close();
    }
    else cout << "The file couldnt be opened. ";
}
