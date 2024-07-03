# Instructions

1. First take the dump of api call as reference, this should contain all the variables for FOND planning instance 
2. In fond_to_hddl_map.json create mapping to all the HDDL variables that derive from FOND instance . This has to be defined 
    The convention is as Follows, 
        p_is+"VariableTypeInHDDL"+"VariableValueFromFOND"

3. In hddl_objects.json file, make sure that there is a unique text mapping to all the HDDL objects . You can generate it using python

4. In predicate_object_map.json specify which predicate each object in hddl takes. Regex in development
5. In situation_to_task_map.json specify which FOND identifer maps to which top_level_task. Here we rely on the fact that once emergency type has been identified, it doesnt change. 