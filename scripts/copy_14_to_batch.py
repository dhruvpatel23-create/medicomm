import shutil
from pathlib import Path

batch_dir = Path("output/imagegen/ophthalmology-2017-2019-img1")
gen_dir = Path("scripts/generate_14_oph_atlas")

mapping = {
    "q015_port_wine.png": "medicomm-img1-aiims-2018-ophthalmology-q015.png",
    "q017_oculomotor_palsy.png": "medicomm-img1-aiims-2018-ophthalmology-q017.png",
    "neet2018_q007_hypopyon.png": "medicomm-img1-neet-pg-2018-ophthalmology-q007.png",
    "q001_choroidal_melanoma.png": "medicomm-img1-aiims-2019-ophthalmology-q001.png",
    "q002_titmus_fly.png": "medicomm-img1-aiims-2019-ophthalmology-q002.png",
    "q003_fish_hook.png": "medicomm-img1-aiims-2019-ophthalmology-q003.png",
    "q006_swinging_flashlight.png": "medicomm-img1-aiims-2019-ophthalmology-q006.png",
    "q009_ffa_macular_ischemia.png": "medicomm-img1-aiims-2019-ophthalmology-q009.png",
    "q011_retina_opl_histology.png": "medicomm-img1-aiims-2019-ophthalmology-q011.png",
    "q013_anterior_ethmoidal_block.png": "medicomm-img1-aiims-2019-ophthalmology-q013.png",
    "neet2019_q005_orbital_blowout_ct.png": "medicomm-img1-neet-pg-2019-ophthalmology-q005.png",
    "neet2019_q009_express_shunt.png": "medicomm-img1-neet-pg-2019-ophthalmology-q009.png",
    "neet2019_q010_maddox_rod.png": "medicomm-img1-neet-pg-2019-ophthalmology-q010.png",
    "neet2019_q011_cover_uncover_test.png": "medicomm-img1-neet-pg-2019-ophthalmology-q011.png",
}

for src_name, dst_name in mapping.items():
    src_file = gen_dir / src_name
    dst_file = batch_dir / dst_name
    if src_file.exists():
        shutil.copy2(src_file, dst_file)
        print(f"Copied {src_name} -> {dst_name} ({dst_file.stat().st_size} bytes)")
    else:
        print(f"ERROR: Missing {src_name}")
