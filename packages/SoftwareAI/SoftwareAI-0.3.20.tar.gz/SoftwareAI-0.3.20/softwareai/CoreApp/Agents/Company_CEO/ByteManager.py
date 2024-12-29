
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
#################



def ByteManager_AgentByteManager(Company_Managers, Pre_Project_Document, Gerente_de_projeto, Equipe_De_Solucoes, Softwareanaysis, SoftwareDevelopment):


    key = "AgentByteManager"
    nameassistant = "ByteManager"
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
    name_app = "appx"
    appappx = FirebaseKeysinit._init_app_(name_app)
    client = OpenAIKeysinit._init_client_(key_openai)

    if UseVectorstoreToGenerateFiles == True:
        name_for_vectorstore = key
        file_paths = [f"{Company_Managers}", f"{Pre_Project_Document}", f"{Gerente_de_projeto}", f"{Equipe_De_Solucoes}", f"{Softwareanaysis}", f"{SoftwareDevelopment}"]
        vector_store_id = Agent_files.auth_vectorstoreAdvanced(appappx, client, name_for_vectorstore, file_paths)

        ByteManager, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appappx, client, key, instructionByteManager, nameassistant, model_select, tools_ByteManager, vectorstore_in_assistant)

        ByteManager = Agent_files_update.update_vectorstore_in_agent(client, ByteManager, [vector_store_id])

        mensagem = f"""
decida oque o usuario esta solicitando com base na mensagem asseguir:
        """

    else:
  
        read_path_Company_Managers = python_functions.analyze_txt(Company_Managers)
        read_path_Pre_Project_Document = python_functions.analyze_txt(Pre_Project_Document)
        read_path_Gerente_de_projeto = python_functions.analyze_txt(Gerente_de_projeto)
        read_path_Equipe_De_Solucoes = python_functions.analyze_txt(Equipe_De_Solucoes)
        read_path_Softwareanaysis = python_functions.analyze_txt(Softwareanaysis)
        read_path_SoftwareDevelopment = python_functions.analyze_txt(SoftwareDevelopment)

        ByteManager, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appappx, client, key, instructionByteManager, nameassistant, model_select, tools_ByteManager, vectorstore_in_assistant)
        
        mensagem = f"""
decida oque o usuario esta solicitando com base na mensagem asseguir:
        {read_path_Company_Managers}
        {read_path_Pre_Project_Document}
        {read_path_Gerente_de_projeto}
        {read_path_Equipe_De_Solucoes}
        {read_path_Softwareanaysis}
        {read_path_SoftwareDevelopment}
        """

    
    exemplo = f""" 
    Caso seja solicitado algum script ou software Responda no formato JSON Exemplo: {'solicitadoalgumcodigo': 'solicitacao...'} 
    """
    
    regras = f""" 
    
    
    """
    mensage_final = mensagem + exemplo + regras
    
    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                    mensagem=mensage_final,
                                                                    agent_id=ByteManager,
                                                                    key=key,
                                                                    app1=appappx,
                                                                    client=client, 
                                                                    tools=tools_ByteManager, 
                                                                    model_select=model_select,
                                                                    aditional_instructions=adxitional_instructions_ByteManager
                                                                )

                                           
                                                                    
                            
     
    date = datetime.now().strftime('%Y-%m-%d')
    output_path_jsonl = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/Destilation/ByteManager/Jsonl/DestilationAgent{date}.jsonl'))
    output_path_json = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/Destilation/ByteManager/Json/DestilationAgent{date}.json'))
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
            