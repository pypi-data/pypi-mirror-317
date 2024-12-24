#region: Modules.
import numpy as np 
from fp.schedulers.scheduler import *
from fp.inputs.wfngeneral import *
#endregion

#region: Variables.
#endregion

#region: Functions.
#endregion

#region: Classes.
class EpsilonInput:
    def __init__(
        self,
        bands,
        cutoff,
        wfn_link,
        wfnq_link,
        job_desc,
        extra_args: str=None,
    ):
        self.bands = bands  
        self.cutoff = cutoff
        self.wfn_link: str = wfn_link
        self.wfnq_link: str = wfnq_link
        self.extra_args: str = extra_args
        self.job_desc: JobProcDesc = job_desc
        
    def get_qgrid_str(self, wfn_input: WfnGeneralInput, qshift):
        return wfn_input.get_kgrid_eps_string(qshift=qshift)
#endregion
