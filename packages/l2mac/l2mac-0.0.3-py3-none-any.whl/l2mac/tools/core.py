"""
This module provides core functionalities for managing and executing various
tools and functions related to code analysis, file operations, and task
management.

Functions:
  available_functions_factory():
    Returns a dictionary of available functions mapped to their respective
    implementations.

  function_definition_list_factory():
    Generates a list of function definitions in the updated format for function
    definitions.

  function_definition_list_factory_internal():
    Internal helper function to create a list of function definitions.

  process_functions_into_function_names(tools: List[dict] = []):
    Processes a list of tools into a list of function names.

  process_function_call_and_return_message(tool_calls: dict, file_dict: dict,
    logger=None, tools=[], enable_tests=True):
    Processes function calls and returns messages based on the execution of the
    specified functions.
"""
import json
import traceback
from typing import Any, List, Tuple

from l2mac.tools.code_analysis import pytest_files, run_python_file
from l2mac.tools.control_unit import (
    check_sub_task_step_complete,
    provide_detailed_sub_task_steps_for_sub_agents,
)
from l2mac.tools.read import list_files, view_files
from l2mac.tools.write import delete_files, write_files


def available_functions_factory():
  available_functions = {
      "provide_detailed_sub_task_steps_for_sub_agents":
      provide_detailed_sub_task_steps_for_sub_agents,
      "sub_task_step_complete": check_sub_task_step_complete,
      "view_files": view_files,
      "list_files": list_files,
      "pytest_files": pytest_files,
      "run_python_file": run_python_file,
      "delete_files": delete_files,
      "write_files": write_files,
  }
  return available_functions


def function_definition_list_factory():
  # Following OpenAI's updated format for function definitions
  functions = function_definition_list_factory_internal()
  tools = []
  for function in functions:
    tools.append({"type": "function", "function": function})
  return tools


def function_definition_list_factory_internal():
  functions = [
      {
          "name": "provide_detailed_sub_task_steps_for_sub_agents",
          "description":
          "For producing a step-by-step plan, where each step paragraph is a "
          "detailed sub-task step for a separate sub-agent (large language "
          "model agent) to complete. Within each detailed step paragraph, "
          "always include a last sentence to create and run tests when "
          "implementing or writing code in that same step.",
          "parameters": {
              "type": "object",
              "properties": {
                  "steps": {
                      "type": "array",
                      "description":
                      "List of strings, where each string is a separate step "
                      "sub-task paragraph for a separate sub-agent to "
                      "complete. Within each detailed step paragraph, always "
                      "include a last sentence to create and run tests when "
                      "implementing or writing code in that same step.",
                      "items": {
                          "type": "string"
                      },  # assuming each file is represented as a string
                  },
              },
              "required": ["steps"],
          },
      },
      {
          "name": "sub_task_step_complete",
          "description":
          "Call this function when the user specified sub task step has been "
          "completed.",
          "parameters": {
              "type": "object",
              "properties": {},
          },
      },
      {
          "name": "view_files",
          "description":
          "Print out the file contents into the response to view.",
          "parameters": {
              "type": "object",
              "properties": {
                  "files": {
                      "type": "array",
                      "description": "list of the files to view",
                      "items": {
                          "type": "string"
                      },  # assuming each file is represented as a string
                  },
              },
              "required": ["files"],
          },
      },
      {
          "name": "run_python_file",
          "description":
          "Run python file and return the output to the response to view. That "
          "is with 'python3 file_name_to_run'.",
          "parameters": {
              "type": "object",
              "properties": {
                  "file_name_to_run": {
                      "type": "string",
                      "description": "file name to run",
                  },
                  "arguments": {
                      "type": "array",
                      "description": "optional run arguments",
                      "items": {
                          "type": "string"
                      },
                  },
              },
              "required": ["file_name_to_run"],
          },
      },
      {
          "name": "pytest_files",
          "description":
          "Run pytest on the input file names and print out the results to the "
          "response to view. If no file names are provided, pytest runs on all "
          "files.",
          "parameters": {
              "type": "object",
              "properties": {
                  "files_to_test": {
                      "type": "array",
                      "description": "file names to run pytest on",
                      "items": {
                          "type": "string"
                      },
                  },
              },
          },
      },
      {
          "name": "write_files",
          "description":
          "Write out multiple files and it will be combined into the existing "
          "code base. Always output the whole file. You always indent code "
          "with tabs.",
          "parameters": {
              "type": "object",
              "properties": {
                  "list_of_file_objects": {
                      "type": "array",
                      "items": {
                          "type": "object",
                          "properties": {
                              "file_path": {
                                  "type": "string",
                                  "description": "Path to the file",
                              },
                              "file_contents": {
                                  "type": "string",
                                  "description": "Contents of the file",
                              },
                          },
                          "required": ["file_path", "file_contents"],
                      },
                  }
              },
              "required": ["list_of_file_objects"],
          },
      },
      {
          "name": "delete_files",
          "description":
          "Delete files. Specify the file names, and these files will be "
          "deleted. If you specify the file name '-1' all files in the folder "
          "will be deleted.",
          "parameters": {
              "type": "object",
              "properties": {
                  "files": {
                      "type": "array",
                      "description":
                      "list of the files to delete. If you provide a file name "
                      "of '-1' all files in the folder will be deleted.",
                      "items": {
                          "type": "string"
                      },  # assuming each file is represented as a string
                  },
              },
              "required": ["files"],
          },
      },
  ]
  return functions


def process_functions_into_function_names(tools: List[dict]):
  function_names = []
  for tool in tools:
    function_names.append(tool["function"]["name"])
  return function_names


def process_function_call_and_return_message(tool_calls: dict,
                                             file_dict: dict,
                                             tools: List[dict],
                                             logger=None,
                                             enable_tests=True) -> \
                                              Tuple[list[dict[str, Any]], dict]:
  function_name = ""
  if len(tools) >= 1:
    functions_available_keys = process_functions_into_function_names(tools)
  else:
    functions_available_keys = list(available_functions_factory().keys())
  functions_available = available_functions_factory()
  return_messages = []
  for tool_call in tool_calls:
    try:
      function_name = tool_call["function"]["name"]
      if function_name not in functions_available_keys:
        json_fun_content = json.dumps({
            "status":
            "error",
            "message":
            f"Function `{function_name}` not found. Please only use the "
            f"functions listed given, which are: {functions_available_keys}",
        })
        function_return_message = {
            "tool_call_id": tool_call["id"],
            "role": "tool",
            "name": function_name,
            "content": json_fun_content,
        }
        return_messages.append(function_return_message)
        continue
      function_to_call = functions_available[function_name]
      function_args = json.loads(tool_call["function"]["arguments"])
      function_args["file_dict"] = file_dict
      function_args["enable_tests"] = enable_tests
      if (function_name == "write_files") or (function_name == "delete_files"):
        function_response, file_dict = function_to_call(**function_args)
      else:
        function_response = function_to_call(**function_args)
      function_return_message = {
          "tool_call_id": tool_call["id"],
          "role": "tool",
          "name": function_name,
          "content": function_response,
      }
      return_messages.append(function_return_message)
    except KeyError as e:
      if logger:
        logger.error("Error in process_function_call_and_return_message()")
        logger.error(e)
        logger.error(traceback.format_exc())
        logger.error(
            f"process_function_call_and_return_message({tool_call},{file_dict})"
        )
      error_message = "".join(traceback.format_exception_only(type(e), e))
      json_fun_content = json.dumps({
          "status":
          "error",
          "message":
          f"Error Decoding Message: {error_message}",
      })
      function_return_message = {
          "tool_call_id": tool_call["id"],
          "role": "tool",
          "name": function_name,
          "content": json_fun_content,
      }
      return_messages.append(function_return_message)
    except json.decoder.JSONDecodeError as e:
      if logger:
        logger.error("Error in process_function_call_and_return_message()")
        logger.error(e)
        logger.error(traceback.format_exc())
        logger.error(
            f"process_function_call_and_return_message({tool_call},{file_dict})"
        )
      error_message = "".join(traceback.format_exception_only(type(e), e))
      error_content = ("Response was too long and was cut off. Please give a "
                       "shorter response! As the response was cut off early, "
                       "there was an error decoding the response: "
                       f"{error_message}")
      json_fun_content = json.dumps({
          "status": "error",
          "message": error_content
      })
      function_return_message = {
          "tool_call_id": tool_call["id"],
          "role": "tool",
          "name": function_name,
          "content": json_fun_content,
      }
      return_messages.append(function_return_message)
    except (TypeError, ValueError, RuntimeError) as e:
      if logger:
        logger.error("Error in process_function_call_and_return_message()")
        logger.error(e)
        logger.error(traceback.format_exc())
        logger.error(
            f"process_function_call_and_return_message({tool_call},{file_dict})"
        )
      error_message = "".join(traceback.format_exception_only(type(e), e))
      json_fun_content = json.dumps({
          "status":
          "error",
          "message":
          f"Error running function: {error_message}",
      })
      function_return_message = {
          "tool_call_id": tool_call["id"],
          "role": "tool",
          "name": function_name,
          "content": json_fun_content,
      }
      return_messages.append(function_return_message)
  return return_messages, file_dict  # pytype: disable=bad-return-type
