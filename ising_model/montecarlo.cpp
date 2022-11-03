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
     // fast
    for (int i = 0; i < im.L; i++){
        for (int j = 0; j < im.L; j++){
            if (metropolis(im, i, j)){
                im.isingmatrix(i, j) = -im.isingmatrix(i, j);
            }
            else{
                continue;
            }
        }
    }
    
    /*// slow
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
    */
}

void MonteCarlo::solver(Isingmodel im, bool energyswitch, bool magnetizationswitch, bool matrixswitch){
    std::vector<double> energies;
    std::vector<double> magnetizations;
    energies.push_back(energy(im));  // Initial energy.
    magnetizations.push_back(magnetization(im));  // Initial magnetization.
    im.E = energies[0];
    im.M = magnetizations[0];
    
    // Prophylactic calculations.
    dE[-2] = exp(-1*(B*(-4)));
    dE[2] =  exp(-1*(B*(4)));
    dE[-4] = exp(-1*(B*(-8)));
    dE[4] = exp(-1*(B*(8)));

    for (int i = 0; i < steps; i++){
        energies.push_back(im.E);  // Saving energies.
        magnetizations.push_back(im.M); // Saving magnetization.
        mccycle(im);
        std::cout << i << std::endl;
    }
    
    if (energyswitch){
        writevaluestofile(im,energies, "datafiles/energies" + filename);
    }
    
    if (magnetizationswitch){
        writevaluestofile(im, magnetizations, "datafiles/magnetizations" + filename);
    }
    
    if (matrixswitch){
        writematrixtofile(im, "datafiles/matrix" + filename);
    }
}

// Returning magnetization.
double MonteCarlo::magnetization(Isingmodel im){
    double magnetization = arma::accu(im.isingmatrix);
    
    return magnetization;
}

// Returning energy.
double MonteCarlo::energy(Isingmodel im){
    double energy = arma::accu(im.isingmatrix % (arma::shift(im.isingmatrix, -1, 0) + arma::shift(im.isingmatrix, 1, 0) + arma::shift(im.isingmatrix, -1, 1) + arma::shift(im.isingmatrix, 1, 1)));
    return energy;
}


void MonteCarlo::writevaluestofile(Isingmodel im, std::vector<double> vector, std::string direc){
    // Writing to file with float values.
    std::ofstream fw(direc, std::ofstream::out);  // Setting the stream to output.
    if (fw.is_open())
    {
      fw << im.L*im.L<< "\n";
      fw << B << "\n";
      fw << T << "\n";
      for (int i = 0; i < vector.size(); i++) {
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

