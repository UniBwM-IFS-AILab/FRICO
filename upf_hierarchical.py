from fastapi import FastAPI
from pydantic import BaseModel, Field, Extra
from typing import Dict, Union

import unified_planning as up
from unified_planning.shortcuts import *
from unified_planning.model.htn import *

import uuid
import json 
import time 
app = FastAPI()



requests_text = []



# with open("state_variables_dump/dump.json") as f: 
#     fond_result_dict = json.load(f)


with open("maps/situation_to_task_map.json") as f: 
    scenario_tasks_dict = json.load(f)

with open("maps/fond_to_hddl_map.json") as f: 
    hddl_predicate_map = json.load(f)
with open("maps/hddl_objects.json") as f: 
    hddl_objects = json.load(f)
with open("maps/predictate_object_map.json") as f: 
    predicate_object_map = json.load(f)



def generate_hddl_file(file_path, objects, subtasks, inits):
    content = f"""(define (problem problemSimplified)
            (:domain airplaneDomain)
            (:objects
                {'\n \t\t\t\t'.join([f'{item}' for item in objects])}
            )

            (:htn
                :subtasks
                (and
                    {'\n \t\t\t\t'.join([f'{item}' for item in subtasks])}
                )
                ; Add subtasks here
            )

            (:init     
                ; Add initial state here
                {'\n \t\t\t\t'.join([f'({item})' for item in inits])}
            )
        )
        """

    # Write the content to the file
    with open(file_path, 'w') as file:
        file.write(content)


def determine_instant_from_dump(fond_result, fond_to_hddl, task_map, hddl_objects, predicate_to_object):
    inits = []
    subtasks = task_map[fond_result["emergency_type"]]
    
    for var in fond_to_hddl: 

        if fond_result[var] != None and fond_result[var]!= False : 
            print(fond_result[var])
            if fond_result[var] == True: 
                hddl_pred = fond_to_hddl[var]
            else: 
                value = "".join(fond_result[var].split(" "))
                value = value.capitalize()
                if fond_to_hddl[var]!="":
                    hddl_pred = fond_to_hddl[var]+value
                    append_str = " "+hddl_objects[predicate_to_object[hddl_pred]]
                    final_str = hddl_pred + append_str
                    inits.append(final_str)
        
    return inits, subtasks

    

class NestedField(BaseModel): 
    key: str 
    value: Union[str, bool, ]

class Item(BaseModel):
    id: int
    domain_file: str
    problem_file: str

    

def return_text_from_solve(pb: Problem, verbose=False):
    result = OneshotPlanner(problem_kind=pb.kind).solve(pb)
    if result.plan is not None:
        return repr(result.plan.action_plan.actions)
    else:
        return "No Plan found: "+ result.status


@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/create_plan")
async def create_wav(item: Item) -> str: 
    
    domain_path = item.domain_file 
    problem_path = item.problem_file
    with open("state_variables_dump/dump.json") as f: 
        fond_result_dict = json.load(f)
    time.sleep(3)
    file_path = 'python_generated.hddl'
    objects = [f"{v} - {k}" for k, v in hddl_objects.items()]
    initial, subtasks= determine_instant_from_dump(fond_result_dict, hddl_predicate_map, scenario_tasks_dict,hddl_objects,predicate_object_map)
    generate_hddl_file(file_path,objects,subtasks,initial)
    reader = up.io.PDDLReader()
    hierarchical_problem = reader.parse_problem(domain_path, file_path)
    
    plan_text = return_text_from_solve(hierarchical_problem)
    print(type(plan_text))

    return plan_text
  