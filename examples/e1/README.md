# Example 1: ChatFlow Framework for a Simple Chatbot

This example demonstrates the usage of the ChatFlow framework for creating a simple chatbot.

## Scenario

Assume that we need a customer service chatbot for a company called Pinnacle Auto Group. The content for the information about the company is separated into three categories: 'sales', 'advertisement', and 'technical'. The chatbot receives the user's input and answers their inquiries.

To create the chatbot, we first need to design its workflow. The chatbot's workflow depends on its usage. In this example, we design the workflow as follows:

The chatbot should have four faces. For each category of the given data, a different bot with its specific prompt will be assigned, as well as a face to handle the user's chitchats. To decide which bot should respond to the user's message, a "condition" node will be defined to make the decision.

## How to Use

First, we need to prepare the information contents related to each category:

```python
marketing_policy = """..."""
sales_policy = """..."""
technical_policy = """..."""
```

As mentioned, the first element must be the decision node, so we prepare its prompt as well as initiating the node.
```python
decision_prompt = f"""Categorize the user message into one of the following categories:
1. technical
2. sales
3. advertisement
4. chitchat

<< USER MESSAGE >>
{user_message}

<< RULES >>
1- Put your answer in JSON format.
2- The output is a JSON object where the value of the input message category is TRUE, and other output keys are FALSE
"""

start_node = NodeFactory.create_node(model_name=model_name,
                                     prompt_template=decision_prompt,
                                     input_variables=['user_message'],
                                     output_variables={'technical': bool,
                                                       'sales': bool,
                                                       'advertisement': bool,
                                                       'chitchat': bool},
                                     return_inputs=True)
```
Then, for each category, we initiate the sub-chatbot within their prompts.
```python
advertisement_prompt = f"""You are a customer service chatbot. Answer the questions based on the provided policies.

<< ADVERTISEMENT QUESTIONS >>
{marketing_policy}


<< USER MESSAGE >>
""" + """{user_message}
BOT RESPONSE:"""
adv_node = NodeFactory.create_node(model_name=model_name,
                                   prompt_template=advertisement_prompt,
                                   input_variables=['user_message'],
                                   output_variables='response',
                                   is_output=True)

technical_prompt = """..."""
tech_node = NodeFactory.create_node(model_name=model_name,
                                    prompt_template=technical_prompt,
                                    input_variables=['user_message'],
                                    output_variables='response',
                                    is_output=True)
sales_prompt = """..."""
sales_node = NodeFactory.create_node(model_name=model_name,
                                     prompt_template=sales_prompt,
                                     input_variables=['user_message'],
                                     output_variables='response',
                                     is_output=True)
chitchat_prompt = """..."""
chitchat_node = NodeFactory.create_node(model_name=model_name,
                                        prompt_template=chitchat_prompt,
                                        input_variables=['user_message'],
                                        output_variables='response',
                                        is_output=True)
```

Now we have to define the chain of workflow of the chatbot. We are going to define that after deciding which category the user's message was, pass the message to the corresponding sub-chatbot.

```python
start_node.set_next_item({sales_node: Condition('sales', True, Operator.EQUALS),
                          adv_node: Condition('advertisement', True, Operator.EQUALS),
                          tech_node: Condition('technical', True, Operator.EQUALS),
                          chitchat_node: Condition('chitchat', True, Operator.EQUALS)})
```
After setting up everything, we are going to create the main chatbot's object, and we can pass messages to it.
```python
customer_service_flow = Flow(start_node=start_node)

inp = {'user_message': "what is the company's name"}
print(customer_service_flow.run(inp))
```



## Workflow Diagram
![Image Alt Text](./assets/diagram.png)
