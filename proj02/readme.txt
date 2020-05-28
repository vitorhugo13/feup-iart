Reinforcement Learnig - Eximo


Bernardo Santos  201706534
João Matos       201705471
Vítor Gonçalves  201703917


Required packages:
    * colorama
    * stable-baselines
    * tensorflow 1.14

The eximo environment package must also be installed, for that execute the following commands:
    1. cd gym-eximo
    2. pip install -e .
    3. cd ..

To ease the training and testing of the models we created a couple of scripts:

 * training.py - used to train new agents
    * usage: python training.py <env> <model> <agent_name>
    * example: python training.py eximo-v3 ppo1 ppo1_v4

 * play.py - used to make a trained agent
    * all of the agents from which we collected the data present in the final report are in the models directory, 
    as well as all of the data, so the only thing needed to see the agents in action is running the command below
    * usage: python play.py <env> <model> <agent_name>
    * example: python play.py eximo-v3 ppo models/eximo-v3/ppo1_v0

Available environments:
 * eximo-v0
 * eximo-v2
 * eximo-v3
 * eximo-v4

Available models:
 * dqn
 * ppo1
 * acer
