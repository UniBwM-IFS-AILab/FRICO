# Instructions

1. First take the dump of api call as reference, this should contain all the variables from the  FOND planning instance. This is in `state_variables_dump.json`. Make sure that the output the output of web_plan action from hovor is correctly pointed inside `create_plan` endpoint.  This is not the same file that we provide here for reference but should be the output path from hovor. 
2. `hddl_objects_python` and `hddl_objects` files contain the name for the  hddl object variables to be  instantiated. In `hddl_objects_python` we just add the subscript 1. Note that this is only needed for Aries Planner. When using PandaPlanner, this does not seem to be an issue. We just provide two possibilities here, so as to have an initial point for when the model will be more complex later on. 
3. The script for generating the mapping is inside `hddl_processing.ipynb`
4. `predicate_object_map` contains information on which predicate takes which objects. 
5. In situation_to_task_map.json specify which FOND identifer maps to which top_level_task. Here we rely on the fact that once emergency type has been identified, it doesnt change. 


# Notes 
    1. The mapping is as of right now very rudimentary. This has to extended to include regex and more capable functions. This will be further developed, when we know the final scenario for the final experiments. 

    2. in `fond_map` dictionary  we map which values are required for which emergency type. This of course can be extended to calibrate with the richness of HDDL model.  We only show here a simplified example.  
2. In fond_to_hddl_map.json create mapping to all the HDDL variables that derive from FOND instance . This has to be defined 
    The convention is as Follows, 
        p_is+"VariableTypeInHDDL"+"VariableValueFromFOND"

3. In hddl_objects.json file, make sure that there is a unique text mapping to all the HDDL objects . You can generate it using python

4. In predicate_object_map.json specify which predicate each object in hddl takes. Regex in development
5. In situation_to_task_map.json specify which FOND identifer maps to which top_level_task. Here we rely on the fact that once emergency type has been identified, it doesnt change. 