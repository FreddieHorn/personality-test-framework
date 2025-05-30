import json
import pandas as pd
from prompts import generate_interaction_prompt, agent_prompt, goal_completion_rate_prompt
from logging import getLogger
log = getLogger(__name__)

def generate_interaction(input_csv: str, output_csv: str, model, tokenizer, mode = "default"):
    log.info("_______GENERATING INTERACTION____________")
    data = pd.read_csv(input_csv)
    # Process rows
    if mode == "default":
        results = []
        # 1 pos - first agent goal, 2 pos - second agent goal, 3 pos - shared goal
        for _, row in data.iterrows():
            interaction = ""
            agent_1_name = row["Character1"]
            agent_2_name = row["Character2"]
            shared_goal=row["shared_goal"]
            first_agent_goal=row["first_agent_goal"]
            second_agent_goal=row["second_agent_goal"]
            scenario=row["scenario"]
            personality1=row["Personality1"]
            personality2=row["Personality2"]
            setting = row["Setting"]

            for i in range(1, 21, 2):
                response = agent_prompt(agent_1_name, scenario, setting, 
                shared_goal, first_agent_goal, personality1, interaction, model = model, tokenizer = tokenizer, turn = i-1)
                interaction+=f"{agent_1_name}:{response['response']}\n"
                response = agent_prompt(agent_2_name, scenario, setting, 
                shared_goal, second_agent_goal, personality2, interaction, model = model, tokenizer = tokenizer, turn = i)
                interaction+=f"{agent_2_name}:{response['response']}\n"

            results.append(interaction)
            log.info(interaction)
        data["interaction"] = results
    elif mode == "script":
        results = []
        # 1 pos - first agent goal, 2 pos - second agent goal, 3 pos - shared goal
        for _, row in data.iterrows():
            interaction = ""
            agent_1_name = row["Character1"]
            agent_2_name = row["Character2"]
            shared_goal=row["shared_goal"]
            first_agent_goal=row["first_agent_goal"]
            second_agent_goal=row["second_agent_goal"]
            scenario=row["scenario"]
            personality1=row["Personality1"]
            personality2=row["Personality2"]
            setting = row["Setting"]
            topic = row["Topic"]

            result = generate_interaction_prompt(agent_1_name, agent_2_name, shared_goal, first_agent_goal, second_agent_goal, scenario, personality1, personality2,
                                                 setting, topic, model, tokenizer)

            results.append(result)
        data["interaction"] = [result.get("interaction", "") for result in results]
     # Save results
    
    data.to_csv(output_csv, index=False)
    log.info(f"Results saved to {output_csv}")