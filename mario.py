from nes_py.wrappers import BinarySpaceToDiscreteSpaceEnv
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0')
env = BinarySpaceToDiscreteSpaceEnv(env, SIMPLE_MOVEMENT)
from statistics import median, mean
from collections import Counter
import numpy as np

LR = 1e-3
goal_steps = 500
score_requirement = 500
initial_games = 10

def initial_population():
	training_data=[]
	scores=[]
	accepted_scores=[]
	for episode in range(initial_games): #variable episode unused
		env.reset()
		#print("episode", episode)
		score=0
		game_memory=[]
		for move in range(goal_steps): #variable move unused
			# This will just create a sample action in any environment.
            # In this environment, the action can be 0 or 1, which is left or right
            #env.render()
			action=env.action_space.sample()
			# this executes the environment with an action, 
            # and returns the observation of the environment, 
            # the reward, if the env is over, and other info.
			observation, reward, done, info=env.step(action)
			game_memory.append([observation, action])
			score+=reward
			env.render()
			if done==True:
				break
		if score>=score_requirement:
			accepted_scores.append(score)
			for data in game_memory:
				training_data.append([data])
		scores.append(score)
	print('Average accepted score:', mean(accepted_scores))
	print(Counter(accepted_scores))
	training_data_save=np.array(training_data)
	np.save('saved.npy', training_data_save)
	return training_data

initial_population()