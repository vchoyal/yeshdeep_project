from ase.io import read
from ase.calculators.eam import EAM
from ase import units
import numpy as np
import os
import sys

print("🚀 Starting Strain–Stress simulation script...")

# === Input Files ===
structure_path = "../data/Cu3Au.poscar"     # structure file
potential_path = "potential/CuAu_fitted.eam.fs"  # EAM potential
output_dir = "outputs/"
os.makedirs(output_dir, exist_ok=True)

print("📁 Checking input files...")

# === Check structure file ===
if not os.path.exists(structure_path):
    print(f"❌ Structure file not found: {structure_path}")
    sys.exit(1)
else:
    print(f"✅ Found structure file: {structure_path}")

# === Check potential file ===
if not os.path.exists(potential_path):
    print(f"❌ Potential file not found: {potential_path}")
    sys.exit(1)
else:
    print(f"✅ Found potential file: {potential_path}")

# === Load Structure ===
try:
    atoms = read(structure_path)
    print(f"✅ Loaded {len(atoms)} atoms from {structure_path}")
except Exception as e:
    print(f"❌ Error reading structure: {e}")
    sys.exit(1)

# === Assign Potential ===
try:
    atoms.calc = EAM(potential=potential_path)
    print("✅ EAM potential successfully assigned.")
except Exception as e:
    print(f"❌ Error assigning EAM potential: {e}")
    sys.exit(1)

# === Define Strain Parameters ===
n_steps = 50               # Number of strain steps
strain_max = 0.10          # Maximum strain (10%)
strain_axis = 2            # z-axis strain

print("🧮 Strain Parameters:")
print(f"   → Axis: {strain_axis} (z-axis)")
print(f"   → Steps: {n_steps}")
print(f"   → Max Strain: {strain_max*100:.1f}%")

# === Output File ===
out_file = os.path.join(output_dir, "stress_strain.txt")
f = open(out_file, "w")
f.write("Step\tStrain\tStress(GPa)\tEnergy(eV)\n")

print("⚙️ Starting Strain–Stress loop...")
print("-----------------------------------------")

try:
    for i in range(n_steps + 1):
        strain = i * strain_max / n_steps

        # Apply strain along the selected axis
        cell = atoms.get_cell()
        cell[strain_axis, strain_axis] *= (1 + strain)
        atoms.set_cell(cell, scale_atoms=True)

        # Get stress tensor and energy
        stress_tensor = atoms.get_stress(voigt=False)
        stress_zz = -stress_tensor[strain_axis, strain_axis] / units.GPa  # Convert to GPa
        energy = atoms.get_potential_energy()

        f.write(f"{i}\t{strain:.5f}\t{stress_zz:.5f}\t{energy:.6f}\n")

        if i % 5 == 0:
            print(f"🧩 Step {i}/{n_steps}: strain={strain:.4f}, stress={stress_zz:.3f} GPa, E={energy:.4f} eV")

    print("-----------------------------------------")
    print("🎯 Strain–Stress simulation completed successfully!")
    print(f"📄 Results saved to:\n   {out_file}")

except Exception as e:
    print(f"❌ Error during strain simulation: {e}")

finally:
    f.close()
    print("🧹 File closed, exiting simulation.")

