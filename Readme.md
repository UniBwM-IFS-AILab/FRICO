

This is the complimentary Repo to the Paper **A Goal-Directed Dialogue System for Assistance in Safety-Critical Application**. 


# Set Up

1. clone the repository for plan4dial 

`git clone https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/plan4dial` 


2. clone the repository for hovor

 `git clone https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/hovor ` 

3. switch to `local_branch` and `local_experiments` branch respectively 

4. To generate the output file from the bot definition, refer to the plan4dial documentation. (local run as well as docker run is possible). Plan4Dial generates `data.prp.json` along with the complete output folder,  which is the input to Hovor. Hovor can also be run either locally or docker. Refer to the respective documentation for this tutorial. 

5. The defined bot has `web_plan` action type. This is action that we use to generate the plans. It takes `endpoint`, `domain_file` and `problem_file` as default payload. (An example for domain and problem file is in `domain_fond.hddl` and `python_generated.hddl` respectively)  As of right now, we discard `problem_file` value and replace it with a generated file name.#Todo Fix this.  You have to make sure that there is a planner-server running that can return the plan from this call. 

6.  To use an example server: install [unified-planning](https://unified-planning.readthedocs.io/en/latest/) and `FastAPI`
7. Then you can run the app inside `upf_hierarchical.py` using `uvicorn`. The mapping functions are inside the maps folder. Refer to `instructions_mapping.md` for more details. 
8. You can install it in your base environment but it is recommended that you install it in virtual environment of your choice. 
9. After this is running, you can carry out the conversation and get the corresponding plans via terminal by running `local_main.py` in hovor.  
10. The above two repos doesn't touch on how to visualize the plans or how to access hovor via API-endpoints. However, we do have have our cockpit interface that can do exactly that. 
 Refer here `https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/js-cockpit` for this. Note that this however requires PANDA planner, because, we are interested in orderings too.

 11. To summarize: 
    
    a. Get plan4dial
    b. Generate output file
    c. Get hovor and run it using the previous output
    d. Run upf server 
    e. Now you should be able to communicate via terminal and generate plans. 
    f. if you want to use the GUI, use the cockpit repo and follow the instructions there. 


# Citation 

This repo is part of the IJCAI Human-Centered AI Special Track paper A Goal-Directed Dialogue System for Assistance in Safety-Critical Application. 
To cite this paper use: 


```
@inproceedings{goaldirectedJamakatel,
author= {Prakash Jamakatel and Rebecca De Venezia  and Christian Muise and Jane Jean Kiam},
year = {2024},
title = {A Goal-Directed Dialogue System for Assistance in Safety-Critical Application},
booktitle={{International Joint Conference on Artificial Intelligence Special Track Human-Centered AI}} 
  }```