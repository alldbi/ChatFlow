from bot.models.node import NodeFactory
from bot.models.condition import Condition, Operator
from bot.models.flow import Flow
import os
from dotenv import load_dotenv
from bot.models.state import State
from assets.prompts import *

load_dotenv()

if __name__ == "__main__":

    node_categorization = NodeFactory.create_node(prompt_template=prompt_categorization,
                                                  input_variables=['user_message'],
                                                  output_variables={'GeneralInquiry': bool,
                                                                    'NutritionInquiry': bool},
                                                  return_inputs=True)

    # ['Unnamed: 0', 'url_for_product', 'product_name', 'product_availability',
    #  'product_calories', 'product_price', 'have_sizes', 'Protein', 'Carbs',
    #  'Fat', 'Salt', 'Saturates', 'Sugars']
    metadata_cols = ['url_for_product', 'product_name']
    price_cols = ['product_name', 'product_price', 'product_availability', 'have_sizes']
    nutrition_cols = ['product_name', 'product_calories', 'have_sizes', 'Protein', 'Carbs', 'Fat', 'Salt', 'Saturates',
                      'Sugars']
    persist_directory = os.path.join(os.getcwd(), "McDonaldsPrice")
    docs_dir = os.path.join(os.getcwd(), "mcdonalds_dataset.csv")
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

    node_categorization.set_next_item({node_general_retrieval: Condition('GeneralInquiry', True, Operator.EQUALS),
                                       node_nutrition_retrieval: Condition('NutritionInquiry', True, Operator.EQUALS)})
    node_general_retrieval.set_next_item(node_general_qa)
    node_nutrition_retrieval.set_next_item(node_nutrition_qa)
    node_confirm_order.set_next_item({node_return_order: Condition('Finished', True, Operator.EQUALS),
                                      node_general_retrieval: Condition('ContinueOrder', True, Operator.EQUALS)})

    states = [State(name='GettingOrder',
                    definition="In this state, the McDonald’s Server and Specialist interact with the customer to take their order and answer costumer's general inquiries about meal prices or nutritional content.",
                    associated_node=node_categorization),
              State(name='ConfirmingOrder',
                    definition='The conversation only transitions to this state when the customer has finalized their order, confirmed it, and indicated that they have no additional requests. Typically, this transition occurs when the server inquires if the customer would like to order anything else or if they have completed their order, and the customer confirms that they have finished.',
                    associated_node=node_confirm_order)]

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
