import sys

if __name__ == "__main__":
    import gym

    from gym_tafl.agents.play import Runner
    from gym_tafl.agents.human_agent_with_rules import HumanAgentWithRules
    from gym_tafl.agents.mcts_agent_with_rules import MctsAgentWithRules

    variant = "Brandubh" if len(sys.argv) < 2 else sys.argv[1]

    env = gym.make("gym_tafl:tafl-v0", variant=variant)

    agents = [
        MctsAgentWithRules(env.action_space),
        HumanAgentWithRules(env.action_space),
    ]

    Runner(env, agents).run()
