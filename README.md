# Trans-America
We implimented a perfect information Trans America game (you know where your opponent's cities are)
and 2 AI's that can play it
* mcts
* minTotalAI

The mcts is fairly similar to the one we wrote for connect 4, but uses a better version of UCB selection which
replaces the ln with another sqrt as sugested in Regulation of Exploration for Simple Regret
Minimization in Monte-Carlo Tree Search (doi, 10.1.1.707.6512)
We also add First Play Urgency (FPU), and Progressive Bias (A Survey of Monte Carlo Tree Search Methods DOI: 10.1109/TCIAIG.2012.2186810)
Both of these narrow the effective search, FPU by allowing us to sometimes not go to bad uninitialized children first,
and Progressive Bias, by allowing some domain knowledge (being close to connected is good) to tilt the node selection.

