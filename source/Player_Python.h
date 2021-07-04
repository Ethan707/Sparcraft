#pragma once

#include "Common.h"
#include "Player.h"

namespace SparCraft
{
	class Player_Python;
}

/*----------------------------------------------------------------------
 | Attack Closest Player
 |----------------------------------------------------------------------
 | Chooses an action with following priority:
 | 1) If it can attack, ATTACK closest enemy unit
 | 2) If it cannot attack:
 |    a) If it is in range to attack an enemy, WAIT until can shoot again
 |    b) If it is not in range of enemy, MOVE towards closest
 `----------------------------------------------------------------------*/
class SparCraft::Player_Python : public SparCraft::Player
{
public:
	Player_Python(const IDType &playerID);
	void getMoves(GameState &state, const MoveArray &moves, std::vector<Action> &moveVec);
	IDType getType() { return PlayerModels::Python; }
};