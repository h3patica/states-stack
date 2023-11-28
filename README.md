# states-stack
A HoI4 automated state transfer tool for creating mods based on modifying states put onto a virtual 'stack'. 

Old and somewhat outdated demonstration:

https://github.com/h3patica/states-stack/assets/73669382/094f1a5b-d16e-44c7-bb41-a2fcaabeb1b2


## Usage
The purpose of this tool is to be able to change the attributes of states within HoI4 en-masse, including their owner, cores, and claims. This is done via `pull`ing states onto the stack, which can then be modified, and then `push`ed back as re-written state files to the ./states/ directory.

The only config required is setting the path of your HoI4 directory in `path.txt`.

Information on commands and their usage can be found via the `help` command.
