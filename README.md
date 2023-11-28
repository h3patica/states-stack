# states-stack
A HoI4 automated state transfer tool for creating mods based on modifying states put onto a virtual 'stack'. 

![Demonstration of an older version](https://cdn.discordapp.com/attachments/1167493068543508521/1169461586021330944/2023-11-01_22-20-07.mp4?ex=65712c79&is=655eb779&hm=96833c6f87ae6c3bf955d2439e1e4890d0a07f3e216826107ac362da0311dffe&)

<video src="[LINK](https://cdn.discordapp.com/attachments/1167493068543508521/1169461586021330944/2023-11-01_22-20-07.mp4?ex=65712c79&is=655eb779&hm=96833c6f87ae6c3bf955d2439e1e4890d0a07f3e216826107ac362da0311dffe&)" controls="controls" style="max-width: 730px;">
</video>

## Usage
The purpose of this tool is to be able to change the attributes of states within HoI4 en-masse, including their owner, cores, and claims. This is done via `pull`ing states onto the stack, which can then be modified, and then `push`ed back as re-written state files to the ./states/ directory.

The only config required is setting the path of your HoI4 directory in `path.txt`.

Information on commands and their usage can be found via the `help` command.
