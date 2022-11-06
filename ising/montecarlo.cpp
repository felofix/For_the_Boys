//
//  montecarlo.cpp
//  ising
//
//  Created by Felix Aarekol Forseth on 28/10/2022.
//

#include "montecarlo.hpp"

// Declaration function.
MonteCarlo::MonteCarlo(int stepsi, double Ti, std::string f){
    steps = stepsi; // steps
    T = Ti/kb; // Temperature.
    B = 1/(kb*T); // Coldness.
    filename = f;
    srand (time(NULL));
    
    // Energy difference map.
    dE[0] =  0;
    dE[-2] = 0; // exp(-1*(B*(-4)));
    dE[2] =  0; // exp(-1*(B*(4)));
    dE[-4] = 0; // exp(-1*(B*(-8)));
    dE[4] =  0;  // exp(-1*(B*(8)));
}

double MonteCarlo::prob(Isingmodel &im, int i, int j){
    int de = im.isingmatrix(i, j)*(im.isingmatrix(i, im.r[j+1]) + im.isingmatrix(i, im.r[j-1]) + im.isingmatrix(im.r[i+1], j) + im.isingmatrix(im.r[i-1], j)); // sum
    im.deltaE = de;
    
    return dE[de];
}

bool MonteCarlo::metropolis(Isingmodel &im, int i, int j){
    double p = prob(im, i, j);
    double ran = rand()/(float)RAND_MAX;  // random Bournulli number.
    if (p >= ran){
        im.E += im.deltaE*2; // updating energy
        im.M -= im.isingmatrix(i, j)*2; // updating magnetization.
        return true;
    }
    else{
        return false;
    }
}

// A Monte Carlo cycle.
void MonteCarlo::mccycle(Isingmodel &im){
    // slow
    for (int i = 0; i < pow(im.L, 2); i++){
        int ii = rand() % im.L;
        int jj = rand() % im.L;
        
        if (metropolis(im, ii, jj)){
            im.isingmatrix(ii, jj) = -im.isingmatrix(ii, jj);
        }
        else{
            continue;
        }
    }
}

void MonteCarlo::solver(Isingmodel im, bool dataswitch, bool energiesswitch, bool magnetizationswitch){
    arma::vec energies(steps, arma::fill::zeros);
    arma::vec magnetizations(steps, arma::fill::zeros);
    energies(0) = energy(im);  // Initial energy.
    magnetizations(0) = magnetization(im);  // Initial magnetization.
    im.E = energies[0];
    im.M = magnetizations[0];
    
    // Prophylactic calculations.
    dE[-2] = exp(-1*(B*(-4)));
    dE[2] =  exp(-1*(B*(4)));
    dE[-4] = exp(-1*(B*(-8)));
    dE[4] = exp(-1*(B*(8)));

    for (int i = 1; i < steps; i++){
        energies(i) = (im.E);       // Saving energies.
        magnetizations(i) = (im.M); // Saving magnetization.
        mccycle(im);
    }
    
    if (dataswitch){
        arma::vec info(5, arma::fill::zeros);
        info(0) = mean_epsilon(energies, pow(im.L, 2));
        info(1) = mean_m(magnetizations, pow(im.L, 2));
        info(2) = hc(energies, pow(im.L,2));
        info(3) = sus(magnetizations, pow(im.L,2));
        info(4) = T*kb;
        writevaluestofile(info, "datafiles/info" + filename);
    }
    
    if (energiesswitch){
        writevaluestofile(energies, "datafiles/energies" + filename);
    }
    
    if (magnetizationswitch){
        writevaluestofile(magnetizations, "datafiles/magnetizations" + filename);
    }
}

// Returning magnetization.
double MonteCarlo::magnetization(Isingmodel im){
    double magnetization = abs(arma::accu(im.isingmatrix));
    return magnetization;
}

// Returning energy.
double MonteCarlo::energy(Isingmodel im){
    double energy = -J*(arma::accu(im.isingmatrix % (arma::shift(im.isingmatrix, -1, 0) + arma::shift(im.isingmatrix, -1, 1))));
    return energy;
}

// Mean epsilon
double MonteCarlo::mean_epsilon(arma::vec energies, int N){
    double mean_eps = arma::mean(energies)/N;
    return mean_eps;
}

// Mean epsilon
double MonteCarlo::mean_m(arma::vec magnetizations, int N){
    double mm = arma::mean(magnetizations)/N;
    return mm; 
}

// Heat cap
double MonteCarlo::hc(arma::vec energies, int N){
    double heatcap = (1/double(N))*(1/(kb*pow(T,2)))*arma::stddev(energies);
    return heatcap;
}

double MonteCarlo::sus(arma::vec magnetizations, int N){
    double s = (1/double(N))*(1/(kb*T))*arma::stddev(magnetizations);
    return s;
}

void MonteCarlo::writevaluestofile(arma::vec vector, std::string direc){
    // Writing to file with float values.
    std::ofstream fw(direc, std::fstream::app);  // Setting the stream to output.
    if (fw.is_open())
    {
      for (int i = 0; i < vector.n_elem; i++) {
          fw << vector[i] << "\n";
      }
      fw.close();
    }
    else std::cout << "The file couldnt be opened. " << std::endl;
}

void MonteCarlo::writematrixtofile(Isingmodel im, std::string direc){
    // Writing to file with float values.
    std::fstream fw;
    fw.open(direc, std::fstream::app);
    if (fw.is_open())
    {
      for (int i = 0; i < im.isingmatrix.n_rows; i++) {
          fw << im.isingmatrix.row(i) << "\n";
      }
      fw.close();
    }
    else std::cout << "The file couldnt be opened. " << std::endl;
}

