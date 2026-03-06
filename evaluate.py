"""Evaluate a saved TAMER model.

Runs a small rendered demo, then a larger headless evaluation.
"""

import argparse

import gym

from tamer.agent import Tamer


def make_env(render: bool):
    if render:
        try:
            return gym.make('MountainCar-v0', render_mode='human')
        except TypeError:
            # Older Gym versions do not support render_mode at make-time.
            return gym.make('MountainCar-v0')
    return gym.make('MountainCar-v0')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='autosave', help='Model filename stem in tamer/saved_models')
    parser.add_argument('--num-examples', type=int, default=3, help='Rendered examples to show before evaluation')
    parser.add_argument('--num-eval', type=int, default=100, help='Headless episodes for evaluation')
    args = parser.parse_args()

    # Rendered examples.
    if args.num_examples > 0:
        demo_env = make_env(render=True)
        demo_agent = Tamer(
            demo_env,
            num_episodes=1,
            discount_factor=1,
            epsilon=0,
            min_eps=0,
            tame=True,
            ts_len=0.0,
            model_file_to_load=args.model,
        )
        demo_agent.play(n_episodes=args.num_examples, render=True)

    # Headless evaluation.
    eval_env = make_env(render=False)
    eval_agent = Tamer(
        eval_env,
        num_episodes=1,
        discount_factor=1,
        epsilon=0,
        min_eps=0,
        tame=True,
        ts_len=0.0,
        model_file_to_load=args.model,
    )
    eval_agent.evaluate(n_episodes=args.num_eval)


if __name__ == '__main__':
    main()
