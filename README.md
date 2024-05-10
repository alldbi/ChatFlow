# ChatFlow Framework
Automate chatbot development with ease using this framework. Create a chatbot by defining nodes and connecting them using conditions. Develop a chatbot in minutes with this intuitive framework.

## Overview
This framework simplifies chatbot development by allowing users to create nodes and connect them to form workflows. It supports various output formats and retrieval nodes, with the ability to define custom nodes. (#TODO)

## Comparison with Agents
LLM-Agents are ...
This framework advantages:  (#TODO)
1   efficiency in terms of number of consumed tokens, 
2   less execution time
3-  more reliable (restricted or predefined planning)

## Installation
<!-- todo -->
<not ready for installation>
To install the framework, simply run:(#TODO)
<!-- Make a copy of '.env.example' file and name it '.env'. Change the value of the variables.<br> -->
<!-- Check 'test-bot.ipynb' in tests directory to get familiar with the library usage. -->

## Modules
*   Node: nodes are execution units of workflows. They receive inputs, process them, and return results in custom format. odes can be executed independently without being a part of a flow. There are multiple Node types with different internal logics:
    *   String Output Node: if output_variables parameter in node factory be a string, a String Output Node will be generated
        ```
        from bot.models.node import NodeFactory
        node = NodeFactory.create_node(prompt_template=advertisement_prompt, 
                                   input_variables=['user_message'],
                                   output_variables='response',
                                   is_output=True, model_name=model_name)
        ```
    *   Json Output Node: to create a json output node, a dictionary containing the variable names and types must be passed as output_variables to the NodeFactory.
        ```
        node = NodeFactory.create_node(prompt_template=decision_prompt, 
                                       input_variables=['user_message'], 
                                       output_variables={'technical':bool, 
                                                       'sales':bool, 
                                                       'advertisement':bool,
                                                       'chitchat': bool},
                                       return_inputs=True, model_name=model_name)
        ```
    *   Retrieval Node: these nodes retrieve data from pdf, csv, and database
        ```
        node = NodeFactory.create_retrieval(prompt_template= prompt_template, 
                                            input_variables=['query'], 
                                            output_variables='response',
                                            persist_directory=persist_directory,
                                            collection_name='test-retrieval',
                                            docs_dir=docs_dir,
                                            context_var='context',
                                            query_var= 'query',
                                            k_result= 3,
                                            return_inputs= True,
                                            is_output= True, 
                                            model_name=model_name)
        ```
    <!-- *   Custom Node -->
*   Condition: conditions are rules that facilitate routing in flow of the chatbot
    ```
    from bot.models.condition import Condition, Operator
    # if the value of 'sales' variable in the start_node outputs be equal to 'True', 
    # sales_node will be the next node in the flow
    start_node.set_next_item({sales_node: Condition('sales', True, Operator.EQUALS),
                          adv_node: Condition('advertisement', True, Operator.EQUALS),
                          tech_node: Condition('technical', True, Operator.EQUALS),
                          chitchat_node: Condition('chitchat', True, Operator.EQUALS)})
    ```
*   State: each state has a name, definition and an associated node. Based on the definition of each state, flow decides a state to resume execution. 
    ```
    state = State(name='chitchat', 
                  definition='in this state counselor will start the conversation with a chitchat and greets the client. counselor can stay as many steps as needed in this state. next state is rapport building.', 
                  associated_node=chitchat_node)
    ```
*   Flow: this module is the final workflow of the chatbot and is responsible for running all blocks together and pass each modules's output to the next one. Setting ```debug=True``` will print the execution log of each node. 
    ```
    from bot.models.flow import Flow
    
    flow = Flow(start_node=start_node, debug=True)
    ```
    ```
    flow = Flow(states=states, start_state=start_state, model_name=model_name, debug=True)
    ```

## Customization

## Examples
These are example usages of the framework:
*   [Simple Customer Service Bot](examples/1-MultifacetedCostumerServiceBot/README.md)
*   [ChatBot with Retrieval Node](examples/2-ScientificPaperQABot/README.md)
*   [ChatBot with SQL Retrieval Node](examples/3-CostumerRecord&PolicyBot/README.md)
*   [English Learning Chatbot](examples/5-EnglishTeacherBot/README.md)
*   [Multi-State Restaurant Order Bot](examples/6-McDonaldServer&NutritionistBot/)

## Contributing

## Version History
current version: v1.0-20240510 (initial version)

