 
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
     0.00000  273.15   0.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00000  273.15   0.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00000  273.15 *******         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00000  558.65   0.010         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00000  273.15   0.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00980  273.19   0.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00000  273.15   0.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00000  273.15   0.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00000  273.15   0.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00000  273.15   0.000         0.000000         0.000000    0.00000000    0.00000000    0.00000000
     0.00000  273.15 *******         0.000000         0.000000    0.00000000    0.00000000    0.00000000
 ];
