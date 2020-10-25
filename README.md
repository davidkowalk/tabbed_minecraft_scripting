# Tabbed Minecraft Scripting
This project aims at producing a more human readable version of Minecraft's mcfunction format. This documentation will explain the new syntax, the components of the compiler and contains a user guide to use this program to compile your project into a Minecraft datapack.

Please read the docs in [/docs/markdown/](https://github.com/davidkowalk/advanced_minecraft_scripting/blob/master/docs/markdown/).

**Note**: This project was formerly called "advanced minecraft scripting". The abbreviation "ams" is a remnant of that name.

## The Language

The AMS transpiler does not actually introduce a new language, but offers a way of organizing existing minecraft code into a more readable format using indentation.

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

This can be useful when you need to write a number of similar lines. **For example:**
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

If statements can also be dramatically simplified:

```mcfunction
execute if
  condition1 run
    say Detected Condition 1
    function namespace:condition1

  condition2 run
    say Detected Condition 2
    function namespace:condition2
```


## Installation

Python scripts don't necessarily need to be installed. This section will however explain how to set it up.

### Download Python

First you need to get the newest version of python.

For Windows you can simply download the newest version from [python.org](https://www.python.org/).

If you are on Linux you can install python3 via apt:
```
sudo apt update
sudo apt install python3
```

Check the installation afterwards with
```
python3 -V
```

### Setting up the Scripts

Download this repository either through the github website or using git through the console:
```
git clone https://github.com/davidkowalk/advanced_minecraft_scripting.git
```
or if you don't have git:
```
wget https://github.com/davidkowalk/advanced_minecraft_scripting/archive/master.zip -outfile tabbed_minecraft_scripting.zip
```

Once you downloaded (and unpacked) the tool into a folder you would like to store it in you need to resolve the dependencies. This project is only dependent on kivy to generate the user interface.
Type
```
pip install kivy
```

### Install the script as an alias in the console

If you are on windows it's also recommended to run the install.ps1 or install.sh on linux, so you can use the ams-transpiler in the console.

**Windows Powershell**
```powershell
PS> .\install.ps1

Searching for profile...
Updating start-up script...
Saving to Disk...

===========
|| DONE! ||
===========
PS >
```

**Linux Bash**
```
user: $ ./install.sh

Finding Executable Directory...
Adding alias to startup file...
Update Current Session
===========
|| DONE! ||
===========
```

Please note that the Windows script will check whether the script is already installed, the Linux script will not. The scripts set the python script as an alias. The install will break if you move the repository after running the script.

See [`/docs/markdown/docs_main.md`](https://github.com/davidkowalk/advanced_minecraft_scripting/blob/master/docs/markdown/docs_main.md#run-in-the-console) for usage reference.


Please report any issues you are having with the install.

### Updating

To update the script to a newer version simpy download the git repository and replace your old `ams_compiler.py` with the newer verion of the file.
