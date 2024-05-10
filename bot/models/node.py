import os

from typing import Dict, List, Set, Union, Any
from enum import Enum

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
import pandas as pd

import sqlite3
from pydantic import BaseModel
from pydantic import create_model

from .flow_item import FlowItem
from .condition import Condition
from .state import State
from .memory import Memory
from ..prompts.state_prompts import state_updater_prompt


class Node(FlowItem):
    def __init__(self, input_variables: List[str],
                 output_variables: Union[Dict[str, type], str],
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None] = None,
                 **kwargs: Any) -> None:
        self.input_variables: List[str] = input_variables
        self.output_variables: str = output_variables
        self.next: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition]] = next_item
        self.model_name = kwargs.get('model_name', None)
        self.temperature = kwargs.get('temperature', 0.1)
        self.max_tokens = kwargs.get('max_tokens', 400)
        self.verbose = kwargs.get('verbose', True)
        self.return_inputs = kwargs.get('return_inputs', False)
        self.is_output = kwargs.get('is_output', False)
        self.history_key = kwargs.get('history_key', 'history')
        self.history_variables = kwargs.get('history_variables', None)
        self.history_count = kwargs.get('history_count', 10)

    def set_next_item(self, next: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition]]) -> None:
        self.next = next
    
    def get_next_item(self):
        return self.next
    
    def initialize(self, **kwargs):
        raise NotImplementedError("This method must be implemented before access!")


class Creative_Node(FlowItem):

# Only temperature was increased

    def __init__(self, model_name,
                 prompt_template: str, 
                 input_variables:List[str], 
                 output_variables: Union[Dict[str, type], str],
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None,
                 temperature: float = 0.9,
                 max_tokens: int = 400,
                 verbose: bool = False,
                 return_inputs: bool = False,
                 is_output: bool = False) -> None:
        self.template = prompt_template
        self.input_variables: List[str] = input_variables
        self.output_variables: str = output_variables
        self.next: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition]] = next_item
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.return_inputs = return_inputs
        self.is_output = is_output
        self.verbose = verbose

    def set_next_item(self, next: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition]])-> None:
        self.next = next
    
    def get_next_item(self):
        return self.next


class JsonOutputNode(Node):
    def __init__(self, prompt_template: str, 
                 input_variables: List[str],
                 output_variables: Dict[str, type],
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None,
                 **kwargs: Any
                 ) -> None:
        """

        input_variables: a list of input variable names
        output_variables: a dictionary with variable names keys and variable types values
                {'a':int, 'b':str}
        """
        super().__init__(input_variables=input_variables,
                         output_variables=output_variables, 
                         next_item=next_item, 
                         **kwargs)
        self.template = prompt_template
        self.parser = self._get_output_parser()

    
    def initialize(self, **kwargs):
        try:
            model_name = self.model_name if self.model_name is not None else kwargs.get('model_name')
        except:
            # TODO implement debugging system
            ValueError("model name is not defined! you must define model_name when you create the node or when you initialize it!")

        llm = ChatOpenAI(model_name=model_name, temperature=self.temperature, max_tokens=self.max_tokens, verbose=self.verbose)
        # https://platform.openai.com/docs/guides/text-generation/json-mode
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
    

    def run(self, inp: Dict, memory: Union[Memory, None]=None):
        if memory is not None:
            # TODO add a method to read the related parts of the history and save them in its associated node. 
            # TODO debug and change the logic of getting input and returning it as output
            inp[self.history_key] = memory.get_history_str(self.history_variables, count=self.history_count)
        try:
            output = self.chain.invoke(input=inp)['parsed']
        except Exception as e:
            print(e)
            output = {k: None for k in self.output_variables}
        
        if self.return_inputs:
            output.update(inp)
            return output
        
        if memory is not None:
            # TODO save output in memory if needed
            pass
        
        return output

    def _get_output_model(self):
        output_model = create_model('OutputModel', **{k: (v, ...) for k, v in self.output_variables.items()})
        return output_model
    
    def _get_output_parser(self) -> JsonOutputParser:
        parser = JsonOutputParser()
        output_model = self._get_output_model()
        parser.pydantic_object = output_model
        return parser


class StrOutputNode(Node):
    def __init__(self, prompt_template: str, 
                 input_variables:List[str], 
                 output_variables: str,
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None,
                 **kwargs: Any
                 ) -> None:
        """

        input_variables: a list of input variable names
        output_variable: a string that is the name of the output string
        """
        super().__init__(input_variables=input_variables,
                         output_variables=output_variables, 
                         next_item=next_item, 
                         **kwargs)
        self.template = prompt_template
        self.parser = self._get_output_parser()
        
    def initialize(self, **kwargs):
        try:
            model_name = self.model_name if self.model_name is not None else kwargs.get('model_name')
        except:
            # TODO implement debugging system
            ValueError("model name is not defined! you must define model_name when you create the node or when you initialize it!")

        self.model = ChatOpenAI(model_name=model_name, temperature=self.temperature, max_tokens=self.max_tokens, verbose=self.verbose)
        
        self.prompt = PromptTemplate(template=self.template
                                     ,input_variables=self.input_variables
                                     )
        # self.chain = self.prompt | self.model | self.parser
        self.chain = self.prompt | self.model

    def run(self, inp: Dict, memory: Union[Memory, None]=None):
        if memory is not None:
            # TODO add a method to read the related parts of the history and save them in its associated node. 
            # TODO debug and change the logic of getting input and returning it as output
            inp[self.history_key] = memory.get_history_str(self.history_variables, count=self.history_count)
        try:
            output = {self.output_variables: self.chain.invoke(input=inp).content}
        except Exception as e:
            print(e)
            output = {self.output_variables: None}
        if self.return_inputs:
            output.update(inp)
        
        if memory is not None:
            # TODO save output in memory if needed
            pass

        return output
    
    def _get_output_parser(self) -> StrOutputParser:
        return StrOutputParser


class RetrievalNode(Node):
    def __init__(self, input_variables: List[str],
                 output_variables: Union[str, Dict[str, type]],
                 persist_directory: str,
                 collection_name: str,
                 docs_dir: str,
                 k_result: int = 1,
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None, 
                 **kwargs: Any
                 ) -> None:
        super().__init__(input_variables=input_variables,
                         output_variables=output_variables, 
                         next_item=next_item,
                         **kwargs)
        # self.node: Union[StrOutputNode, JsonOutputNode] = NodeFactory.create_node(prompt_template=prompt_template,
        #                  input_variables=input_variables,
        #                  output_variables=output_variables,
        #                  next_item=next_item,
        #                  **kwargs)
        # TODO
        self.embeddings = OpenAIEmbeddings()
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.docs_dir = docs_dir
        self.content_cols = kwargs.get('content_cols', [])
        self.metadata_cols = kwargs.get('metadata_cols', [])
        self._init_v_store()
        self.k = k_result

    def initialize(self, **kwargs):
        pass
    
    def _init_v_store(self):
        if self._is_initiated_before():
            self.vector_db = Chroma(collection_name=self.collection_name, 
                                    persist_directory=self.persist_directory, 
                                    embedding_function=self.embeddings)
        else:
            # create the vector db and add embeddings
            if self.docs_dir[-4:] == ".pdf":
                loader = PyPDFLoader(self.docs_dir)

                loaded_document = loader.load()

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=10,
                    length_function=len,
                    is_separator_regex=False,
                )
                documents = text_splitter.split_documents(loaded_document)

                # TODO enable other embedding types
                self.vector_db = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory,
                    collection_name=self.collection_name,
                )

            elif self.docs_dir[-4:] == ".csv":
                temp_df = pd.read_csv(self.docs_dir)
                texts = []
                metadatas = []
                for i in range(len(temp_df)):
                    content = ""
                    for col in self.content_cols:
                        content += col + "\n" + str(temp_df.iloc[i][col]) + "\n"
                    texts.append(content)

                    metadata = {}
                    for col in self.metadata_cols:
                        metadata[col] = str(temp_df.iloc[i][col])
                    metadatas.append(metadata)

                self.vector_db = Chroma.from_texts(
                    texts=texts,
                    metadatas=metadatas,
                    collection_name=self.collection_name,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory,
                )

    def _is_initiated_before(self):
        # TODO a better checking method
        db_file_path = os.path.join(self.persist_directory,"chroma.sqlite3")
        return os.path.exists(db_file_path)
    
    def run(self, inp: Dict, memory: Union[Memory, None] = None):
        # TODO the pdf loader or the similarity search doesn't work properly and I dont get any results
        retriever = self.vector_db.as_retriever()
        if len(self.input_variables) == 1:
            query = inp[self.input_variables[0]]
        else:
            query = ""
            for var in self.input_variables:
                query += f"{var}: {inp[var]}\n"
        retrieved_docs = retriever.get_relevant_documents(query=query, k=self.k)
        # retrieved_docs = self.vector_db.similarity_search(query=inp[self.query_var], k=self.k)
        if isinstance(self.output_variables, str):
            inp[self.output_variables] = '\n'.join(d.page_content for d in retrieved_docs)
            return inp
        else:
            raise NotImplementedError("Not supported yet!")


class StateUpdater(FlowItem):
    def __init__(self, initial_state: State, 
                 states: List[State] = None, 
                #  temperature: float = 0.1, max_tokens: int = 400, 
                #  verbose: bool = False, return_inputs: bool = False, 
                #  is_output: bool = False, 
                 **kwargs) -> None:
        # self.model_name = model_name
        self.current_state: State = initial_state
        self.states: List[State] = states
        self._init_vars()
        self.node_runner = JsonOutputNode(self.prompt_template, 
                                          self.input_variables, self.output_variables, 
                                          **kwargs)
        self.node_runner.initialize(**kwargs)
        
    def _init_vars(self):
        prompt = state_updater_prompt()
        self.input_variables = ['history', 'current_state']
        output_variables = {}
        name_to_state = {}
        for state in self.states:
            prompt += str(state)
            output_variables[state.name] = bool
            name_to_state[state.name] = state
        
        prompt += """
return a json object, with the name of all states, set current state to true and al of the other states to false."""
        self.prompt_template = prompt
        self.output_variables = output_variables
        self.name_to_state = name_to_state

    def update_state(self, history):
        inp = {'history': history, 'current_state':self.current_state.name}
        # TODO may be run is better than this name?
        decision_result = self.node_runner.run(inp)
        for st_name, v in decision_result.items():
            if v:
                self.current_state = self.name_to_state[st_name]
                break
    

class SQLRetrievalNode(Node):
    def __init__(self, db_path: str, input_variables: List[str], output_variables: Union[str, Dict[str, type]],
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None] = None,
                 **kwargs: Any
                 ) -> None:
        # TODO
        self.db_path = db_path
        self.db = None
        self.conn = None
        self._connect_to_db()
        super().__init__(input_variables=input_variables,
                         output_variables=output_variables,
                         next_item=next_item,
                         **kwargs)
        
    def initialize(self, **kwargs):
        pass

    def _connect_to_db(self):
        try:
            self.db = SQLDatabase.from_uri(f"sqlite:///{self.db_path}")
            self.conn = sqlite3.connect(self.db_path)
        except Exception as e:
            print(f"An error occurred while connecting to the database. Error: {e}")

    def run(self, inp: Dict, memory: Union[Memory, None] = None):
        if self.db is None or self.conn is None:
            return {}
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        chain = create_sql_query_chain(llm, self.db)
        if len(self.input_variables) == 1:
            query = inp[self.input_variables[0]]
        else:
            query = ""
            for var in self.input_variables:
                query += f"{var}: {inp[var]}\n"
        query = chain.invoke({"question": query})
        c = self.conn.cursor()
        c.execute(query)
        if isinstance(self.output_variables, str):
            inp[self.output_variables] = c.fetchall()
            return inp
        else:
            raise NotImplementedError("Not supported yet!")


class NodeFactory:
    @staticmethod
    def create_node(prompt_template: str, 
                    input_variables: List[str], 
                    output_variables: Union[Dict[str, type], str],
                    next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None, 
                    **kwargs) -> Node:
        if isinstance(output_variables, str):
            return StrOutputNode(prompt_template, 
                                 input_variables, output_variables, next_item,
                                 **kwargs)
        elif isinstance(output_variables, Dict):
            return JsonOutputNode(prompt_template, 
                                 input_variables, output_variables, next_item,
                                 **kwargs)
        else:
            raise ValueError("invalid output variables type!")
        
    @staticmethod
    def create_retrieval(input_variables: List[str],
                 output_variables: Union[str, Dict[str, type]],
                 persist_directory: str,
                 collection_name: str,
                 docs_dir: str,
                 k_result: int = 1,
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None, 
                 **kwargs):
        return RetrievalNode(input_variables=input_variables, output_variables=output_variables,
                             persist_directory=persist_directory, collection_name=collection_name,
                             docs_dir=docs_dir, k_result=k_result, next_item=next_item, **kwargs)

    @staticmethod
    def create_sql_node(input_variables: List[str],
                        output_variables: Union[str, Dict[str, type]],
                        db_path: str,
                        next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None] = None,
                        **kwargs):
        return SQLRetrievalNode(input_variables=input_variables, output_variables=output_variables,
                                db_path=db_path, next_item=next_item, **kwargs)
