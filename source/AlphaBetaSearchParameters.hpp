#pragma once

#include "Common.h"

namespace SparCraft
{
    class AlphaBetaSearchParameters;
}

class SparCraft::AlphaBetaSearchParameters
{                         // DEFAULT				DESCRIPTION
    IDType _searchMethod; // ID-AB                The Method to use for AB Search
    IDType _maxPlayer;    // Player_One			The player who will make maximizing moves
    IDType _maxDepth;     // Max_Depth            Maximum depth of AB search to allow

    size_t _timeLimit;          // 0					Search time limit. 0 means no time limit
    size_t _maxChildren;        // 10                   Max children at each node
    IDType _moveOrdering;       // ScriptFirst          Move ordering method for child generation
    IDType _evalMethod;         // LTD				Evaluation function type
    IDType _simScripts[2];      // NOKDPS               Policy to use for playouts
    IDType _playerToMoveMethod; // Alternate			The player to move policy
    IDType _playerModel[2];     // None                 Player model to use for each player
    int _beamSize;
    bool _learning;
    std::string _policyFilename;

    std::string _graphVizFilename; // ""                   File name to output graph viz file

    std::vector<IDType> _orderedMoveScripts;

    std::vector<std::vector<std::string>> _desc; // 2-column description vector

public:
    // default constructor
    AlphaBetaSearchParameters()
        : _searchMethod(SearchMethods::IDAlphaBeta), _maxPlayer(Players::Player_One), _maxDepth(Constants::Max_Search_Depth), _timeLimit(0), _maxChildren(10), _moveOrdering(MoveOrderMethod::ScriptFirst), _evalMethod(SparCraft::EvaluationMethods::Playout), _playerToMoveMethod(SparCraft::PlayerToMove::Alternate), _beamSize(20), _policyFilename("policy_filename"), _learning(false)
    {
        setPlayerModel(Players::Player_One, PlayerModels::None);
        setPlayerModel(Players::Player_Two, PlayerModels::None);
        setSimScripts(PlayerModels::NOKDPS, PlayerModels::NOKDPS);
    }

    const IDType &searchMethod() const { return _searchMethod; }
    const IDType &maxPlayer() const { return _maxPlayer; }
    const IDType &maxDepth() const { return _maxDepth; }
    const int &getBeamSize() const { return _beamSize; }
    const std::string &getFilename() const { return _policyFilename; }
    const bool &isLearning() const { return _learning; }
    const size_t &timeLimit() const { return _timeLimit; }
    const size_t &maxChildren() const { return _maxChildren; }
    const IDType &moveOrderingMethod() const { return _moveOrdering; }
    const IDType &evalMethod() const { return _evalMethod; }
    const IDType &simScript(const IDType &player) const { return _simScripts[player]; }
    const IDType &playerToMoveMethod() const { return _playerToMoveMethod; }
    const IDType &playerModel(const IDType &player) const { return _playerModel[player]; }
    const std::string &graphVizFilename() const { return _graphVizFilename; }
    const std::vector<IDType> &getOrderedMoveScripts() const { return _orderedMoveScripts; }

    void setSearchMethod(const IDType &method) { _searchMethod = method; }
    void setMaxPlayer(const IDType &player) { _maxPlayer = player; }
    void setMaxDepth(const IDType &depth) { _maxDepth = depth; }
    void setBeamSize(const int &beam) { _beamSize = beam; }
    void setPolicyFilename(const std::string &file) { _policyFilename = file; }
    void setLearning(const bool &learning) { _learning = learning; }

    void setTimeLimit(const size_t &timeLimit) { _timeLimit = timeLimit; }
    void setMaxChildren(const size_t &children) { _maxChildren = children; }
    void setMoveOrderingMethod(const size_t &method) { _moveOrdering = method; }
    void setEvalMethod(const IDType &eval) { _evalMethod = eval; }
    void setSimScripts(const IDType &p1, const IDType &p2)
    {
        _simScripts[0] = p1;
        _simScripts[1] = p2;
    }
    void setPlayerToMoveMethod(const IDType &method) { _playerToMoveMethod = method; }
    void setGraphVizFilename(const std::string &filename) { _graphVizFilename = filename; }
    void addOrderedMoveScript(const IDType &script) { _orderedMoveScripts.push_back(script); }
    void setPlayerModel(const IDType &player, const IDType &model) { _playerModel[player] = model; }

    std::vector<std::vector<std::string>> &getDescription()
    {
        if (_desc.size() == 0)
        {
            _desc.push_back(std::vector<std::string>());
            _desc.push_back(std::vector<std::string>());

            std::stringstream ss;

            _desc[0].push_back("Player Type:");
            _desc[0].push_back("Time Limit:");
            _desc[0].push_back("Max Children:");
            _desc[0].push_back("Move Ordering:");
            _desc[0].push_back("Player To Move:");
            _desc[0].push_back("Opponent Model:");

            ss << "AlphaBeta";
            _desc[1].push_back(ss.str());
            ss.str(std::string());
            ss << timeLimit() << "ms";
            _desc[1].push_back(ss.str());
            ss.str(std::string());
            ss << maxChildren();
            _desc[1].push_back(ss.str());
            ss.str(std::string());
            ss << MoveOrderMethod::getName(moveOrderingMethod());
            _desc[1].push_back(ss.str());
            ss.str(std::string());
            ss << PlayerToMove::getName(playerToMoveMethod());
            _desc[1].push_back(ss.str());
            ss.str(std::string());
            ss << PlayerModels::getName(playerModel((maxPlayer() + 1) % 2));
            _desc[1].push_back(ss.str());
            ss.str(std::string());
        }

        return _desc;
    }
};
