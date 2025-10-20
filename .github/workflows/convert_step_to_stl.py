#!/usr/bin/env python3
"""
Convert STEP files to STL format using FreeCAD
Usage: python convert_step_to_stl.py <step_file>
"""

import sys
import os
from FreeCAD import Part
from MeshPart import meshFromShape

def convert_step_to_stl(step_file):
    """Convert a STEP file to STL format"""
    try:
        # Get the output STL filename
        stl_file = os.path.splitext(step_file)[0] + '.stl'
        
        # Get quality settings from environment
        linear_def = float(os.environ.get('LINEAR_DEFLECTION', 0.002))
        angular_def = float(os.environ.get('ANGULAR_DEFLECTION', 0.174533))
        
        print(f"Converting {step_file} to {stl_file}...")
        print(f"  Quality: LinearDeflection={linear_def}mm, AngularDeflection={angular_def:.4f}rad")
        
        # Import STEP file
        shape = Part.Shape()
        shape.read(step_file)
        
        # Create mesh from shape with high-quality settings
        mesh = meshFromShape(
            Shape=shape,
            LinearDeflection=linear_def,
            AngularDeflection=angular_def
        )
        
        # Export to STL
        mesh.write(stl_file, "STL")
        
        print(f"✓ Successfully created {stl_file}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {step_file}: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_step_to_stl.py <step_file>", file=sys.stderr)
        sys.exit(1)
    
    step_file = sys.argv[1]
    if not os.path.exists(step_file):
        print(f"Error: File {step_file} not found", file=sys.stderr)
        sys.exit(1)
    
    success = convert_step_to_stl(step_file)
    sys.exit(0 if success else 1)
