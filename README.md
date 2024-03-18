# Word Document RCE with a ChatGPT-3.5-Turbo Langchain Agent
This repository demonstrates the use of a Langchain Agent to carry out Remote Code Execution (RCE). Specifically, it involves opening a reverse shell on a target device hosting the Agent.

Please note this is NOT an exploit in ChatGPT-3.5-Turbo itself (you could replace it with any competent enough LLM) or Lanchain. It's an example of how if proper measures are not taken when using an LLM as an Agent with a set of tools (primarily the ability to execute arbitary code), you risk enabling exploits like RCE. The Python REPL provided by Langchain and used in this example, explicitly states that it can enable RCE. This code is for research purposes only and should be treated as such.

## Instructions
1. Open the repository in VSCode and use [devcontainers](https://code.visualstudio.com/docs/remote/containers) to open the repository using the Command Palette command `Dev Containers: Rebuild and Reopen in Container`.
2. Execute `pip install -r requirements.txt` to install the necessary dependencies.
3. Set your `OPEN_API_KEY` environment variable in the `run_agent.py` file at the bottom.
4. Start the agent by running `python run_agent.py`. This hosts the agent with a Gradio frontend accessible at `localhost:8999`.
5. In a separate terminal, execute `python run_shell_connection.py`. This script hosts a socket that polls for a connection to the reverse-shell code found in the attached Word document.
6. Upload the `Document_Processing_Instructions.docx` file through the Gradio frontend's upload field, located under the "Additional Inputs" tabs at the bottom.
7. Submit the following prompt through the Gradio frontend: "Can you execute the instructions in Document_Processing_Instructions.docx?"

After approximately twenty seconds, you should see a connection to the socket initiated from the `run_shell_connection.py` script, indicating that the LLM agent has executed the hidden code at the beginning of the Word document.

You can now execute commands that will be carried out through the reverse-shell on the device running the LLM. As this is a proof of concept, the reverse-shell is only suitable for basic single-step commands (ls, pwd, mkdir, rmdir, rm, etc.).

## Word Document
To view the code in the Word document, open it in Microsoft Word, select all the text (CMD/CTRL + A), and then click the 'Show/Hide formatting marks' button in the Font section of the Home tab. The code text is hidden by setting the font effects to 'Hidden'.

## Usage Notes
This repository is setup for demoing purposes with running both the Agent and shell connection on the same device. If you want to run this on seperate devices, set the address/port in `python run_shell_connection.py` to point to the device you will be running the Agent on. If you change the port in `python run_shell_connection.py`, you will need to also change the port specified in the hidden code within `Document_Processing_Instructions.docx` to match.

## Please Note
The agent does NOT always execute the code; occasionally, ChatGPT-3.5-Turbo may recognize the nature of the code (a reverse shell) and refuse to run it. With the given prompt, the code executes approximately 80% of the time.

Any questions please feel free to reach out!
