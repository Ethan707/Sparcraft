#include "Player_Python.h"

using namespace SparCraft;

Player_Python::Player_Python(const IDType &playerID)
{
	_playerID = playerID;
}

void Player_Python::getMoves(GameState &state, const MoveArray &moves, std::vector<Action> &moveVec)
{
	moveVec.clear();
	std::cout << "Begin" << std::endl;
	std::cout << "PlayerID " << (int)_playerID << std::endl;
	state.print();
	moves.print();
	std::cout << "End" << std::endl;

	// receive the move index from python
	for (IDType u(0); u < moves.numUnits(); ++u)
	{
		int moveIndex;
		std::cin >> moveIndex;
		moveVec.push_back(moves.getMove(u, moveIndex));
	}
}
