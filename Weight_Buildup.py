#Vehicle Weight Buildup
import Test3 as t3
import pandas as pd

foil_points = pd.read_csv('PSU_90097.txt', delim_whitespace=True)

#defined densities for materials
fiberglass_d = 0 #some density without resin
kevlar_d = 0
carbon_fiber_d = 0
resin_d = 0 #some density of the resin
fast_hardener_d = 0
slow_hardener_d = 0
aluminum_d = 0 #assume t6-6061
wheel_d = 0 #some general assumed density for rc wheels
motor_d = 0 #some general motor density
electronics_d = 0 #some general density of the onboard avionics
wire_d = 0  #some general density of wire length
foam_d = 0 #some general density of the core foam
balsa_d = 0 #some general density of the balsa structure

#Construction
hardner_mix = .5 #hardner mixture ratio
resin_mix = 100/33 #resin to hardner mixture ratio
composite_mix = 1/1 #ratio of the weights of resin to composite
wing_layer_thickness = .05 #in
wing_layer_density = 0#2*(surface_area*wing_layer_thickness*composite)

#Construction Outputs
resin_weight = (wing_layer_density/2)

#Constraints
payload_m = 2 #payload mass (lbs)

def main():
    #for surface area do a linear approximation of the distance formula from point to point
    #Idea - take the point data, and using a method of parallelopipeds and triangles (for the leading and trailing edges) find the area
    #then multiply that with span
    #multiply that with the foam density
    #add that time the surface area * wing_layer_thickness* wing_layer_density
    print(foil_points.iat[0,0])
    print(foil_points)
if __name__ == '__main__':
    main()