# HW 1 - Monopoles
### Bruh Beyene

A complete depth-first search that attempts to place m monopoles (1…m) into n rooms, where no pairs add to equal another in the same room, e.g. if (1, 2) were in room 1, then (3) must be in another room.

I started by studing Bart Massey's 'Sliding Tile Puzzle Solver' which used a dfs. Here, no state information needs to be saved explicitly because no state can be revisited while traversing possibilites. The following was scribbled on paper before I understood the problem ...

> while current != n
>>	depth = 0
>>	room = 0
>>	if compatible
>>>		place current
>>>		current++
>>>		depth++
>>>		room++

... which isn't correct at all but it showed me that I should be tracking the state of the room configuration and not the traversal of the rooms. As I drew out the tree, I saw that the depth was the monopole count. If n = 2 and the rooms are in order:

- at depth 1: [ 1 ][  ]
- at depth 2: [ 1 ][ 2 ] , [ 1,2 ][  ]
- at depth 3: [ 1,3 ][ 2 ] , [ 1 ][ 2,3 ] , [ 1,2,3 ][  ] , [ 1,2 ][ 3 ]

So, the dfs stack became the possible rooms while the depth was the current monopole count. When all of the rooms were exhausted with no branch having a solution, it removes the monopole (back up a level) and tries the next room of the branch above.

What is left is seeing if a heuristic exists.
