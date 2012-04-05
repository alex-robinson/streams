 
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
     1.00000  288.15   1.013        -1.085005         5.863119    0.00000000    1.15781525    1.15781525
    33.92850  383.15  17.000       -34.057622       185.267789    6.69082381   39.28293593   45.97375975
    27.52370  383.15  17.000       -27.628447       150.294148    5.42777388   31.86736035   37.29513423
     6.40470  383.15  17.000        -6.429074        34.973091    1.26303009    7.41545909    8.67848918
    28.52370 1763.37  16.490       -17.535064       222.690004   38.40983773   13.76683490   52.17667263
     6.40470  383.15  16.490        -6.429074        35.017772    1.25015526    7.41545909    8.66561435
    34.92850 1547.54  16.490       -24.259455       262.147750   38.15009166   21.13970475   59.28979642
     1.00000  298.15  17.000         0.000000        53.139736    3.35417431  117.51297435  120.86714867
 ];
