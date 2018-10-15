#Vehicle Weight Buildup
import Test3 as t3
import pandas as pd
import math as m
from matplotlib import pyplot as plt

foil_points = pd.read_csv('PSU_90097.txt', delim_whitespace=True)

#defined densities for materials
thickness = .0025 #arbitrary thickness in yards
fiberglass_145oz_d = (1.45*28.3495/thickness)/764555 #g/cm^3 ,1.45 oz/y^2
fiberglass_35oz_d = (3.5*28.3495/thickness)/764555 #g/cm^3 ,3.5 oz/y^2
kevlar_d = 0
carbon_fiber_8oz_d = (8*28.3495/thickness)/764555 #g/cm^3 ,8 oz/y^2
resin_d = 1.16 #g/cm^3
fast_hardener_d = 1.04 #g/cm^3
slow_hardener_d = 0.95 #g/cm^3
glass_bubbles_d = 0.875295868/(thickness*91.44) #g/cm^3 (use it for the surface of the foam
aluminum_d = 0 #assume t6-6061
wheel_d = 0 #some general assumed density for rc wheels
motor_d = 0 #some general motor density
electronics_d = 0 #some general density of the onboard avionics
wire_d = 0  #some general density of wire length
foam_d = 0.01356651 #g/cm^3 some general density of the core foam
balsa_d = 0 #some general density of the balsa structure

#Construction
hardner_mix = .5 #hardner mixture ratio between the two hardeners
resin_mix = 100 #resin to hardner mixture ratio
hardner_to_resin_mix = 33
composite_mix = 1/1 #ratio of the weights of resin to composite
wing_num_layer_5_oz = 2 #per side
wing_num_layer_145_oz = 1 #per side
carbon_spar_width = 1 #in


#Constraints
payload_m = 2 #payload mass (lbs)

def main():
    working_points_old = []
    #for surface area do a linear approximation of the distance formula from point to point
    #Idea - take the point data, and using a method of parallelopipeds and triangles (for the leading and trailing edges) find the area
    num_points = 64 #this is the number of points in the point sheet
    i = num_points
    foil_perimeter = 0
    foil_area = 0
    #perimeter calc
    while i>0:
        if i>1:
            foil_perimeter = foil_perimeter + m.sqrt((foil_points.iat[(i-1),1]-foil_points.iat[i,1])**2 + (foil_points.iat[(i-1),0]-foil_points.iat[i,0])**2)
        else:
            foil_perimeter = foil_perimeter + m.sqrt((foil_points.iat[(i+num_points-1), 1] - foil_points.iat[i, 1]) ** 2 + (foil_points.iat[i+num_points-1, 0] - foil_points.iat[i, 0]) ** 2)
        i=i-1
    #area calc
    i = num_points  #reset
    #initial Triangle
    foil_area = abs(foil_points.iat[i,0]*(foil_points.iat[i-1,1]-foil_points.iat[num_points-i,1]) + foil_points.iat[i-1,0]*(foil_points.iat[num_points-i,1]-foil_points.iat[i,1])+foil_points.iat[num_points-i,0]*(foil_points.iat[i,1]-foil_points.iat[i-1,1]))
    #used the first 2 points and the last point
    i=i-2   #new starting place
    num_polygons = (i-2)/4  #number of polygons being used for the rest of the area
    working_points = [[0,0],[0,0],[0,0],[0,0]] #storage of points being currently used
    c = 0 #counter for working points
    while num_polygons>0:
        while c<4:
            if c<2:
                working_points[c][0] = foil_points.iat[i,0]
                working_points[c][1] = foil_points.iat[i,1]
                i = i - 1
            else:
                if c == 2:
                    i = i + 2
                working_points[c][0] = foil_points.iat[num_points-i, 0]
                working_points[c][1] = foil_points.iat[num_points-i, 1]
                i = i + 1
                if c == 3:
                    i = i-2
            c = c + 1
        c = 0
        foil_points.plot(x='Xpos', y='Ypos')
        plt.scatter(working_points[0][0],working_points[0][1])
        plt.scatter(working_points[1][0],working_points[1][1])
        plt.scatter(working_points[2][0],working_points[2][1])
        plt.scatter(working_points[3][0],working_points[3][1])
        #plt.show()
        #input("Press Enter to continue...")
        #print(working_points)
        val_0 = max(working_points)
        val_1 = min(working_points)
        val_2 = max(working_points, key=lambda x: x[1])
        val_3 = min(working_points, key=lambda x: x[1])
        foil_area = foil_area + (abs((val_0[0]-val_1[0]))*abs((val_2[1]-val_3[1]))) # add the area of the large rectangle that encompasses the polygon
        k = 0
        while k < 4:
            if k < 3:
                foil_area = foil_area - abs(((working_points[(k+1)][0] - working_points[k][0])*(working_points[(k+1)][1]-working_points[k][1]))/2) #now subtract the triangles aroung the polygon
            else:
                foil_area = foil_area - abs(((working_points[(k-3)][0] - working_points[k][0]) * (working_points[(k-3)][1] - working_points[k][1])) / 4)  # now subtract the triangles aroung the polygon
            k = k + 1
        #print(working_points)
        i = i - 2
        num_polygons = num_polygons - 1
    #then Scale the perimeter and the Area to the Chord
    tip_perimeter = foil_perimeter * t3.Ct
    root_perimeter = foil_perimeter * t3.Cr
    tip_area = foil_area * t3.Ct**2 #to m^2
    root_area = foil_area * t3.Cr**2 #to m^2

    #then solve for volume

    wing_vol = (1/3)* t3.bo2 *(root_area+tip_area+ m.sqrt(root_area*tip_area)) #this doesn't take into account the sweep or twist

    #to find surface area of one wing
    wing_surf_area = foil_perimeter*t3.Cr*t3.bo2 - (t3.bo2/2)*(1-t3.taper)*t3.Cr #this is only one wing in m^2

    #actually do weight build up
    #wing
    wing_foam_weight = wing_vol*1000000*foam_d #grams
    wing_fiberglass_weight = wing_surf_area*thickness*0.9144*1000000*fiberglass_35oz_d*wing_num_layer_5_oz + wing_surf_area*0.9144*1000000*thickness*fiberglass_145oz_d*wing_num_layer_145_oz
    wing_resin_and_hardner_weight = wing_fiberglass_weight*composite_mix
    wing_resin_weight = (wing_resin_and_hardner_weight/(resin_mix + hardner_to_resin_mix))*resin_mix
    wing_hardner_weight = wing_resin_and_hardner_weight-wing_resin_weight
    wing_longset_hardner_weight = wing_hardner_weight*hardner_mix
    wing_shortset_hardner_weight = wing_hardner_weight-wing_longset_hardner_weight
    # add spar calc
    carbon_spar = []
    num_spar_thicc = int(t3.bo2*3.28084) #calculates the number of times we need to up the thiccness of the spar
    while num_spar_thicc > 0:
        if num_spar_thicc == int(t3.bo2*3.28084):
            carbon_spar.append(2*t3.bo2 * 100 * carbon_spar_width * 2.54 * thickness * 91.44 * carbon_fiber_8oz_d)
        else:
            carbon_spar.append(2*((t3.bo2*3.28084)-((t3.bo2*3.28084)/(int(t3.bo2*3.28084)-num_spar_thicc)))*100*carbon_spar_width*2.54*thickness*91.44*carbon_fiber_8oz_d)
        num_spar_thicc = num_spar_thicc-1
    counter = len(carbon_spar)
    carbon_spar_weight = 0
    while counter>0:
        carbon_spar_weight = carbon_spar_weight + carbon_spar[counter-1]   #should be in g
        counter=counter-1

    #add glass bubbles
    glass_bubbles_weight = wing_surf_area*10000*glass_bubbles_d*thickness*91.44
    single_wing_weight = wing_foam_weight+wing_fiberglass_weight+wing_resin_and_hardner_weight + carbon_spar_weight + glass_bubbles_weight
    #do tail approx

    #add in the carbon fiber rod for tail

    #fuselage approx

    #electronics approx
        #use this for the prop calcs and battery sizing


    total_plane_weight = 2*single_wing_weight

    print("Wing Foam Weight (g): ",wing_foam_weight)
    print("Wing Fiberglass Weight (g): ", wing_fiberglass_weight)
    print("Wing Carbon Spar Weight (g): ", carbon_spar_weight)
    print("Wing Glass Bubbles Weight (g): ", glass_bubbles_weight)
    print("Wing Resin and Hardner Weight (g): ", wing_resin_and_hardner_weight)
    print("Wing Resin Weight (g): ", wing_resin_weight)
    print("Wing Long Set Hardener Weight (g): ", wing_longset_hardner_weight)
    print("Wing Short Set Hardener Weight (g): ", wing_shortset_hardner_weight)
    print("Single Wing Weight (g): ",single_wing_weight)



    #print("Chord Length (in): ",t3.Cr*39.3701)
    #print("Max Thickness (in): ",t3.Cr * 39.3701*.097)
    #print("tip area: ",tip_area,", root area: ",root_area)
    #print("root perimeter (m): ",root_perimeter)
    #print("tip perimeter (m): ", tip_perimeter)
    #print("wing surface area: ",wing_surf_area)

if __name__ == '__main__':
    main()