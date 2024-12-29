
#################The agent was created with SoftwareAI#################


# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#################
# IMPORT SoftwareAI All Paths 
from softwareai.CoreApp._init_paths_ import *
#################
# IMPORT SoftwareAI Instructions
from softwareai.CoreApp.SoftwareAI.Instructions._init_Instructions_ import *
#################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp.SoftwareAI.Tools._init_tools_ import *
#################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
######################################################################


class Dallas2:
    def __init__(self, pathRoadmap, cronograma, planilha, PreProjeto):
        self.pathRoadmap = pathRoadmap
        self.cronograma = cronograma
        self.planilha = planilha
        self.PreProjeto = PreProjeto
    def Dallas2_AgentForPlanningDallas(self, mensagem):
        key = "AgentForPlanningDallas"
        nameassistant = "Dallas2"
        model_select = "gpt-4o-mini-2024-07-18"
        UseVectorstoreToGenerateFiles = False
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None
        Upload_list_for_code_interpreter_in_thread = None
        github_username, github_token = None, None
        key_openai = OpenAIKeysteste.keys()
        name_app = "app2"
        appapp2 = FirebaseKeysinit._init_app_(name_app)
        client = OpenAIKeysinit._init_client_(key_openai)

        if UseVectorstoreToGenerateFiles == True:
            name_for_vectorstore = key
            file_paths = [f"{self.pathRoadmap}", f"{self.cronograma}", f"{self.planilha}", f"{self.PreProjeto}"]
            vector_store_id = Agent_files.auth_vectorstoreAdvanced(appapp2, client, name_for_vectorstore, file_paths)

            Dallas2, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appapp2, client, key, instructionDallas2, nameassistant, model_select, tools_Dallas2, vectorstore_in_assistant)

            Dallas2 = Agent_files_update.update_vectorstore_in_agent(client, Dallas2, [vector_store_id])

            mensagem = f"""
    Analise os quatro arquivos  relacionados ao projeto de software

            """

        else:
    
            read_path_pathRoadmap = python_functions.analyze_txt(self.pathRoadmap)
            read_path_cronograma = python_functions.analyze_txt(self.cronograma)
            read_path_planilha = python_functions.analyze_txt(self.planilha)
            read_path_PreProjeto = python_functions.analyze_txt(self.PreProjeto)

            Dallas2, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appapp2, client, key, instructionDallas2, nameassistant, model_select, tools_Dallas2, vectorstore_in_assistant)
            
            mensagem = f"""
Analise os quatro arquivos  relacionados ao projeto de software

            {read_path_pathRoadmap}
            {read_path_cronograma}
            {read_path_planilha}
            {read_path_PreProjeto}
            """

        
        exemplo = f""" 
        
        """
        
        regras = f""" 
        
        
        """
        mensage_final = mensagem + exemplo + regras
        
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                        mensagem=mensage_final,
                                                                        agent_id=Dallas2,
                                                                        key=key,
                                                                        app1=appapp2,
                                                                        client=client, 
                                                                        tools=tools_Dallas2, 
                                                                        model_select=model_select,
                                                                        aditional_instructions=adxitional_instructions_Dallas2
                                                                    )

                                            
                                                                        
                                
         
        date = datetime.now().strftime('%Y-%m-%d')
        output_path_jsonl = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/Destilation/Dallas2/Jsonl/DestilationAgent{date}.jsonl'))
        output_path_json = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/Destilation/Dallas2/Json/DestilationAgent{date}.json'))
        os.makedirs(output_path_json, exist_ok=True)
        os.makedirs(output_path_jsonl, exist_ok=True)
            
        datasetjson = {
            "input": mensage_final.strip(),
            "output": response.strip()
        }
        datasetjsonl = {
            "messages": [
                {"role": "system", "content": f"{instructionsassistant}"},
                {"role": "user", "content": f"{mensage_final.strip()}"},
                {"role": "assistant", "content": f"{response.strip()}"}
            ]
        }
                    



        finaloutputjson = os.path.join(output_path_json, f"DestilationDateTime_{date.replace('-', '_').replace(':', '_')}.json")
        with open(finaloutputjson, 'a', encoding='utf-8') as json_file:
            json.dump(datasetjson, json_file, indent=4, ensure_ascii=False)
        
        finaloutputjsonl = os.path.join(output_path_jsonl, f"DestilationDateTime_{date.replace('-', '_').replace(':', '_')}.jsonl")
        with open(finaloutputjsonl, 'a', encoding='utf-8') as json_file:
            json_file.write(json.dumps(datasetjsonl, ensure_ascii=False) + "\n")
        

        print(f"Dataset salvo")


            

        return response
            