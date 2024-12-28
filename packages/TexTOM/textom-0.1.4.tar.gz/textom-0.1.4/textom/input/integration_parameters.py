############ Input ###############
path_in = '/dataSATA/data_synchrotron/esrf_id13_2024_2_enthesis/20240215/RAW_DATA/biomorph_blobb/ls3299_biomorph_blobb.h5'
h5_proj_pattern = 'biomorph_blobb_tt_tomo_d*.1'
h5_data_path = 'measurement/eiger'
h5_tilt_angle_path = None #'instrument/positioners/smyd'
h5_rot_angle_path = None # 'instrument/positioners/owisrz'
h5_ty_path = 'measurement/nnp5_position'
h5_tz_path = 'measurement/nnp6_position'
h5_fov0_path = 'technique/dim0'
h5_fov1_path = 'technique/dim1'
h5_ion_path = 'measurement/ct34'
dir_out  = '/dataSATA/data_synchrotron/esrf_id13_2024_2_enthesis/20240215/PROCESSED_DATA/'
title = 'biomorph_blobb'
resume = 186 # put -1 to start at the beginning

# Integration mode
mode = 1 # 1: 1D, 2: 2D, 3: both

# CPU - parallelisation
n_tasks = 8
cores_per_task = 16

# Parameters for pyFAI azimuthal integration
rad_range = [0.4, 35] # radial range
rad_unit = 'q_nm^-1' # radial parameter and unit ('q_nm^-1', ''2th_deg', etc)
azi_range = [-180, 180] # azimuthal range in degree
npt_rad = 100 # number of points radial direction
npt_azi = 120 # number of points azimuthal direction
npt_rad_1D = 2000 # number of points radial direction
int_method=('bbox','csr','cython') # pyFAI integration methods
poni_path = '/dataSATA/data_synchrotron/esrf_id13_2024_2_enthesis/20240215/PROCESSED_DATA/HWS_R2E_ENV/R3VIEWER/m290.poni'
mask_path = '/dataSATA/data_synchrotron/esrf_id13_2024_2_enthesis/20240215/PROCESSED_DATA/mask_ls3299.edf'
polarisation_factor= 0.95 # polarisation factor, usually 0.95 or 0.99
flatfield_correction = None
solidangle_correction = True
darkcurrent_correction = None
##############################