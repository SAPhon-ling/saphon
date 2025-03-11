#CreateDropdownAndNestedDropdowns i.e. for undergoers in processes field, we also create another dropdown for type, morpheme_class, and positional_restriction
import yaml
import os
from pathlib import Path
import json
"""
    <form id = "processesFilterForm" action="#">
        <label for="processes">Processes: </label>
        <select name="processes" id="processes">
            <option value="">Select a process</option>
            <option value="LDNH">LDNH</option>
            <option value="LO">LO</option>
        </select>
        <select name="direction" id="direction">
            <option value="">Select a direction</option>
            <option value="left">Leftward</option>
            <option value="bidirectional">Bidirectional</option>
            <option value="right_Ṽ">Rightward</option>
        </select>
        <button id="addProcess">Add</button>
        <div id="containerX"></div>
    </form>
"""

newLangsYAMLFolderDirectory = '../../../newLangsYaml'
newLangsJSONFolderDirectory = '../../../newLangsJSON'
yamlFolderPath = os.path.abspath(os.path.join(os.getcwd(), newLangsYAMLFolderDirectory))
jsonFolderPath = os.path.abspath(os.path.join(os.getcwd(), newLangsJSONFolderDirectory))

for jsonFile in os.listdir(jsonFolderPath):
    baseFileName = Path(jsonFile).stem
    with open(os.path.join(jsonFolderPath, jsonFile), "r", encoding="utf-8") as f:
        languageJSON = json.load(f)






