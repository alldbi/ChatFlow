def state_updater_prompt():
    prompt_template = """History of a chat is provided.
Choose the next state based on the state definitions. 
Set name of the state that is the best matched for next state to true.
Set all of the other states to false.
return output in json format.

<< CHAT HISTORY >>
{history}

<< CURRENT STATE >>
{current_state}


"""
    return prompt_template