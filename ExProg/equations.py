
# T: temperature in K, p: pressure in bar, h: enthalpy in kJ/kmol, s: entropy in kJ/kmolK, cp: specific heat in kJ/kmolK, x: molar percentage in -, 
# mdot: mass flow in kg/s, MW: molecular weight in gr, v: volume, e: specific exergy in kJ/kmol and kJ/kg, E: absolute exergy in kW/MW
# H_, a, b, c, d, y: constants used in the calculation of enthalpies, R: ideal gas constant= 8.314 kJ/kmolK
# el: element in stream, str: stream, ch: chemical, ph: physical, tot: total
# 0: Reference point
# x_H2O_new(g), x_H2O(l)

T0, p0, h0_T, s_Tp_0, cp0_T, R 	 																			
T, p, mdot, h_T, s_Tp, cp_T, x_el, h_T_el, s_Tp_el, s0_el, h0_el	
				
MW_str, e_ph_str, e_ph_str_kg, e_ch_str, e_ch_str_kg, mdot_str, h_T_str, s_Tp_str, 
s0_str, h0_str, cp_str, E_ph_str, E_ch_str, v_str 									# Variables for mixtures/streams (str)

e_ph, e_ch, e_tot, E_ph, E_ch, E_tot												# tot: total (ph+ch)
H_el, a_el, b_el, c_el, d_el, y_el													# Constants used in the calculation of enthalpies


##### Calculations of enthalpies h (depends only on T, because we assume ideal gases)
y_el = T_stream/1000
 
h_T_el = 10^3 * (H_el + a_el*y_el + b_el/2 * y_el^2 - c_el*y_el^(-1) + d_el/3 * y_el^3)

# If H_el etc not known for the element, then 
h_T_el = ( (cp0_el) * (T_str-T0) ) + h_T0_el                                        # NO change in cp

##### Calculations of entropies (depend both on T and p)
s_Tp_el = ( s_el + a_el*ln(T) + b_el*y_el - c_el/2 * y_el^(-2) + d_el/2 * y_el^2) ) - R * ln (p_str/p0)

# If H_el etc not known for the element, then 
s_Tp_el = (  (cp_T0_el / T_str ) * (T_str-T0) - R * ln(p_str/p0) ) + s_Tp0_el

###### Calculations of specific heats (depend on T)
cp_T_el = ( a_el + b_el * y_el + c_el * y_el**(-2) + d_el * y_el**(2) )

# If a_el etc not known for the element, then use cp_0
cp_T_el = cp_T0_el 
																
## NOW STREAM CALCULATIONS ##

CASE 1: % H2O < 1.0																	# It means it is flue gas, air or other streams	(gases/liquids or solids)													
#--------- The following apply for all stream types except water/steam -------------#
#!!!! CHECK IF IT IS flue gas & calculate % of liquid water for calculating h_0
# At 25C the pressure would be 0.0317bar
# x_H2O_new(g) = ( 0.0317 * ( 1- x_H2O ) ) / (1 - 0.0317)								# % mol
# x_H2O(l) = x_H2O(l) + (x_H2O - x_H2O_new(g))


h_T_str  = SUM all (h_T_el * x_el)													# Enthalpy at T for mixture 
h_T0_str = SUM all (h_T0_el * x_el)													# Enthalpy at T_0 for mixture

s_Tp_str  = SUM all (s_Tp_el * x_el) 												# Entropy at T for mixture
s_Tp0_str = SUM all (s_Tp0_el * x_el)												# Entropy at T_0 for mixture
#-----------------------------------------------------------------------------------#

CASE 2: % H2O = 1.0
#------------------ The following apply for water/steam streams --------------------#
#!!!! CHECK IF WE HAVE SATURATED WATER OR STEAM  !!!!!
# If yes, then h_T_str should be taken from the IAPWS IF97 steam tables for saturated streams
# If not, do the following
h_T_str  = ( (cp_T_el - cp_T0_el) * (T_str-T0) ) + h_T0_el							# here el: H2O
s_Tp_str = ( (cp_T_el - cp_T0_el) * ln(T_str/T0) + s_Tp0_el
#-----------------------------------------------------------------------------------#

## DONE CASES

	
##### Calculations of exergies
# Physical specific exergy of stream str  ###
e_ph_str = (h_T_str - h_T0_str - T0 * (s_Tp_str - s0_str))				# kJ/kmol
e_ph_str_kg = e_ph_el * MW_str											# kJ/kg

# Absolute physical exergy for mixture in MW
E_ph_str = e_ph_str_kg * mdot_str /1000							


# Chemical specific exergy of element el ###
e_ch_str = SUM(e_ch_el * x_el) + R * T_0 * SUM(x_el * ln (x_el))		# kJ/kmol
e_ch_str_kg = e_ch_el * MW_str											# kJ/kg

# Absolute chemical exergy for mixture in MW
E_ch_str = e_ch_str_kg * mdot_str /1000

# Total Exergy
# Specific
e_tot_str_kg = e_ph_str_kg + e_ch_str_kg
# Absolute
E_tot_str = E_ph_str + E_ch_str
E_tot_str2 = e_tot_str_kg * mdot_str
# CHECK if E_tot_str = E_tot_str2