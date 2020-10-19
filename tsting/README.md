# HW 1 - Monopoles
### Bruh Beyene

A complete depth-first search that attempts to place m monopoles (1…m) into n rooms, where no pairs add to equal another in the same room, e.g. if (1, 2) were in room 1, then (3) must be in another room.

I started by studying Bart Massey's 'Sliding Tile Puzzle Solver' which has a dfs solver. But here, no stop list because no state can be revisited while traversing possibilites. The following was scribbled on paper before I understood the problem ...

> while current != m
>>	depth = 0
>>	room = 0
>>	if compatible
>>>		place current
>>>		current++
>>>		depth++
>>>		room++

... which isn't correct at all but it showed me that I should be tracking and traversing the states of the room configuration and not the rooms themselves. As I drew out the tree, I saw that the depth was the monopole count. Then, if n = 2 and m = 3, the first, second and fourth of the possible configurations are compatible ...

- at depth 1: [ 1 ][ - ]
- at depth 2: [ 1 ][ 2 ] , [ 1,2 ][ - ]
- at depth 3: [ 1,3 ][ 2 ] , [ 1 ][ 2,3 ] , [ 1,2,3 ][ - ] , [ 1,2 ][ 3 ]

... so, the dfs stacks became the possible rooms while the depth was the current monopole count. When all of the rooms were exhausted with no branch having a solution, it removes the monopole from the stack and tries the next rooms of the branch above.

What is left is seeing if a heuristic exists.
