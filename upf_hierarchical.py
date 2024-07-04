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




fond_map = {
    "fire_emergency": {"location", "fire_smell", "fire_color"},
    "landing_gear_malfunction": {"landing_gear_specifier"}, 
    "health_emergency": {"physical_health_emergency", "mental_health_emergency"}
}



with open("maps/situation_to_task_map.json") as f: 
    scenario_tasks_dict = json.load(f)

with open("maps/hddl_objects.json") as f: 
    hddl_objects = json.load(f)
with open("maps/predictate_object_map.json") as f: 
    predicate_object_map = json.load(f)

indent = " " * 4
newline = "\n"  

def generate_hddl_file(file_path, objects, subtasks, inits):
    content = f"""(define (problem problemSimplified)
        {indent}(:domain airplaneDomain)
        {indent}(:objects
        {indent}{indent}{newline.join([f'{indent+ item}' for item in objects])}
        {indent})

        {indent}(:htn
        {indent}{indent}:subtasks
        {indent}{indent}(and
        {indent}{indent}{indent}{newline.join([f'{item}' for item in subtasks])}
        {indent}{indent})
        {indent}{indent}; Add subtasks here
        {indent})

        {indent}(:init     
        {indent}{indent}; Add initial state here
        {indent}{indent}{newline.join([f'({item})' for item in inits])}
        {indent})
    )
    """

    # Write the content to the file
    with open(file_path, 'w') as file:
        file.write(content)








def determine_instant_from_dump(fond_result,task_map, hddl_predicate_arguments_object, hddl_objects_shorthand):
    inits = []
    print(fond_result["emergency_type"])
    subtasks = task_map[fond_result["emergency_type"]]
    print(subtasks)
    match fond_result["emergency_type"]: 
        
        case "smoke_unknown_location_and_fire_known" | "smell_known_location_required" | "smoke_known_location_required":
            
            for i in fond_map["fire_emergency"]: 
                
                fond_value = fond_result[i]
                
                if fond_value == "engine": 
                    
                    inits.append("p_isEngineFire"+ " "+hddl_objects_shorthand[hddl_predicate_arguments_object["p_isEngineFire"]])
                
                elif fond_value == "wing": 
                    inits.append("p_isWingFire"+" "+hddl_objects_shorthand[hddl_predicate_arguments_object["p_isWingFire"]])
                    
                elif fond_value == "electric": 
                    inits.append("p_isElectricFire"+" "+hddl_objects_shorthand[hddl_predicate_arguments_object["p_isElectricFire"]])
                    inits.append("p_isOn"+" "+ "mas")
                    inits.append("p_isOn"+" "+ "mbs")

        
        case "landing_gear_malfunction_emergency": 
            

            
            for i in fond_map["landing_gear_malfunction"]: 
                
                fond_value = fond_result[i]
                
                if fond_value == "side": 
                    
                    inits.append("p_isSide"+ " " +hddl_objects_shorthand[hddl_predicate_arguments_object["p_isSide"]])
                
                elif fond_value == "nose": 
                    inits.append("p_isNose" +" " +hddl_objects_shorthand[hddl_predicate_arguments_object["p_isNose"]])

        case "physical_health_emergency":
            if fond_result["mental_state_description"]: 
                inits.append("p_isMental"+ " " +hddl_objects_shorthand[hddl_predicate_arguments_object["p_isMental"]])
                    #This is to catch the case wether it is also a mental health emergency. The bot asks if there are any physical issues after mental health request. This needs to be resolved. 
            else: 
                inits.append("p_isPhysical"+ " " +hddl_objects_shorthand[hddl_predicate_arguments_object["p_isPhysical"]])
            
            
            
        
        case _:
            return "something went wrong"
            
             
           
           

        
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
async def create_plan(item: Item) -> str: 
    
    domain_path = item.domain_file 
    problem_path = item.problem_file
    with open("maps/dump.json") as f:   # This is a reference from the dump made by hovor. See webactionsplan class in hovor for where it is.  
        fond_result_dict = json.load(f)
    time.sleep(3)
    domain_path = "domain/domain_fond.hddl"
    file_path = 'python_generated.hddl'
    objects = [f"{v} - {k}" for k, v in hddl_objects.items()]
    initial, subtasks= determine_instant_from_dump(fond_result_dict,scenario_tasks_dict, predicate_object_map, hddl_objects)
    generate_hddl_file(file_path,objects,subtasks,initial)
    reader = up.io.PDDLReader()
    hierarchical_problem = reader.parse_problem(domain_path, file_path)
    
    plan_text = return_text_from_solve(hierarchical_problem)
    print((plan_text))

    return plan_text
  