# Advanced Minecraft Scripting
This project aims at producing a more human readable version of Minecraft's mcfunction format. This documentation will explain the new syntax, the components of the compiler and contains a user guide to use this program to compile your project into a Minecraft datapack.

## Syntax

The AMS scripting language is based on the mcfunction syntax. The new syntax simply aims at making the code more readable and reducing duplicate code.

### The Child System

Whenever the compiler finds an line of code indented with a **tab** or a **space** it will interpret this as a child to the previous line of code with one less indent. Whenever a command is a child it's parent is simply prepended.

**Example:**
```mcfunction
execute store result score @s
    x1 run data get entity @s Pos[0] 1
    y1 run data get entity @s Pos[1] 1
    z1 run data get entity @s Pos[2] 1
```

Parsed through the compiler this is assembled into this valid mcfunction code.

```mcfunction
execute store result score @s x1 run data get entity @s Pos[0] 1
execute store result score @s y1 run data get entity @s Pos[1] 1
execute store result score @s z1 run data get entity @s Pos[2] 1
```

This can be done as many times as necessary.

**Example:**
```mcfunction
execute as @a
  if score @s dummy_scores matches 1
    run function main:func1
  if score @s dummy_scores matches 2
    if score state game_states matches 0
      run function main:func2
```
Compiles to:
```mcfunction
execute as @a if score @s dummy_scores matches 1 run function main:func1
execute as @a if score @s dummy_scores matches 2 if score state game_states matches 0 run function main:func2
```

### Comments and empty lines

In an input file comments can be added with a "#". While empty lines or lines only containing white-spaces will be ignored, comments will be transferred into the compiled code. Make sure, that the comment has as many or more white-spaces in the front as the following line:

```
parent
  line1

  #comment
  line2
```

will compile to
```
parent line1
#comment
parent line2
```

If a comment however is succeeded by a line with more white spaces than itself it will throw a warning and not compile that line, since comments can not have children:

```error
parent
  line1
#comment
  line2
```

Will produce a warning.

## Usage

There are many different options to either integrate the compiler into your own application or directly use it as an application. This section will focus on the former.

### Visual Interface

Simply run ``interface.py`` with python and press "Load and Compile File". You will be prompted with a read path to select. Afterwards the program may briefly freeze but you will then be prompted with a save dialog. Select where you want to save the compiled file to and press "Save".

### Run as an import
Import the compiler into your program and run it with an input and an output path.:
```python
from interface import compile
compile(input_path, output_path)
```

### Run in the Console
Using the ams transpiler in the console yields the distinct advantage of adding config files allowing the user to compile entire projects at a time.

To install the ams transpiler for windows powershell find the `install.ps1` script. This script will then create a new powershell-profile if needed and add an alias to the setup for the `powershell_wrapper.ps1` script you can find in `/src/`.

After running the installer you can reference the wrapper-script with `ams` in Powershell. Arguments will be passed on to the python script. You can get a help prompt by typing in powershell:

```
>>> ams -h

asm transpiler is designed for mincraft mcfunctions to be transformed [...]
```

#### Syntax

The transpiler script takes six possible arguments:
```
ams [-c <filename>] [-i <filename>] [-o <filename>] [-d --debug] [-h, --h, -help]
```
or
```
ams -p [project file] -i [filename(s)] -o [filename(s)]
```

| Argument | Description |
|----------|-------------|
|    -h    | Shows help prompt. Aliases are `--h` or `-help`.
|    -p    | Creates configuration file which can be used by -c
|    -c    | Takes a path to a configuration file. See the config file section for more info.
|    -i    | Takes a single input file, that will be passed through the compiler. Will be ignored if `-c` is supplied.
|    -o    | Takes a name for a single output file. -i is required. If no output file is supplied the transpiler will prepend "out_" infront of the path supplied with `-i`.
|    -d    | If flag is set the transpiler will show debug information. Alias: `--debug`

#### Configuration File

If you want to transpile multiple files at once you will want to write a configuration file. The configuration file must supply an array of input and output files in the JSON format. Example:

```json
{
  "ifiles": [
    "folder/input1.mcfunction",
    "folder/input2.mcfunction",
    "input3.mcfunction"
  ],

  "ofiles": [
    "folder/output1.mcfunction",
    "folder/output2.mcfunction",
    "output3.mcfunction"
  ]
}
```

The paths can either be relative to the current working directory or absolute. They require no formatting beyond that.

After you have written the configuration file you can feed the transpiler with it.

#### Creating a Configuration File

Configuration files can be created either by hand or with the -p tag.
```
ams -p [project file] -i [filename(s)] -o [filename(s)]
```

The project file is the path to the configuration file which will be written to. The "-i" tag defines that the following will be paths to the input files as defined in the previous section. All filenames have to be separated by spaces.

**Example**:
```
ams -p project.json -i in1 in2 in3 -o out1 out2 out3
```
Alternatively to `-p` you can also use `--createproject`

#### Aliasing

The configuration file may contain a `define` tag. It defines an object pairing aliases to their values.

**Example**
```json
{
  ...
  "define": {
    "alias1": "value1",
    "alias2": "value2"
  }
}
```

This tag will not be autogenerated when using `-p` but has to be added manually.

#### Examples
Let's say in your datapack you have a folder-structure like this:
```
+---namespace
|   +---config.json
|   +---source
|   |   +---function1.ams
|   |   \---function2.ams
|   \---functions
```

The file ending .ams is reccomended, but the fileending .mcfunction may be more practical to use with existing IDEs. The transpiler does not differenciate between different suffixes. The config file may contain something like this:

```json
{
  "ifiles": [
    "./source/function1.ams",
    "./source/function2.ams"
  ],

  "ofiles": [
    "./functions/function1.mcfunction",
    "./functions/function2.mcfunction"
  ]
}
```

Pass the configuration file into the ams transpiler:
```
>>> ams -c config.json

Compiling ./source/function1.ams...
DONE!

Compiling ./source/function2.ams...
DONE!
```

The transpiler will then produce the specified output files or overwrite them if they already exist.

If you want to transpile single files you can use the -i and -o tag:

```
ams -i ./source/function1.ams -o ./functions/function1.mcfunction
```
