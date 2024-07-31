

This is the complimentary Repo to the Paper **A Goal-Directed Dialogue System for Assistance in Safety-Critical Application**. 


# Set Up

This set-up has been tested on a system `Ubuntu 22.04` both inside docker container and natively. This system has not been tested in windows or inside docker container with windows host. 



## Initial steps 

1. Clone the repository with `git clone https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/ijcai-submission.git `
2. Initialize the submodules with `git submodule update`

## Folder Structure 

After git submodule update, you will have the following folder structure: 

          hovor\*
          plan4dial\*

Hovor is responsible for executing the dialogue while plan4dial is responsible for the generation of the dialogue graph. 

### Plan4Dial


It is strongly recommended using virtual environments if you are not running dockerized versions of the repos. 


1. Make sure that you are at the `ijcai_submission` tag for `plan4dial` using `git checkout ijcai_submission`

4. Note that `rbp.sif` is in Teamdrive for internal use (/spaces/ai-lab/veröffentlichung_paper_vortrag/2024_ijcai). Refer to plan4dial docs on how to get this file from Christian Muise.  

4. To generate the output file from the bot definition, refer to the [plan4dial documentation.](https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/plan4dial/-/blob/local_branch/README.md?ref_type=heads) (local run as well as docker run is possible). Plan4Dial generates `data.prp.json` along with the complete output folder.

### Hovor

 The output folder of Plan4dial is the input hovor.  The output file is passed on as arguement [here](https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/hovor/-/blob/local_experiments/contingent_plan_executor/local_main.py?ref_type=heads#L16). Make sure to change the path. Hovor can also be run either locally or docker. Refer to [the documentation for this](https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/hovor/-/blob/local_experiments/README.md?ref_type=heads).  Local run is used for debugging and development purpose, once debuggin and development is done, you can build the docker image and use it to run the code.  So, if you are only interested in running the code, prefer running inside docker.  If you are interested in debugging and developing, it might be preferable to set up an local environment (however you can attach debugger [using vscode](https://code.visualstudio.com/docs/containers/debug-common)  and achieve the same result, so it is a matter of personal preference). 

1. For Hovor, the defined bot has `web_plan` action type. This is action that we use to generate the plans. It takes `endpoint`, `domain_file` and `problem_file` as default payload. (An example for domain and problem file is in `domain_fond.hddl` and `python_generated.hddl` respectively)  As of right now, we discard `problem_file` value and replace it with a generated file name.#Todo Fix this.  You have to make sure that there is a planner-server running that can return the plan from this call. 

### UPF server

1.  To use an example server: install [unified-planning](https://unified-planning.readthedocs.io/en/latest/) and `FastAPI` 
     1. To install UP use `pip install unified-planning` . Install all the default planning engines using `pip install unified-planning[engines]` If this does not work use `pip install up-aries` to install the aries planning engine.  If you get a numpy error, downgrade numpy using `pip install numpy==1.26.4`
     2. To install FastAPI use `pip install fastapi`
     3. Make sure that you install `python>3.10` The version we used is `3.11.9`.
     4. make sure that you have the correct `dump.json` file inside `create_plan` function. 
     
7. Then you can run the app inside `upf_hierarchical.py` using `uvicorn`. To run the app use`uvicorn server:app --reload` The mapping functions are inside the maps folder. Refer to `instructions_mapping.md` for more details. 
8. You can install it in your base environment but it is recommended that you install it in virtual environment of your choice. 
9. After this is running, you can carry out the conversation and get the corresponding plans via terminal by running `local_main.py` in hovor. This will launch the dialogue inside the terminal. For IJCAI bot, the possiblities on how to respond can be seen from [this file ](https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/plan4dial/-/blame/local_branch/plan4dial/local_data/conversation_alignment_bots/ijcai_bot/ijcai_bot.yml?ref_type=heads#L617).  To use the Flask server, use the file ` python contingent_plan_executor/app.py path/bot_name/output_files`. Make sure you are at the right directory level, since it is important such that relative paths work. <del>There is one more hard-coded path [here](https://git.unibw.de/angewandte-ki-f-r-dynamische-system /hovor/-/blob/local_experiments/contingent_plan_executor/hovor/__init__.py?ref_type=heads#L40) make sure, you change this too for server mode. </del>  In local run, to run hovor from terminal directly use: `python contingent_plan_executor/local_main.py path/bot_name/output_files`. Note that the output path is the path to folder generated by plan4dial. 
10. The above two repos doesn't touch on how to visualize the plans or how to access hovor via API-endpoints. However, we do have have our cockpit interface that can do exactly that. 
 Refer here `https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/js-cockpit` for this. Note that this however requires PANDA planner, because, we are interested in orderings too.

 11. To summarize: 
    
    a. Get plan4dial
    b. Generate output file
    c. Get hovor and run it using the previous output
    d. Run upf server 
    e. Now you should be able to communicate via terminal and generate plans. 
    f. if you want to use the GUI, use the cockpit repo and follow the instructions there. 

# Known Issues

1. If you are using Ubuntu, Docker installed using snap causes issues. Install docker using `apt-get` .
2. You might need to change the Rasa version to `rasa==3.6.1a1` in [requirements.txt file for Plan4Dial](https://git.unibw.de/angewandte-ki-f-r-dynamische-systeme/plan4dial/-/blob/local_branch/requirements.txt?ref_type=heads#L3).
3. While loading inside docker, sometimes Rasa takes a long time to load. Note that hovor cannot work with Rasa. 


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