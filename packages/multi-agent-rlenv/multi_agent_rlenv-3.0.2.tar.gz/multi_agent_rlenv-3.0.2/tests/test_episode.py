from typing import Any
import numpy as np
from marlenv.models import Transition, Episode, MARLEnv
from marlenv import wrappers, DiscreteMockEnv


def generate_episode(env: MARLEnv[Any, Any], with_probs: bool = False) -> Episode:
    obs, state = env.reset()
    episode = Episode.new(obs, state)
    while not episode.is_finished:
        action = env.action_space.sample()
        probs = None
        if with_probs:
            probs = np.random.random(action.shape)
        step = env.step(action)
        episode.add(Transition.from_step(obs, state, action, step, action_probs=probs))
        obs = step.obs
        state = step.state
    return episode


def test_episode_builder_is_done():
    env = DiscreteMockEnv(2)
    obs, state = env.reset()
    # Set the 'done' flag
    builder = Episode.new(obs, state)
    assert not builder.is_finished
    builder.add(Transition(obs, state, [0, 0], [0], False, {}, obs, state, False))
    assert not builder.is_finished
    builder.add(Transition(obs, state, [0, 0], [0], True, {}, obs, state, False))
    assert builder.is_finished

    # Set the 'truncated' flag
    builder = Episode.new(obs, state)
    assert not builder.is_finished
    builder.add(Transition(obs, state, [0, 0], 0, False, {}, obs, state, False))
    assert not builder.is_finished
    builder.add(Transition(obs, state, [0, 0], 0, False, {}, obs, state, True))
    assert builder.is_finished


def test_returns():
    obs, state = DiscreteMockEnv(2).reset()
    episode = Episode.new(obs, state)
    n_steps = 20
    gamma = 0.95
    rewards = []
    for i in range(n_steps):
        done = i == n_steps - 1
        r = np.random.rand(5).astype(np.float32)
        rewards.append(r)
        t = Transition(obs, state, [0, 0], r, done, {}, obs, state, False)
        episode.add(t)
    rewards = np.array(rewards, dtype=np.float32)
    returns = episode.compute_returns(discount=gamma)
    for i, r in enumerate(returns):
        G_t = rewards[-1]
        for j in range(len(rewards) - 2, i - 1, -1):
            G_t = rewards[j] + gamma * G_t
        assert all(abs(r - G_t) < 1e-6)


def test_dones_not_set_when_truncated():
    END_GAME = 10
    # The time limit issues a 'truncated' flag at t=10 but the episode should not be done
    env = wrappers.TimeLimit(DiscreteMockEnv(2, end_game=END_GAME), END_GAME - 1, add_extra=False)
    episode = generate_episode(env)
    # The episode sould be truncated but not done
    assert np.all(episode.dones == 0)
    padded = episode.padded(END_GAME * 2)
    assert np.all(padded.dones == 0)


def test_done_when_time_limit_reached_with_extras():
    END_GAME = 10
    env = wrappers.TimeLimit(DiscreteMockEnv(2, end_game=END_GAME), END_GAME - 1, add_extra=True)
    episode = generate_episode(env)
    # The episode sould be truncated but not done
    assert episode.dones[-1] == 1.0
    padded = episode.padded(END_GAME * 2)
    assert np.all(padded.dones[len(episode) - 1 :] == 1)


def test_dones_set_with_paddings():
    # The time limit issues a 'truncated' flag at t=10 but the episode should not be done
    END_GAME = 1
    env = DiscreteMockEnv(2, end_game=END_GAME)
    episode = generate_episode(env)
    # The episode sould be truncated but not done
    assert np.all(episode.dones[:-1] == 0)
    assert episode.dones[-1] == 1
    padded = episode.padded(END_GAME * 2)
    assert np.all(padded.dones[: END_GAME - 1] == 0)
    assert np.all(padded.dones[END_GAME - 1 :] == 1)


def test_masks():
    env = wrappers.TimeLimit(DiscreteMockEnv(2), 10)
    episode = generate_episode(env)
    assert np.all(episode.mask == 1)
    padded = episode.padded(25)
    assert np.all(padded.mask[:10] == 1)
    assert np.all(padded.mask[10:] == 0)


def test_padded_raises_error_with_too_small_size():
    env = DiscreteMockEnv(2)
    episode = generate_episode(env)
    try:
        episode.padded(1)
        assert False
    except ValueError:
        pass


def test_padded():
    env = wrappers.TimeLimit(DiscreteMockEnv(2), 10, add_extra=False)

    for i in range(5, 11):
        env.step_limit = i
        episode = generate_episode(env)
        assert len(episode) == i
        padded = episode.padded(10)
        assert len(padded._observations) == 11
        assert len(padded.obs) == 10
        assert len(padded.next_obs) == 10
        assert len(padded.actions) == 10
        assert len(padded.rewards) == 10
        assert len(padded.dones) == 10
        assert len(padded.extras) == 10
        assert len(padded.next_extras) == 10
        assert len(padded.available_actions) == 10
        assert len(padded.next_available_actions) == 10
        assert len(padded.mask) == 10


def test_retrieve_episode_transitions():
    env = wrappers.TimeLimit(DiscreteMockEnv(2), 10, add_extra=False)
    episode = generate_episode(env)
    transitions = list(episode.transitions())
    assert len(transitions) == 10
    assert all(not t.done for t in transitions)
    assert all(not t.truncated for t in transitions[:-1])
    assert transitions[-1].truncated


def test_iterate_on_episode():
    env = wrappers.TimeLimit(DiscreteMockEnv(2), 10, add_extra=False)
    episode = generate_episode(env)
    for i, t in enumerate(episode):  # type: ignore
        assert not t.done
        if i == 9:
            assert t.truncated
        else:
            assert not t.truncated


def test_episode_with_logprobs():
    env = wrappers.TimeLimit(DiscreteMockEnv(2), 10, add_extra=False)
    episode = generate_episode(env, with_probs=True)
    action_probs = episode["action_probs"]
    assert action_probs is not None
    assert len(action_probs) == 10
