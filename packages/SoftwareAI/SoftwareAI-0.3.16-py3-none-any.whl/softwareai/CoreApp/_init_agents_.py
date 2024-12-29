from softwareai.CoreApp.Agents.Company_CEO.AI_ByteManager_Company_CEO import ByteManager
from softwareai.CoreApp.Agents.Software_Requirements_Analysis.Dallas2 import Dallas2_AgentForPlanningDallas
from softwareai.CoreApp.Agents.Software_Planning.AI_Bob_Software_Planning import Gerente_de_projeto
from softwareai.CoreApp.Agents.Software_Documentation.AI_CloudArchitect_Software_Documentation import Software_Documentation
from softwareai.CoreApp.Agents.Software_Planning.AI_Dallas_Software_Planning import Equipe_De_Solucoes
from softwareai.CoreApp.Agents.Software_Development.AI_DataWeaver_Software_Development import software_improvements
from softwareai.CoreApp.Agents.Company_Managers.AI_MatrixMinder_Company_Managers import Company_Managers
from softwareai.CoreApp.Agents.Software_Development.AI_QuantumCore_Software_Development import SoftwareDevelopment
from softwareai.CoreApp.Agents.Software_Development.AI_SignalMaster_Software_Development import SoftwareDevelopment_SignalMaster
from softwareai.CoreApp.Agents.Software_Requirements_Analysis.AI_SynthOperator_Software_Requirements_Analysis import Softwareanaysis
from softwareai.CoreApp.Agents.Pre_Project.AI_Tigrao_Pre_Project import Pre_Project_Document
from softwareai.CoreApp.Agents.Software_Development.AI_NexGenCoder_Software_Development import SoftwareDevelopment_NexGenCoder

class AgentInitializer:
    _agents = {}

    @classmethod
    def initialize_agents(cls):
        """Initializes all agents and stores them in the _agents dictionary."""
        cls._agents['Gerente_de_projeto'] = Gerente_de_projeto()
        cls._agents['Dallas2'] = Dallas2_AgentForPlanningDallas()
        cls._agents['Company_Managers'] = Company_Managers() 
        cls._agents['Pre_Project_Document'] = Pre_Project_Document() 
        cls._agents['Software_Documentation'] = Software_Documentation()
        cls._agents['Equipe_De_Solucoes'] = Equipe_De_Solucoes()
        cls._agents['Softwareanaysis'] = Softwareanaysis()
        cls._agents['software_improvements'] = software_improvements()
        cls._agents['SoftwareDevelopment_SignalMaster'] = SoftwareDevelopment_SignalMaster()
        cls._agents['SoftwareDevelopment_NexGenCoder'] = SoftwareDevelopment_NexGenCoder()
        cls._agents['SoftwareDevelopment'] = SoftwareDevelopment(
            cls._agents['Software_Documentation'],
            cls._agents['software_improvements'],
            cls._agents['SoftwareDevelopment_SignalMaster'],
            cls._agents['SoftwareDevelopment_NexGenCoder']
        )
        cls._agents['ByteManager'] = ByteManager(
            cls._agents['Company_Managers'],
            cls._agents['Pre_Project_Document'],
            cls._agents['Gerente_de_projeto'],
            cls._agents['Equipe_De_Solucoes'],
            cls._agents['Softwareanaysis'],
            cls._agents['SoftwareDevelopment']
        )

    @classmethod
    def get_agent(cls, agent_name):
        """Returns an agent instance by name."""
        return cls._agents.get(agent_name)

AgentInitializer.initialize_agents()