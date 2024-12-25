'''connector for Simio, dependent on python for .net (pythonnet)


'''
import os
import sys

import clr  # @UnresolvedImport

# TODO:: do some auto discovery here analogue to netlogo?
sys.path.append('C:/Program Files (x86)/Simio')
clr.AddReference('SimioDLL')
clr.AddReference('SimioAPI')
import SimioAPI  # @UnresolvedImport

from ..em_framework import FileModel, SingleReplication
from ..util import CaseError, EMAError
from ..util.ema_logging import get_module_logger, method_logger

# Created on 27 June 2019
#
# .. codeauthor:: jhkwakkel <j.h.kwakkel (at) tudelft (dot) nl>
_logger = get_module_logger(__name__)

class SimioModel(FileModel, SingleReplication):
    
    @method_logger(__name__)
    def __init__(self, name, wd=None, model_file=None, main_model=None):
        """interface to the model

        Parameters
        ----------
        name : str
               name of the modelInterface. The name should contain only
               alpha-numerical characters.
        working_directory : str
                            working_directory for the model.
        model_file  : str
                     the name of the model file
        main_model : str

        Raises
        ------
        EMAError
            if name contains non alpha-numerical characters
        ValueError
            if model_file cannot be found

        """    
        super(SimioModel, self).__init__(name, wd=wd, model_file=model_file)
        assert main_model != None
        self.main_model_name = main_model
        self.output = {}
    
    @method_logger(__name__)
    def model_init(self, policy):
        super(SimioModel, self).model_init(policy)
        _logger.debug('initializing model')
        
        # get project
        path_to_file = os.path.join(self.working_directory, self.model_file)
        self.project = SimioAPI.ISimioProject(SimioAPI.SimioProjectFactory.LoadProject(path_to_file))
        self.policy = policy
        
        # get model
        models = SimioAPI.IModels(self.project.get_Models())
        model = models.get_Item(self.main_model_name)
        
        if not model:
            raise EMAError((f'''main model with name {self.main_model_name} '
                            'not found'''))
               
        self.model = SimioAPI.IModel(model)
        
        # set up new EMA specific experiment on model
        _logger.debug('setting up EMA experiment')
        self.experiment = SimioAPI.IExperiment(model.Experiments.Create('ema experiment'))
        SimioAPI.IExperimentResponses(self.experiment.Responses).Clear()
        
        # use all available responses as template for experiment responses
        responses = get_responses(model)
        
        for outcome in self.outcomes:
            for name in outcome.variable_name:
                name = outcome.name
                try:
                    value = responses[name]
                except KeyError:
                    raise EMAError(f'response with name \'{name}\' not found')
                
                response = SimioAPI.IExperimentResponse(self.experiment.Responses.Create(name))
                response.set_Expression(value.Expression)
                response.set_Objective(value.Objective)
        
        # remove any scenarios on experiment
        self.scenarios = SimioAPI.IScenarios(self.experiment.Scenarios)
        self.scenarios.Clear()
        
        # make control map
        controls = SimioAPI.IExperimentControls(self.experiment.get_Controls())
        self.control_map = {}
        
        for i in range(controls.Count):
            control = controls.get_Item(i)
            
            self.control_map[control.Name] = control      
            
        _logger.debug('model initialized successfully') 
     
    @method_logger(__name__)
    def run_experiment(self, experiment):
        self.case = experiment
        _logger.debug('Setup SIMIO scenario')
        
        scenario = self.scenarios.Create()
        _logger.debug(f'nr. of scenarios is {self.scenarios.Count}')

        for key, value in experiment.items():
            try:
                control = self.control_map[key]
            except KeyError:
                raise EMAError(('''uncertainty not specified as '
                                  'control in simio model'''))
            else:
                ret = scenario.SetControlValue(control, str(value))
                
                if ret:
                    _logger.debug(f'{key} set successfully')
                else:
                    raise CaseError(f'failed to set {key}')
            
        _logger.debug('SIMIO scenario setup completed')
            
        self.experiment.ScenarioEnded += self.scenario_ended   
        self.experiment.RunCompleted += self.run_completed  
        
        _logger.debug('preparing to run model')
        self.experiment.Run()
        _logger.debug('run completed')
        return self.output

    @method_logger(__name__)
    def reset_model(self):
        """
        Method for reseting the model to its initial state. The default
        implementation only sets the outputs to an empty dict. 

        """
        super(SimioModel, self).reset_model()
        
        self.scenarios.Clear()
        self.output = {}
      
    @method_logger(__name__)  
    def scenario_ended(self, sender, scenario_ended_event):
        '''scenario ended event handler'''
        
#         ema_logging.debug('scenario ended called!')
    
        # This event handler will be called when all replications for a
        # given scenario have completed.  At this point the statistics
        # produced by this scenario should be available.
        experiment = SimioAPI.IExperiment(sender)
        scenario = SimioAPI.IScenario(scenario_ended_event.Scenario)
        
        _logger.debug((f'''scenario {scenario.Name} for experiment '
                       '{experiment.Name} completed'''))
        responses = experiment.Scenarios.get_Responses()
        
        # http://stackoverflow.com/questions/16484167/python-net-framework-reference-argument-double
        
        for response in responses:
            _logger.debug(f'{response}')
            response_value = 0.0
            try:
                success, response_value = scenario.GetResponseValue(response, 
                                                                response_value)
            except TypeError:
                _logger.warning((f'''type error when trying to get a '
                                 'response for {response.Name}'''))
                raise
            
            if success:
                self.output[response.Name] = response_value
            else:
                # no valid response value
                error = CaseError(f'no valid response for {response.Name}',
                                  self.case) 
                _logger.exception(str(error))
                
                raise 
     
    @method_logger(__name__)   
    def run_completed(self, sender, run_completed_event):
        '''run completed event handler'''
        
        _logger.debug('run completed')
        
        # This event handler is the last one to be called during the run.
        # When running async, this is the correct place to shut things down.
        experiment = SimioAPI.IExperiment(sender)
        # Un-wire from the run events when we're done.
        experiment.ScenarioEnded -= self.scenario_ended
        experiment.RunCompleted -= self.run_completed


def get_responses(model):
    '''Helper function for getting responses 
    
    this function gathers all responses defined on all experiments available
    on the model.
    
    Parameters
    ----------
    model : SimioAPI.IModel instance
    
    '''
    
    response_map = {}
    
    experiments = SimioAPI.IExperiments(model.Experiments)
    for i in range(experiments.Count):
        experiment = SimioAPI.IExperiment(experiments.get_Item(i))
        responses = SimioAPI.IExperimentResponses(experiment.Responses)
        for j in range(responses.Count):
            response = SimioAPI.IExperimentResponse(responses.get_Item(j))
            
            response_map[response.Name] = response
    
    return response_map
    
  
    