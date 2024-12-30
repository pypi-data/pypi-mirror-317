from multiprocessing import Process, Event, Queue
import os
import subprocess
import shlex
import argparse
import re
import random
import subprocess

from nucleus.data_viz.planner import plan
from nucleus.terminal.suggestion import session, PLACEHOLDER
from nucleus.gui import run_flask_app
from nucleus.terminal.planner import QueryManager
from nucleus.logger import log
from nucleus.tools import MessagePrinter

def extract_command(text):
    """
    Extracts a command from a text block surrounded by triple backticks and in bash syntax.
    
    Args:
        text (str): The input text containing the command.
        
    Returns:
        str: The extracted command, or None if no command is found.
    """
    match = re.search(r"```bash\n(.+?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def confirm_ask():
    """
    Prompt the user to decide whether to run or not.
    """
    ask_text = "\n[bold cyan]Do you want to run?[/bold cyan] [green](Yes or No):[/green] "
    # console.print(ask_text, end=" ")
    response = console.input(ask_text).strip().lower()
    if response in ['yes', 'y']:
        return True
    elif response in ['no', 'n']:
        return False
    else:
        print("Invalid input. Please respond with 'Yes' or 'No'.")
        confirm_ask()  # Re-prompt the user


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--openai-api-key",  help="Specify the OpenAI API key")
    parser.add_argument("--anthropic-api-key", help="Specify the Anthropic API key")
    args = parser.parse_args()

    model, api_key = None, None

    input_vals = {
        'LLM': []
    }

    if args.openai_api_key:
        model = 'openai'
        api_key = args.openai_api_key

        input_vals['LLM'] = [{
            'model': model, 
            "api_key": api_key
            }]
        
        return input_vals
    
    if args.anthropic_api_key:
        model = "anthropic"
        api_key = args.anthropic_api_key

        input_vals['LLM'] = [{
            'model': model, 
            "api_key": api_key
            }]
        
        return input_vals

    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if openai_api_key:
        model='openai'
        api_key = openai_api_key
        
        input_vals['LLM'].append({
            "model":model,
            "api_key": api_key
        })
    
    if anthropic_api_key:
        model='anthropic'
        api_key = anthropic_api_key

        input_vals['LLM'].append({
            "model":model,
            "api_key": api_key
        })
    
    if gemini_api_key:
        model='gemini'
        api_key = gemini_api_key

        input_vals['LLM'].append({
            "model":model,
            "api_key": api_key
        })
    
    return input_vals
    
def main():

    input_vals = {}

    input_args = args_parser()
    if not len(input_args['LLM']):
        log.error("Error: No API key provided. Please provide an API key to proceed.")
        return

    if len(input_args['LLM'])==1:
        input_vals['LLM'] = input_args['LLM'][0]

    if len(input_args["LLM"])>1:
        log.warning("Multiple API keys found in your environment variables, but none explicitly provided.")
        llm = random.choice(input_args["LLM"])
        log.info(f"Randomly selected API key for the model '{llm['model']}'.")
        input_vals['LLM'] = llm


    message_printer = MessagePrinter()

    message_printer.system_message("Type commands as usual. ask anything u want")
    message_printer.system_message("Type 'exit' or 'quit' to stop the program.\n")

    ## run flask local server for visualization
    data_queue = Queue()
    flask_process = Process(target=run_flask_app, args=(data_queue,))
    flask_process.start()

    query_responder = QueryManager(input_vals, message_printer)
    while True:
        try:
            # Prompt for user input

            user_input = session.prompt("\n> ", placeholder=PLACEHOLDER)

            # Check if the user wants to exit
            if user_input.lower() == "":
                continue

            if user_input.lower() in ["exit", "quit"]:
                message_printer.system_message("Exiting shell. Goodbye!")
                                
                flask_process.terminate()
                flask_process.join()

                break

            if user_input.lower()[0] in "!":
                # handle 'cd' command to change directory
                user_input = user_input[1:]
                if user_input.startswith("cd"):
                    parts = shlex.split(user_input)
                    if len(parts) > 1:
                        new_dir = parts[1]
                    else:
                        new_dir = os.path.expanduser("~")
                    try:
                        os.chdir(new_dir)
                    except FileNotFoundError:
                        print(f"cd: {new_dir}: No such file or directory")
                    except Exception as e:
                        print(f"cd: {e}")
                else:
                    subprocess.run(shlex.split(user_input), check=False)

            elif user_input.startswith("/show"):
                file_input = user_input.split("/show", 1)[-1].strip()
                config = plan(file_input, session)
                data_queue.put(config)

                message_printer.system_message("You can view the file at http://127.0.0.0:5000")

            elif user_input == "/close":
                if flask_process and flask_process.is_alive():
                    message_printer.system_message("Stopping visualization process...")
                    flask_process.terminate()
                    flask_process.join()
                # Run other normal terminal commands
                else:
                    subprocess.run(shlex.split(user_input), check=False)
            else:
                query_responder.execute_query(user_input)

        except KeyboardInterrupt:
            message_printer.system_message("\n Exiting shell. Goodbye!")
            break
        except Exception as e:
            log.error("Error in main : {e}")
    
    flask_process.terminate()
    flask_process.join()



if __name__ == "__main__":
    main()