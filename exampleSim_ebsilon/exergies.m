 
 %***************************************************
 %*                                                 *
 %*                   EBSTEX 2002                   *
 %*                                                 *
 %*      Uses IAPWS-IF97 for the properties of      *
 %*                 water and steam.                *
 %*                                                 *
 %*                  Frank Cziesla                  *
 %*                 October 21, 2002                *
 %*            f.cziesla@iet.tu-berlin.de           *
 %*              modifiziert für Ebsilon            *
 %*                  von Lea Boche                  *
 %*                                                 *
 %*              FOR INTERNAL USE ONLY!             *
 %*                                                 *
 %*         Technische Universitaet Berlin          *
 %*          Institut fuer Energietechnik           *
 %*           Marchstr. 18, 10587 Berlin            *
 %*                                                 *
 %* Ref.: W. Eisermann, W. Hasberg, G. Tsatsaronis  *
 %*       "THESIS-Ein Rechenprogramm zur Simulation *
 %*        und Entwicklung von Energieumwandlungs-  *
 %*        anlagen", Brennst.-Waerme-Kraft, 36,1/2, *
 %*        1984, pp. 45-51.                         *
 %*                                                 *
 %***************************************************
 
 % Nur zum Gebrauch am Institut fuer Energietechnik
 % der Technischen Universitaet Berlin.
 
 % Version: August 24, 2007
 
 % m [kg/s], T [K], p[bar], H [MW], S [kW/K],
 % EPH [MW], ECH [MW], E [MW]
 
 E = [
    10.00000  523.15  50.000       -33.953818        93.688300    0.00000000  421.80982775  421.80982775
     0.50000  523.15  50.000        -1.065834         1.870217    0.00000000    6.90542402    6.90542402
     0.50000  523.15  50.000        -0.183827         2.836819    0.00000000   11.50210563   11.50210563
     8.00000  523.15  50.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.40000  523.15  50.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.20000  523.15  50.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
 ];
