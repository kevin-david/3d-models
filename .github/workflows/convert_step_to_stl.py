#!/usr/bin/env python3
"""
Convert STEP files to STL format using OpenCASCADE
Usage: python convert_step_to_stl.py <step_file>
"""

import sys
import os
from OCC.Core import STEPControl_Reader, BRepMesh_IncrementalMesh
from OCC.Core import TopExp_Explorer, TopAbs_FACE
from OCC.Core import StlAPI_Writer
from OCC.Core import BRep_Tool
from OCC.Core import TopoDS

def convert_step_to_stl(step_file):
    """Convert a STEP file to STL format using OpenCASCADE"""
    try:
        # Get the output STL filename
        stl_file = os.path.splitext(step_file)[0] + '.stl'
        
        # Get quality settings from environment
        linear_def = float(os.environ.get('LINEAR_DEFLECTION', 0.002))
        angular_def = float(os.environ.get('ANGULAR_DEFLECTION', 0.174533))
        
        print(f"Converting {step_file} to {stl_file}...")
        print(f"  Quality: LinearDeflection={linear_def}mm, AngularDeflection={angular_def:.4f}rad")
        
        # Read STEP file
        reader = STEPControl_Reader()
        status = reader.ReadFile(step_file)
        
        if status != 1:  # IFSelect_RetDone
            raise Exception(f"Failed to read STEP file: status {status}")
        
        # Transfer all roots
        reader.TransferRoots()
        shape = reader.OneShape()
        
        if shape.IsNull():
            raise Exception("No shape found in STEP file")
        
        # Create mesh with specified quality
        mesh = BRepMesh_IncrementalMesh(shape, linear_def, False, angular_def, True)
        mesh.Perform()
        
        # Write STL file
        writer = StlAPI_Writer()
        writer.Write(shape, stl_file)
        
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
