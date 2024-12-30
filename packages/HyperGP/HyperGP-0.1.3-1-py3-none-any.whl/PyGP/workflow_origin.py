from .base.base_struct import BaseStruct
from PyGP.mods import AvailableMods, __Mods
import types
import itertools
from PyGP.base.base_struct import States
from PyGP.library.states import WorkflowStates
class GpOptimizer(BaseStruct, __Mods):
    
    available_mods = AvailableMods()
    
    def __init__(self, states=None, module_states=None, monitor=None, parallel=True, gpu=True, cash=False, precision=8, **kwargs):
        self.gpu=gpu
        self.func_list, self.func_name = [], []
        self.workflowstates = WorkflowStates()
        super().__init__(states, module_states, **kwargs)
        if parallel:
            self.enable('parallel')
    
    def iter_component(self, funcs):
        for func in funcs:
            f = func[0]
            print(type(f))
            if type(f) == types.FunctionType or type(f) == types.BuiltinFunctionType:
                self.func_name.append(f.__name__)
                self.workflowstates[f.__name__ + '_ret'] = None
            else:
                self.func_name.append(f.__class__.__name__)
                self.workflowstates[f.__class__.__name__ + '_ret'] = None
        print(self.func_name)
        self.func_list.extend(funcs)
    
    def enable(self, mod, **kwargs):
        if getattr(self, mod):
            self.__setattr__(mod, self.available_mods.__getattribute__(mod)())
            self.__getattribute__(mod)._popSet(self, **kwargs)
            
    def run(self, iter):
        for i in range(iter):
            print('iteration: %d'%i)
            for j, (func, f_name) in enumerate(zip(self.func_list, self.func_name)):
                f, states, parallel = func[0], func[1][0], func[2]
                print('func: ', f_name, type(f))
                if len(func[1]) > 1:
                    kwargs = func[1][1]
                else:
                    kwargs = {}
                self.workflowstates[f_name + '_ret'] = self.__parallel(f, states, parallel, **kwargs)
                if len(func) > 3 and func[3] != None:
                    # print(self.states[f_name + '_ret'])
                    func[3] = self.workflowstates[f_name + '_ret']

    def __parallel(self, method, states, parallel=True, **kwargs):
        if isinstance(method, list) and len(method) != len(states):
            raise ValueError('The method size %d not equal to the cond size %d' % (len(method), len(states)))
        if 'parallel' in self.gmodule_states and parallel:
            ret_cond = self.parallel(method, states, **kwargs)
        else:
            ret_cond = []
            if isinstance(states, States):
                ret_cond.append(method(**states, **kwargs))
            elif isinstance(states, list):
                assert len(states) == len(method)
                for i, state in enumerate(states):
                    ret_cond.append(method(**state, **kwargs)
                                if not isinstance(method, list)
                                else method[i](**state, **kwargs))
            else:
                assert 0==1
        return ret_cond
                    
    def step():
        pass
    