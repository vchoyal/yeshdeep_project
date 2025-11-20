from ase.io import read, Trajectory
from ase.calculators.eam import EAM
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
import numpy as np
import os

# --- File paths ---
structure_path = "../data/Cu3Au.poscar"
potential_path = "potential/CuAu_fitted.eam.fs"
output_dir = "outputs/"
os.makedirs(output_dir, exist_ok=True)

print("🚀 Starting MD simulation with feature extraction...")
print("📁 Checking input files...")

# --- Check input files ---
if not os.path.exists(structure_path):
    raise FileNotFoundError(f"❌ Structure file not found: {structure_path}")
if not os.path.exists(potential_path):
    raise FileNotFoundError(f"❌ Potential file not found: {potential_path}")

# --- Load structure ---
atoms = read(structure_path)
print(f"✅ Loaded {len(atoms)} atoms from {structure_path}")

# --- Assign EAM potential ---
calc = EAM(potential=potential_path)
atoms.calc = calc

# --- Initialize velocities at 800 K ---
MaxwellBoltzmannDistribution(atoms, temperature_K=800)

# --- Setup MD integrator ---
timestep = 5 * units.fs
dyn = VelocityVerlet(atoms, timestep)

# --- Prepare output files ---
traj_path = os.path.join(output_dir, "md.traj")
data_path = os.path.join(output_dir, "md_features_output.txt")

traj = Trajectory(traj_path, 'w', atoms)
data_file = open(data_path, "w")

# --- Write header ---
data_file.write(
    "Step\tVolume(Å³)\tPressure(GPa)\tMeanForce(eV/Å)\tMaxForce(eV/Å)\t"
    "Stress_xx(GPa)\tStress_yy(GPa)\tStress_zz(GPa)\t"
    "TotalEnergy(eV)\tTemperature(K)\n"
)

print("⚙️ Running MD simulation and collecting features...")

# --- Run MD ---
n_steps = 2000
for step in range(n_steps):
    dyn.run(1)

    # --- Compute physical quantities ---
    epot = atoms.get_potential_energy()
    ekin = atoms.get_kinetic_energy()
    total_energy = epot + ekin
    temp = ekin / (1.5 * units.kB * len(atoms))

    stress_tensor = atoms.get_stress(voigt=False)
    stress_diag = np.diag(stress_tensor) / -units.GPa  # GPa
    stress_xx, stress_yy, stress_zz = stress_diag

    forces = atoms.get_forces()
    force_mags = np.linalg.norm(forces, axis=1)
    mean_force = np.mean(force_mags)
    max_force = np.max(force_mags)

    volume = atoms.get_volume()
    pressure = -np.trace(stress_tensor) / (3.0 * units.GPa)

    # --- Write data ---
    data_file.write(
        f"{step}\t{volume:.6f}\t{pressure:.6f}\t{mean_force:.6f}\t{max_force:.6f}\t"
        f"{stress_xx:.6f}\t{stress_yy:.6f}\t{stress_zz:.6f}\t"
        f"{total_energy:.6f}\t{temp:.2f}\n"
    )

    traj.write()

    # --- Log progress ---
    if step % 100 == 0:
        print(f"🧩 Step {step}: E_total={total_energy:.4f} eV, Temp={temp:.2f} K")

# --- Cleanup ---
data_file.close()
traj.close()

print("✅ MD simulation completed successfully!")
print(f"📊 Data saved to: {data_path}")
print(f"📄 Trajectory saved to: {traj_path}")

