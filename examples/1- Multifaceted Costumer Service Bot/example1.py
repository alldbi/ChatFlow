from dotenv import load_dotenv
from bot.models.condition import Condition, Operator
from bot.models.node import NodeFactory
from bot.models.flow import Flow
from assets.prompts import *


load_dotenv()

if __name__ == "__main__":
    start_node = NodeFactory.create_node(prompt_template=decision_prompt,
                                         input_variables=['user_message'],
                                         output_variables={'technical': bool,
                                                           'sales': bool,
                                                           'advertisement': bool,
                                                           'chitchat': bool},
                                         return_inputs=True)

    adv_node = NodeFactory.create_node(prompt_template=advertisement_prompt,
                                       input_variables=['user_message'],
                                       output_variables='response',
                                       is_output=True)

    tech_node = NodeFactory.create_node(prompt_template=technical_prompt,
                                        input_variables=['user_message'],
                                        output_variables='response',)

    sales_node = NodeFactory.create_node(prompt_template=sales_prompt,
                                         input_variables=['user_message'],
                                         output_variables='response',
                                         is_output=True)

    chitchat_node = NodeFactory.create_node(prompt_template=chitchat_prompt,
                                            input_variables=['user_message'],
                                            output_variables='response',
                                            is_output=True)

    start_node.set_next_item({sales_node: Condition('sales', True, Operator.EQUALS),
                              adv_node: Condition('advertisement', True, Operator.EQUALS),
                              tech_node: Condition('technical', True, Operator.EQUALS),
                              chitchat_node: Condition('chitchat', True, Operator.EQUALS)})

    customer_service_flow = Flow(start_node=start_node)
    customer_service_flow.initialize()

    inp = {'user_message': "what is the company's name"}
    print(customer_service_flow.run(inp))
