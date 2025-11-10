import openterrace
import numpy as np
import math
import pickle 

SOLID_NAME = 'basalto'     
OUTPUT_FILENAME = f'resultados_{SOLID_NAME}.pkl'

T_init = 40 + 273.15
T_fluid_in = 80 + 273.15
flow_rate = 1.0
porosity = 0.4
L_bed = 2.5
D_tank = 1.0
D_p = 0.025
sim_duration = 8 * 3600
output_freq = 300
N_nodes = 50

A_cross_section = np.pi * (D_tank/2)**2
G = flow_rate / A_cross_section



def run_simulation_and_save():

    ot = openterrace.Simulate(t_end=sim_duration, dt=1.0) 
    
    try:
        # Configuración del modelo y sustancias
        packed_bed = ot.create_phase(n=N_nodes, type='bed') 
        packed_bed.select_domain_shape(
            domain='cylinder_1d', 
            H=L_bed, D=D_tank, epsilon=porosity, dp=D_p, 
            G=G
        )
        packed_bed.select_substance('ATS50')
        packed_bed.select_substance(SOLID_NAME)
        packed_bed.select_initial_conditions(T=T_init)
        
        # Condiciones de frontera
        packed_bed.select_bc(bc_type='fixed_value', parameter='T', value=T_fluid_in, position=(slice(None, None, None), 0))
        packed_bed.select_bc(bc_type='zero_gradient', parameter='T', position=(slice(None, None, None), -1))

        packed_bed.select_output(times=np.arange(0, sim_duration + output_freq, output_freq))

        ot.run_simulation()
        
        time_data_h = packed_bed.data.time / 3600
        T_solid_C = packed_bed.data.T[:, -1, 0] - 273.15 
        
        
        with open(OUTPUT_FILENAME, 'wb') as f:
            pickle.dump((time_data_h, T_solid_C), f)
            
        print(f"guardado {SOLID_NAME} guardados en {OUTPUT_FILENAME}")
        
    except Exception as e:
        print(f"fallo de  {SOLID_NAME}. Error: {e}")


if __name__ == "__main__":
    run_simulation_and_save()