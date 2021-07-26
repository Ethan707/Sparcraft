#include "Player_Random.h"

using namespace SparCraft;

Player_Random::Player_Random(const IDType &playerID)
	: rand(0, std::numeric_limits<int>::max(), Constants::Seed_Player_Random_Time ? static_cast<unsigned int>(std::time(0)) : 0)
{
	_playerID = playerID;
}

void Player_Random::getMoves(GameState &state, const MoveArray &moves, std::vector<Action> &moveVec)
{
	std::cout << "Begin" << std::endl;
	std::cout << "PlayerID " << (int)_playerID << std::endl;
	state.print();
	moves.print();
	std::cout << "End" << std::endl;
	for (size_t u(0); u < moves.numUnits(); u++)
	{
		moveVec.push_back(moves.getMove(u, rand.nextInt() % moves.numMoves(u)));
	}
}
