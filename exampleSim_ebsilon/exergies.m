 
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
     1.00000  288.15   1.013        -0.014516         6.826248    0.00000000    0.00282187    0.00282187
    35.00350  423.15  17.000         4.261041       224.174329    9.02461511    0.09877541    9.12339052
    28.39580  423.15  17.000         3.456673       181.856357    7.32101500    0.08012932    7.40114432
     6.60760  423.15  17.000         0.804355        42.317319    1.70357380    0.01864580    1.72221960
    29.39580 1757.59  16.490        -1.744627       247.002998   42.50635654    0.46365132   42.97000787
     6.60760  423.15  16.490         0.804355        42.375090    1.68692689    0.01864580    1.70557269
    36.00350 1547.54  16.490        -0.956381       294.201792   42.87471097    0.41548225   43.29019321
     1.00000  298.15  17.000        -4.667047        10.141161    0.42154328   51.53369718   51.95524046
 ];
