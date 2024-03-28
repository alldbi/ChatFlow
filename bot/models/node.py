from typing import Dict, List, Set, Union
from enum import Enum

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel
from pydantic import create_model

from .flow_item import FlowItem



class JsonOutputNode(FlowItem):
    def __init__(self, model_name,
                 prompt_template: str, 
                 input_variables:List[str], 
                 output_variables: Dict[str, type],
                 temperature: float = 0.1,
                 max_tokens: int = 400,
                 verbose: bool = False,
                 return_inputs: bool = False,
                 is_output: bool = False
                 ) -> None:
        """

        input_variables: a list of input variable names
        output_variables: a dictionary with variable names keys and variable types values
                {'a':int, 'b':str}
        """
        self.template = prompt_template
        self.input_variables: List[str] = input_variables
        self.output_variables: Dict[str, type] = output_variables
        self.return_inputs = return_inputs
        self.is_output = is_output

        self.parser = self._get_output_parser()

        llm = ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens, verbose=verbose)
        self.model = llm.with_structured_output(
                    self._get_output_model(),
                    method="json_mode",
                    include_raw=True
                )
        
        self.prompt = PromptTemplate(template=self.template
                                     ,input_variables=self.input_variables
                                    #  ,partial_variables={"format_instructions": self.parser.get_format_instructions()}
                                     )
        # self.chain = self.prompt | self.model | self.parser
        self.chain = self.prompt | self.model
    
    
    def run(self, inp: Dict):
        # TODO run the prompt and generate output
        try:
            output = self.chain.invoke(input=inp)['parsed']
        except Exception as e:
            print(e)
            output = {k: None for k in self.output_variables}
        
        if self.return_inputs:
            return output.update(self.input_variables)
        
        return output

    def _get_output_model(self):
        output_model = create_model('OutputModel', **{k: (v, ...) for k, v in self.output_variables.items()})
        return output_model
    
    def _get_output_parser(self) -> JsonOutputParser:
        parser = JsonOutputParser()
        output_model = self._get_output_model()
        parser.pydantic_object = output_model
        return parser
    

class StrOutputNode(FlowItem):
    def __init__(self, model_name,
                 prompt_template: str, 
                 input_variables:List[str], 
                 output_variable: str,
                 temperature: float = 0.1,
                 max_tokens: int = 400,
                 verbose: bool = False,
                 return_inputs: bool = False,
                 is_output: bool = False
                 ) -> None:
        """

        input_variables: a list of input variable names
        output_variable: a string that is the name of the output string
        """
        self.template = prompt_template
        self.input_variables: List[str] = input_variables
        self.output_variable: str = output_variable
        self.return_inputs = return_inputs
        self.is_output = is_output

        self.parser = self._get_output_parser()

        self.model = ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens, verbose=verbose)
        
        self.prompt = PromptTemplate(template=self.template
                                     ,input_variables=self.input_variables
                                     )
        # self.chain = self.prompt | self.model | self.parser
        self.chain = self.prompt | self.model
        
    
    def run(self, inp: Dict):
        # TODO run the prompt and generate output
        try:
            output = {self.output_variable: self.chain.invoke(input=inp).content}
        except Exception as e:
            print(e)
            output = {self.output_variable: None}
        if self.return_inputs:
            return output.update(self.input_variables)
        return output
    
    def _get_output_parser(self) -> StrOutputParser:
        return StrOutputParser

class RetrievalJsonOutputNode(JsonOutputNode):
    def __init__(self, model_name, 
                 prompt_template: str, 
                 input_variables: List[str], 
                 output_variables: Dict[str, type], 
                 temperature: float = 0.1, 
                 max_tokens: int = 400, 
                 verbose: bool = False, 
                 return_inputs: bool = False,
                 is_output: bool = False) -> None:
        super().__init__(model_name, prompt_template, input_variables, output_variables, temperature, max_tokens, verbose, return_inputs, is_output)

class RetrievalStrOutputNode(StrOutputNode):
    def __init__(self, model_name, 
                 prompt_template: str, 
                 input_variables: List[str], 
                 output_variable: str, 
                 temperature: float = 0.1, 
                 max_tokens: int = 400, 
                 verbose: bool = False, 
                 return_inputs: bool = False,
                 is_output: bool = False) -> None:
        super().__init__(model_name, prompt_template, input_variables, output_variable, temperature, max_tokens, verbose, return_inputs, is_output)

# class DecisionNode(JsonOutputNode):
#     def __init__(self, id,  prompt, input_variables, output_variables) -> None:
#         super().__init__(id)
        
#     def next_node(self):
#         # TODO run the prompt to select one of the output ids
#         output_id = ""
#         return output_id
    
#     def output(self, inp: Dict):
#         return inp
    





# def node_factory(json_node):
#     """
#     returns a node
#     """
#     prompt = json_node["prompt"]
#     input_variables = json_node["input_variables"]
#     output_variables = json_node["output_variables"]
#     next_nodes = json_node["next_nodes"]
#     output_node_ids = json_node[""]
#     if json_node['is_decision']:
#         # make a decision node TODO
#         pass
#     else:
#         # make a normal node TODO
#         pass
