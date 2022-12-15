# 2022-3806ICT-Group-Assignment

The goal of this assignment was to use the process analysis toolkit (PAT3.exe) (available: https://pat.comp.nus.edu.sg/ ) to generate mutations of a maze-
 as a simulated agent moved navigated the maze towards a goal cell.
 
There were several rules about this scenario-
 1: The agent can only take a limited number of steps proportional to the size of the maze.
 2: If the goal itself is moved it should still be reachable within the remaining steps.
 3: The path already taken by the agent must be preserved fully.
 4: The agent will have a probability to trigger the mutation with each step.
 5: The maze must remain whole- no there can be no unreachable sections.
 6: The general maze-like structure should be preserved rather than replaced with noise.
 
The resultant methods generate a mutations by finding T-junctions or potential T-junctions resembling:

#####     #####
XXXXX     XXX#X
##X## AND ##X## (respectively)
##X##     ##X##

and opening or closing one of the three paths, thus each distinct change preserves a mazelike structure but also creates or destroyes a possible pathing choice.
