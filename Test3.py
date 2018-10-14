import math as m
#this is directly from Evan's Design Excel
#Environmental req.
air_tempf = 100 #deg. Farenheight
air_pressure = 101325 #Pa

#Input Parameters
#General Plane
vehicle_weight_lbs = 15 #lbs
WoS = 2.5 #lbs/ft^2 (W/S)
flight_speed = 20 #m/s
fuselage_width = 0.5 #ft

#Wing
AR = 6
LE_sweep = 5 #degrees
taper = 0.6
dihedral = 5
#Twist Subsection
RcTP = 50 #%
Rcl = 4 #degrees
TcTP = 50 #%
Tcl = -4 #degrees

#Airfoil info
airfoil_cl = .65
max_cl = 1.6
alpha = 0
pmaxt = 25 #%
e = 0.9
M = 0.059 #custom calc at 0 altitude and 20 m/s

#Calculated Parameters
#Environment
air_tempc = (air_tempf-32) * (5/9) #conversion to Celcius
air_tempk = air_tempc + 273.15 #conversion to Kelvin
air_density = air_pressure/(287.05*air_tempk) #calculated air density from pressure and air temp

#General Plane
vehicle_weight_N = vehicle_weight_lbs*4.44822 #conversion to newtons
WoS_M = WoS*47.8803 #Conversion of the W/S to Metric (N/M^2)
S = vehicle_weight_lbs/WoS #ft^2
S_M = vehicle_weight_N/WoS_M #m^2

#For a Single Wing
So2 = S_M/2 #m^2 (S/2)
Cr = (2*So2)/(m.sqrt(AR*So2)*(1+taper)) #m
Ct = Cr*taper #m
bo2 = m.sqrt(AR*So2) #m
b = bo2*2 #m

#More General Plane
fuselage_width_M = fuselage_width*0.3048 #conversion to Meters
C_intersect_M = Cr-((fuselage_width_M/2)/bo2)*(Cr-Ct) #m
C_intersect_ft = C_intersect_M/0.3048 #conversion to ft
SexpoSref = (S - 0.5*(Cr+C_intersect_M)*(fuselage_width_M/2))/S #Sexp/Sref

#Airfoil info
required_Cl = (2*vehicle_weight_N)/(S*air_density*flight_speed**2) #Calculation of the required Cl
B = m.sqrt(1-M**2)
n = airfoil_cl/((2*m.pi)/B)
LE_Max_t = 0 #m.tan(LE_sweep*(180/m.pi))- 4/AR * (pmaxt*(1-taper)/(1+taper))
n_Max_Cl = max_cl/((2*m.pi)/B)

Cl_90p = airfoil_cl*.9 #90% of airfoil Cl
Cl_small = airfoil_cl/(1+airfoil_cl/(m.pi*e*AR*2))
Cl_big = (2*m.pi*AR*2)/(2+m.sqrt(4+((AR*2)**2 + B**2)/n**2 *(1+m.tan((LE_Max_t**2)/B**2))))*SexpoSref

Cl_90p_Max = max_cl*.9
Cl_small_Max = max_cl/(1+max_cl/(m.pi*e*AR*2))
Cl_big_Max = (2*m.pi*AR*2)/(2+m.sqrt(4+((AR*2)**2 + B**2)/n_Max_Cl**2 *(1+m.tan((LE_Max_t**2)/B**2))))*SexpoSref

Stall_90p = m.sqrt((2*vehicle_weight_N)/(air_density*S_M*Cl_90p_Max))
Stall_small = m.sqrt((2*vehicle_weight_N)/air_density*S_M*Cl_small_Max)
Stall_big = m.sqrt((2*vehicle_weight_N)/air_density*S_M*Cl_big_Max)

#modified area for cl
S_90p = (2*vehicle_weight_N)/(airfoil_cl*air_density*flight_speed**2)
S_small = (2*vehicle_weight_N)/(Cl_small*air_density*flight_speed**2)
S_big = (2*vehicle_weight_N)/(Cl_big*air_density*flight_speed**2)