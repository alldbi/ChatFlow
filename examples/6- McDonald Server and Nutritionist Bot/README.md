# Example 6
# McDonald's Server Bot

This guide will walk you through the process of using the ChatFlow framework to create a McDonald's server chatbot. This chatbot accesses a csv file containing prices and nutrition values of foods.

## Scenario

The chatbot is consists of two `States`. One for taking the costumer's order and answering to their inquiries, and the other to give the costumer their final recept. 

The first `State` has two phases, one accesses the meal availabilities and the other accesses the nutritional information. 

Note that this example is about to show you how you can work with states and different phases of a chatbot. In production or real world problem this scenario could be implemented using simpler and less complicated workflow.

## Workflow Diagram
![Image Alt Text](./assets/diagram.PNG)

## Setup

Before you start, import the necessary modules and load the environment variables from the .env file.

```python
from dotenv import load_dotenv
from bot.models.condition import Condition, Operator
from bot.models.node import NodeFactory
from bot.models.flow import Flow
from assets.prompts import *


load_dotenv()
```

## Building the Chatbot

First create the nodes and workflow of the first state. for that a decision node must be implemented.

```python

node_categorization = NodeFactory.create_node(prompt_template=prompt_categorization,
                                              input_variables=['user_message'],
                                              output_variables={'GeneralInquiry': bool,
                                                                'NutritionInquiry': bool},
                                              return_inputs=True)
```

Next, define which columns of your data each phases of the first state should access.
```python
metadata_cols = ['url_for_product', 'product_name']
price_cols = ['product_name', 'product_price', 'product_availability', 'have_sizes']
nutrition_cols = ['product_name', 'product_calories', 'have_sizes', 'Protein', 'Carbs', 'Fat', 'Salt', 'Saturates',
                  'Sugars']
persist_directory = os.path.join(os.getcwd(), "McDonaldsPrice")
docs_dir = os.path.join(os.getcwd(), "mcdonalds_dataset.csv")
```


Now create the nodes for handling interaction with the user

```python
node_general_retrieval = NodeFactory.create_retrieval(input_variables=['user_message'],
                                                      output_variables='context',
                                                      persist_directory=persist_directory,
                                                      collection_name='food-price',
                                                      content_cols=price_cols,
                                                      metadata_cols=metadata_cols,
                                                      docs_dir=docs_dir,
                                                      k_result=10,
                                                      return_inputs=True)

node_general_qa = NodeFactory.create_node(prompt_template=prompt_price_retrieval,
                                          input_variables=['user_message', 'context'],
                                          output_variables='response',
                                          history_variables=['user_message', 'response'],
                                          is_output=True)

# persist_directory = os.path.join(os.getcwd(), "McDonaldsNutrition")
# docs_dir = os.path.join(os.getcwd(), "mcdonalds_dataset.csv")
node_nutrition_retrieval = NodeFactory.create_retrieval(input_variables=['user_message'],
                                                        output_variables='context',
                                                        persist_directory=persist_directory,
                                                        collection_name='food-nutrition',
                                                        content_cols=nutrition_cols,
                                                        metadata_cols=metadata_cols,
                                                        docs_dir=docs_dir,
                                                        k_result=4,
                                                        return_inputs=True)

node_nutrition_qa = NodeFactory.create_node(prompt_template=prompt_price_retrieval,
                                            input_variables=['user_message', 'context'],
                                            output_variables='response',
                                            history_variables=['user_message', 'response'],
                                            is_output=True)
```

Now the second state must be implemented. this state first checks the history of chat and decides wheather the user's order is finished. If it was, the other node looks up the history of chat and returns the reciept.

```python
node_confirm_order = NodeFactory.create_node(prompt_template=prompt_confirm_order,
                                             input_variables=['history'],
                                             output_variables={'Finished': bool,
                                                               'ContinueOrder': bool},
                                             history_variables=['user_message', 'response'],
                                             history_count=2,
                                             return_inputs=True)

node_return_order = NodeFactory.create_node(prompt_template=prompt_return_order,
                                            input_variables=['history'],
                                            output_variables='response',
                                            history_variables=['user_message', 'response'],
                                            return_inputs=True,
                                            is_output=True)
```

build up the workflow of your chatbot
```python
node_categorization.set_next_item({node_general_retrieval: Condition('GeneralInquiry', True, Operator.EQUALS),
                                   node_nutrition_retrieval: Condition('NutritionInquiry', True, Operator.EQUALS)})
node_general_retrieval.set_next_item(node_general_qa)
node_nutrition_retrieval.set_next_item(node_nutrition_qa)
node_confirm_order.set_next_item({node_return_order: Condition('Finished', True, Operator.EQUALS),
                                  node_general_retrieval: Condition('ContinueOrder', True, Operator.EQUALS)})
```

Now the states must be created. Each state has it's specific definition and it must be defined properly to avoid the transition mistakes. Also the start node of each state must be passed to them.
```python
states = [State(name='GettingOrder',
            definition="In this state, the McDonald’s Server and Specialist interact with the customer to take their order and answer costumer's general inquiries about meal prices or nutritional content.",
            associated_node=node_categorization),
      State(name='ConfirmingOrder',
            definition='The conversation only transitions to this state when the customer has finalized their order, confirmed it, and indicated that they have no additional requests. Typically, this transition occurs when the server inquires if the customer would like to order anything else or if they have completed their order, and the customer confirms that they have finished.',
            associated_node=node_confirm_order)]
```

After setting up everything, create the main chatbot object and initialize it. You can now pass messages to it.

```python
flow_bot = Flow(states=states, start_state=states[0])
flow_bot.initialize()

while True:
    query = input("User:  ")
    if query == "exit":
        break
    inp = {'user_message': query}
    answer = flow_bot.run(inp)
    print("____________________Bot Answer___________________________")
    print(answer['response'])
    print("__________________________________________________________")
```
