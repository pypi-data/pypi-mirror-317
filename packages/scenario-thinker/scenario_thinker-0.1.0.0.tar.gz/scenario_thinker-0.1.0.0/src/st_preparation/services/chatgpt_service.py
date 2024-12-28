from openai import OpenAI
import os
from dotenv import load_dotenv
from services.parse_scenario import parse_feature_file
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import ast
import re
system_input = """
Return me a json object, which will have two keys: one named "code", which will be executable for python with method exec(),
another one will be called "bdd" and will be used as .py file for a bdd feature step usage.
Please provide me "code" value as simple as possible, parseable by ast module.
Please find objects by looking first for id of them. Try to find objects by their attributes, class and using xpath, at the final you can use finding by text.
Do not put imports in python code - i do not need them. I already have prepared in python code from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By.

Give me one line at a time.

EXAMPLE OF WORKINIG:

Feature scenario file:
The BDD scenario is as follows:
    Given visiting site localhost:3000/button_with_redirect
    When I click button with text "Go to my favorites"
    Then I will be redirected into site localhost:3000/my_favourites

Upper scenario should result in this actions for Selenium WebDriver to:
    Navigate to the page localhost:3000/button_with_redirect
    Click on the button with the text "Go to my favorites"
    Verify that the URL is equal to localhost:3000/my_favourites
    
HTML code:
<html>
  <body>
    <div style="display: flex; align-items: center; justify-content: center; width: 100vw; height: 100vh;">
  <a href="/my_favourites">
    <button style="background-color: cyan; border: none; font-size: 30px; cursor: pointer; ">
      Go to my favorites
    </button>
  </a>
</div>
  

</body></html>

So for the line 'Given visiting site localhost:3000/button_with_redirect' it will be: 
{
  "code": "driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))\ndriver.get('http://localhost:3000/button_with_redirect')",
  "bdd": "@given('visiting site \"localhost:3000/button_with_redirect\"')\ndef step_visit_site(context, url):\n    context.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))\n    context.driver.get(url)"
}
For the line 'When I click button with text "Go to my favorites"', it will be: 
{
  "code": "button = driver.find_element(By.XPATH, '//button[contains(text(), \"Go to my favorites\")]')\nbutton.click()",
  "bdd": "@when('I click button with text \"Go to my favorites\"')\ndef step_click_button(context):\n    button = context.driver.find_element(By.XPATH, '//button[contains(text(), \"Go to my favorites\")]')\n    button.click()"
}
For the line 'Then I will be redirected into site localhost:3000/my_favourites', it will be:
{
  "code": "current_url = driver.current_url\nassert current_url == 'http://localhost:3000/my_favourites', f'Expected URL to be http://localhost:3000/my_favourites but got {current_url}'",
  "bdd": "@then('I will be redirected into site localhost:3000/my_favourites')\ndef step_verify_redirection(context):\n    current_url = context.driver.current_url\n    assert current_url == 'http://localhost:3000/my_favourites', f'Expected URL to be http://localhost:3000/my_favourites but got {current_url}'"
}
Do not treat \n as something special, do not format it for me.
If you want to get element by text you should use [contains(text(), \"Go to my favorites\")] instead of [text(), \"Go to my favorites\"]
In first line, do not attach imports to "code" in python meant for execution. Its already taken care of. 
Initialization of driver for python execution is taken care of (driver = webdriver.Firefox()) so do not worry about it neither.
Do not use string interpolation in adnotations(@). It may cause some unforseen issues.
Also please make output in json parseable in python
Return json without that funny json string after ``` and without ``` at all. Just as normal json in string.
When you need to upload picture, modify this snippet code: downloads_file_path = os.path.join(os.path.expanduser("~"), "Downloads", "<name_of_file>")
If feature file ask you to submit a form, find a button element and click it, do not submit a form automatically.
Do not look for elements by their text content.
Find them by their id, Find them by css classes using xpath (even by single, unique css classes), by name of inputs, by type of inputs.
Text content should be at the last place, do not use text content of element.
PLEASE LOOK CAREFULLY AT THE HTML CODE. DO NOT MAKE STUPID MISTAKES LIKE CLICK SUBMIT BUTTON, WHERE IN HTML CODE THERE IS NONE SUBMIT BUTTON.
PLEASE DO NOT USE FINDING ELEMENT BY TEXT.
WHEN YOU MAKE CODE, PLEASE CHECK IF THEY ARE INITIALIZED

[no prose]
"""


class ChatGptService:
  def __init__(self, test=False):
    load_dotenv()
    API_KEY = os.getenv("OPEN_AI_VALUE")
    self.client = OpenAI(api_key=API_KEY)

  def create_single_request(self, html, feature_scenario, text_line):
    user_input = self.get_user_input(html, feature_scenario, text_line)

    if user_input is None:
      return {
        "code": "None",
        "bdd": "None"
      }

    # print("user_input", user_input)
    # print("system_input", system_input)
    response = self.client.chat.completions.create(
      # model="gpt-3.5-turbo-0125",
      model="gpt-4-turbo",
      messages=[
        {"role": "system", "content": system_input},
        {"role": "user", "content": user_input}
      ]
    )

    answer = response.choices[0].message.content
    # print(answer)
    print("Odpowiedz: ", answer)
    answer_dict = json.loads(answer)

    # print(repr(answer))
    # answer = answer.replace("\n", " ")
    print("\n\nResponse: ", answer)
    # answer = answer.replace("json", "")
    # answer_dict = ast.literal_eval(answer)
    print("\n\nAfter ast: ", answer_dict)
    print("After getting hash: ", answer_dict["code"])

    # print("Raw Response:\n", answer)
    # print("\n\n\n")

    # # Clean up response with regex to remove any explanation or unwanted text
    # cleaned_answer = re.sub(r'[^\{\}\[\]":,]+', '', answer).strip()
    # print("Cleaned Response:\n", cleaned_answer)

    # Try parsing as JSON first
    # try:
    #     answer_dict = json.loads(cleaned_answer)
    #     print("Parsed as JSON")
    # except json.JSONDecodeError:
    #     print("Not valid JSON, trying literal_eval")

    #     # If it's not JSON, fall back to literal_eval
    #     try:
    #         answer_dict = ast.literal_eval(cleaned_answer)
    #         print("Parsed using literal_eval")
    #     except (ValueError, SyntaxError):
    #         print("The response could not be parsed as a valid dictionary.")
    #         return None
    
    return answer_dict

    # answer = answer.replace('\n', '\\n')
    # print("\n\n\n\n")
    # print(answer)
    # print("\n\n\n\n")
    # print("\n\n\n\n")
    # print(repr(answer))
    # print("\n\n\n\n")
    # answer = json.loads(answer)

    # print(type(answer))
    # print("response: ", response.choices[0])
    # print(answer)
    # print("\n\n\n\n")
    return answer

  def get_user_input(self, html, feature_scenario, text_line):
    return f"""
    Provide me execution code for text_line {text_line}.
    HTML_code: 
    {html}
    (if upper line says EMPTY, try to intepret this prompt without html. Probably it will be something easy as visit page)
    Feature file: 
    {feature_scenario}
    """

  def get_response(self, feature_scenario):
    ready_file = """from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By"""

    driver = webdriver.Firefox()
    # driver.get("http://localhost:3000/every_input")
    # submit_button = driver.find_element(By.XPATH, "//button[@class='w-full px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2']")
    # submit_button.click()
    # elem = driver.find_element("xpath", "//body")
    # html = elem.get_attribute("outerHTML")
    html = "EMPTY"

    json_data = parse_feature_file(feature_scenario)
    # print(json_data)
    # print(json_data.get("Scenario"))
    for scenario_json in json_data["Scenario"]:
      ready_file = ready_file + "\n\n"
      for given_line in scenario_json["Given"]:
          # ready_file = ready_file + given_line
        
# a = [1, 2, 3]
# try: 
#     print ("Second element = %d" %(a[1]))

#     print ("Fourth element = %d" %(a[3]))

# except:
#     print ("An error occurred")
        # try:
        generated_code = self.create_single_request(html, feature_scenario, given_line)
        print("generated_code: ", generated_code, "\n\n\n\n")
        exec(generated_code["code"])
    #     except Exception as error:
    # # handle the exception
    #       print("An exception occurred:", error) # An exception occurred: division by zero:
    #       print("An exception occurred:", repr(error)) # An exception occurred: division by zero:
    #       print("An exception occurred:", error.args) # An exception occurred: division by zero:

    #       driver.close()
    #       return ready_file + "\n\n You can finish it by yourself. It was some kind of problem here"
        elem = driver.find_element("xpath", "//*")
        html = elem.get_attribute("outerHTML")
        ready_file = ready_file + generated_code["bdd"]
        ready_file = ready_file + "\n"

      for when_line in scenario_json["When"]:
        # print("generated_code: ", generated_code, "\n\n\n\n")
        # exec(generated_code["code"])
        try:
          # generated_code = self.create_single_request(html, feature_scenario, given_line)
          generated_code = self.create_single_request(html, feature_scenario, when_line)
          print("generated_code: ", generated_code, "\n\n\n\n")
          exec(generated_code["code"])
        except Exception as error:
    # handle the exception
          print("An exception occurred:", error) # An exception occurred: division by zero:
          # print("An exception occurred:", error.message) # An exception occurred: division by zero:
          driver.close()
          return ready_file + "\n\n You can finish it by yourself. It was some kind of problem here"
        elem = driver.find_element("xpath", "//*")
        html = elem.get_attribute("outerHTML")
        ready_file = ready_file + generated_code["bdd"]
        ready_file = ready_file + "\n"

      for then_line in scenario_json["Then"]:
        # generated_code = self.create_single_request(html, feature_scenario, then_line)
        # print("generated_code: ", generated_code, "\n\n\n\n")
        # exec(generated_code["code"])
        try:
          # generated_code = self.create_single_request(html, feature_scenario, given_line)
          generated_code = self.create_single_request(html, feature_scenario, then_line)
          print("generated_code: ", generated_code, "\n\n\n\n")
          exec(generated_code["code"])
        except Exception as error:
    # handle the exception
          print("An exception occurred:", error) # An exception occurred: division by zero:
          driver.close()
          return ready_file + "\n\n You can finish it by yourself. It was some kind of problem here"

        elem = driver.find_element("xpath", "//*")
        html = elem.get_attribute("outerHTML")
        ready_file = ready_file + generated_code["bdd"]
        ready_file = ready_file + "\n"

      # request = self.create_single_request(html, feature_scenario, input_line=i)
      # exec(request["code"])
      # ready_file = ready_file + "\n\n\n"
      # ready_file = ready_file + request["bdd"]
      # elem = driver.find_element("xpath", "//*")
      # html = elem.get_attribute("outerHTML")
    driver.close()
    return ready_file