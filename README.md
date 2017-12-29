This repository contains algorithms to play pacman.

SearchAgent: Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficienly. We implemented search strategies like Depth-first search, Breadth-first search, Uniform-cost search and A-star search, and built cornerHeuristic (getting to all the corners efficiently), foodHeuristic (eating as much food as possible), and findPathToClosestDot to solve the problem suboptimally.

MultiAgentPacman: We designed Adversarial Search agents for the classic version of Pacman including ghosts. We implemented minimax and expectimax search, alpha-beta pruning, and built evaluation functions to evaluate states rather than actions.

SolvingMDPs: In this project, we implemented value iteration and Q-learning to solve MDPs (Markov Decision Processes). The value iteration agent is an offline planner which arrives at a complete policy before ever interacting with the real environment. The Q-learning agent, in contrast, learns by trial and error from interactions with the environment. We implemented epsilon-greedy action selection in the Q-learning agent and developed a crawler robot which learned how to walk using Q-learning. We also implemented an approximate Q-learning agent that learns weights for features of states.

InferenceAndParticleFiltering: This time, the ghosts are invisible. We designed pacman agents that use sensors to locate and eat invisible ghosts. We advanced from locating single, stationary ghosts to hunting packs of multiple moving ghosts with ruthless efficiency. We used Exact Inference and Approximate Inference (Particle Filtering) to achieve this.

MultiPlayerContest: This project involves a multi-player capture-the-flag variant of pacman where agents conttrol both pacman and ghosts in coordinated team-based strategies. The aim was to try to eat the food on the far side of the map (enemy territory) while defending the food on our home side.
