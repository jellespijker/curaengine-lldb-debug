# curaengine-lldb-debug
LLDB debugging tools (such as pretty printers) for CuraEngine

![GitHub Logo](resources/prettyprint.jpg)

## Currently implemented
 - [x] cura::Temperature
 - [x] cura::Velocity
 - [x] cura::Acceleration
 - [x] cura::LayerIndex
 - [x] cura::Ratio
 - [x] cura::AngleDegrees
 - [x] cura::Point3
 - [x] cura::Point
 - [x] cura::AABB3D
 - [x] cura::ExtruderTrain
 - [x] cura::LayerPlan (partially implemented)
 
  # Instructions
 
 Add the following to your ``~/.ldbinit``
 ```txt
settings set target.load-cwd-lldbinit true
```
Create a `.ldbinit` file in the root of your **CuraEngine** directory containing the following:
```text
command script import <path to your curaengine-lldb-debug repo>/curaengine.py
```

# Usefull sources:

- https://lldb.llvm.org/use/variable.html
- https://lldb.llvm.org/python_reference/index.html
- https://github.com/llvm/llvm-project/tree/master/lldb/examples
- https://github.com/fantaosha/LLDB-Eigen-Pretty-Printer/blob/master/LLDB_Eigen_Pretty_Printer.py
