from os import environ as env, fsync
import sys

if "DYLD_LIBRARY_PATH" in env:
	LIB_PATH = env["DYLD_LIBRARY_PATH"]
elif "LD_LIBRARY_PATH" in env:
	LIB_PATH = env["LD_LIBRARY_PATH"]
else:
	print("Soar LIBRARY_PATH environment variable not set; quitting")
	exit(1)
sys.path.append(LIB_PATH)
import Python_sml_ClientInterface as sml


# Callback functions to help us see what is happening inside agent's mind
def register_print_callback(kernel, agent, function, user_data=None):
	agent.RegisterForPrintEvent(sml.smlEVENT_PRINT, function, user_data)
def callback_print_message(mid, user_data, agent, message):
	print(message.strip())

# Main program
if __name__ == "__main__":
    #Create kernel and agent
    kernel = sml.Kernel.CreateKernelInCurrentThread()
    agent = kernel.CreateAgent("agent")
    register_print_callback(kernel, agent, callback_print_message, None)
    #Load soar sources
    agent.ExecuteCommandLine("source hello-world.soar")
    #Run agent for one step
    run_result=agent.RunSelf(1)
    #Close agent and kernel
    kernel.DestroyAgent(agent)
    kernel.Shutdown()
