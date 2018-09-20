"""Making sure we are running the right version of python"""
import sys
import time
if sys.version_info[0] >= 3:
    raise "Must be using Python 2"

"""Making sure soar library path environment is set
Remember to set the environment variable to point to where soar build is located, e.g.:
export LD_LIBRARY_PATH=~/Desktop/Soar/out
"""
from os import environ as env, fsync
import sys
from random import *

if "DYLD_LIBRARY_PATH" in env:
	LIB_PATH = env["DYLD_LIBRARY_PATH"]
elif "LD_LIBRARY_PATH" in env:
	LIB_PATH = env["LD_LIBRARY_PATH"]
else:
	print("Soar LIBRARY_PATH environment variable not set; quitting")
	exit(1)
sys.path.append(LIB_PATH)
import Python_sml_ClientInterface as sml


""" Callback functions to help us see what is happening inside agent's mind"""
def register_print_callback(kernel, agent, function, user_data=None):
	agent.RegisterForPrintEvent(sml.smlEVENT_PRINT, function, user_data)
def callback_print_message(mid, user_data, agent, message):
	print(message.strip())

""" Client to interact with agent's mind"""
def cli(agent):
	cmd = raw_input("soar> ")
	while cmd not in ("exit", "quit"):
		if cmd:
			print(agent.ExecuteCommandLine(cmd).strip())
		cmd = raw_input("soar> ")

""" Gets an output value from output link for a given attribute """
def getOutput(attribute):
    aa=agent.ExecuteCommandLine("print i3").replace("(", "").replace(")", "") 
    bb=aa.split(" ")
    attribute="^"+attribute
    value=None
    if attribute in aa:
        pos=bb.index(attribute)
        value=bb[pos+1]
    return value


class ToyEnv(object):
    """
    A very simple 'environment': sensors return two random numbers and expects a single number as actuation.
    """
    def __init__(self):
        """Return a new toy env object."""


    def get_sensors(self):
        """"""
        a=randint(1, 10)
        b=randint(1, 10)
        sensors=[a,b]
        print("---> Environment sensed: ",sensors)
        return sensors

    def set_actuators(self, act):
        """"""
        print("---> Environment acted:",act)


""" Main program """
if __name__ == "__main__":

    

    #Instantiate link to environment
    te = ToyEnv()

    #Create soar kernel and agent
    kernel = sml.Kernel.CreateKernelInCurrentThread()
    agent = kernel.CreateAgent("agent")
    register_print_callback(kernel, agent, callback_print_message, None)

    #Load soar sources
    agent.ExecuteCommandLine("source toy-env-multitask.soar")

    #Get input link and create input  structure
    input_link=agent.GetInputLink()
    
    a_value=agent.CreateFloatWME(input_link, "a", -1.0)
    b_value=agent.CreateFloatWME(input_link, "b", -1.0)

    #Get output link
    output_link=agent.GetOutputLink()

    ### Start Soar cognitive cycle ###
    #

    firstRun = True
    for i in range(0,3): # replace by a "while True:" to run forever
        print(" ------------- Soar cycle: ",i," ------------- ")
    # 1) sense the environment
        sense=te.get_sensors()

    # 2) push senses to soar
        
        a_value.Update(sense[0])
        b_value.Update(sense[1])

    # 3) make soar think about it
        result=0
#        run_result=agent.RunSelf(1)    #Run agent for one step
        run_result=agent.RunSelfTilOutput()    #Run agent until output
#        cli(agent)
        if(firstRun): #First run for initialization
            run_result=agent.RunSelfTilOutput()
            firstRun=False            
            
    # 4) get results from soar
        output_link=agent.GetOutputLink()# returns an Identifier
        if output_link!= None:
            result_output_wme = output_link.FindByAttribute("add_result", 0) 
          #  result_sub_output_wme = output_link.FindByAttribute("sub_result", 0)
            result=[]
            if result_output_wme != None:
                result.append(float(result_output_wme.GetValueAsString()))
              #  result.append(float(result_sub_output_wme.GetValueAsString()))

    #5) send result to environment
        te.set_actuators(result) 

#    value=getOutput("add_result") #TODO testing alternative to agent.GetOutputLink()
#    print(value)

    cli(agent) #open client to interact with agent

    #Close agent and kernel
    kernel.DestroyAgent(agent)
    kernel.Shutdown()



## SANDBOX #######

#        resultWME = agent.CreateIdWME(output_link, "result")
#        resultValueWME=agent.CreateFloatWME(resultWME, "value", -1.0)

#        print("resultWME: ",resultWME.IsIdentifier())
#        resultWME.AddStatusComplete() # A

#        found_resultWME=output_link.FindByAttribute("result", 0)
#        print("found_resultWME: ",found_resultWME.IsIdentifier())
#        found_resultWME.AddStatusComplete() #B



#        resultStatusWME=agent.CreateStringWME(resultWME, "status", "ongoing")



#            test_result_output_wme = output_link.FindByAttribute("result", 0)
#            test_result_output_wme.AddStatusComplete()
            

#            test_result=None
#            if test_result_output_wme != None:
                #test_val_wme = test_result_output_wme.FindByAttribute("value", 0)
                #test_status_wme = test_result_output_wme.FindByAttribute("status", 0)
                #test_status = test_status_wme.GetValueAsString()
                #print("test_status: ",test_status)

#result_output_wme.ConvertToIdentifier()

#    #the output of "print s1" should contain "^rhstest success"
#    if kernel.ExecuteCommandLine("print s1", "Soar1").find("^rhstest success") == -1:
#	    print >> sys.stderr, "\nRHS test FAILED"
#	    sys.exit(1)

#    testWME=agent.CreateFloatWME(input_link, "test", -1.0)
#    agent.DestroyWME(testWME)
