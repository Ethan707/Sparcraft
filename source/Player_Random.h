#pragma once

#include "Common.h"
#include "Player.h"
#include "Random.hpp"

namespace SparCraft
{
	/*----------------------------------------------------------------------
 | Random Player
 |----------------------------------------------------------------------
 | Chooses a random legal move per unit and implements it
 `----------------------------------------------------------------------*/
	class Player_Random : public Player
	{
		RandomInt rand;

	public:
		Player_Random(const IDType &playerID);
		void getMoves(GameState &state, const MoveArray &moves, std::vector<Action> &moveVec);
		IDType getType() { return PlayerModels::Random; }
	};
}