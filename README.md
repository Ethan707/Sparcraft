<!--
 * @Author: Ethan Chen
 * @Date: 2021-07-04 11:22:06
 * @LastEditTime: 2021-07-05 20:58:34
 * @LastEditors: Ethan Chen
 * @Description: 
 * @FilePath: \Sparcraft\README.md
-->
# Sparcraft

Compilation Instructions:

1. Install the required libraries
   * `libsdl2-dev`
   * `libsdl2-image-dev`

2. Clone the BWAPI github repository somewhere on your system

   `git clone https://github.com/bwapi/bwapi.git`

3. Edit the Makefile to point to the directory that you cloned `BWAPI`

	`BWAPI_DIR=/where_you_cloned_to/bwapi/bwapi`

	**P.S. it is `bwapi/bwapi` here**

4. If your BWAPI_DIR doesn't contain the file `svnrev.h`, you need to generate it using the vbs script in that dir
   (note: this may have to be done in windows, but you can just copy the generated .h files to Linux and it will work)

5. Run `make` in the SparCraft directory, the binary will go to the `SparCraft/bin` directory

6. cd to `SparCraft/bin` and run `./SparCraft ../sample_experiment/sample_exp.txt`

## Format of Communication

```
Begin
Time {gameTime}
Unit {Player} {HP} {firstTimeFree} {Position x} {Position y}
Unit {Player} {HP} {firstTimeFree} {Position x} {Position y}

Move {unitIndex} {Player} {MoveType} {moveIndex} {Position x} {Position y}
...
Move {unitIndex} {Player} {MoveType} {moveIndex} {Position x} {Position y}
End
```

## Action

### Attack

example:

```c++
moves.add(Action(unitIndex, playerIndex, ActionTypes::ATTACK, u));
```

```c++
SparCraft::Action::Action(
    const SparCraft::IDType &unitIndex,
    const SparCraft::IDType &player,
    const SparCraft::IDType &type,
    const SparCraft::IDType &moveIndex
)
```

`unitIndex` -> index of unit

`playerIndex` -> unit's owner

`moveIndex` -> move target, here is the enemy Unit `u`

### Move

```c++
for (IDType d(0); d < Constants::Num_Directions; ++d)
...
moves.add(Action(unitIndex, playerIndex, ActionTypes::MOVE, d, dest));
```

```c++
Action::Action(
    const IDType &unitIndex,
    const IDType &player,
    const IDType &type,
    const IDType &moveIndex,
    const Position &dest
)
```

`unitIndex` -> index of unit

`playerIndex` -> unit's owner

`moveIndex` -> Here is the **index of direction，not the move target**

## DSL for Sparcarft

TODO

### TODO List

1. Add Bottom Up Search
2. Add simulated annealing
3. ~~Add player id to Player_Python~~
4. ~~Test 2 python players at the same time and paly~~
   1. ~~Python random vs Python random~~
   2. ~~Python AttackClosest vs Python AttackClosest~~
   3. ~~Python random vs Python AttackClosest~~
