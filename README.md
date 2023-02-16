# repo skeleton  
## Execute Note:  
* a `__init__.py` file shows that the package imports all from underlying modules.  
* always run `python -B xxx.py` file under `autodl` directory in case of relative importing  

## Code Note:
* Base:  
&nbsp;&nbsp;&nbsp;&nbsp;model & layer & frames
* Compute:  
&nbsp;&nbsp;&nbsp;&nbsp;performance & tools & hardware-sensitive  
* Utils:  
&nbsp;&nbsp;&nbsp;&nbsp;data & algo & preprocess  
* Modules:  
&nbsp;&nbsp;&nbsp;&nbsp;customized module blocks/bulks for projs
* Loss:  
&nbsp;&nbsp;&nbsp;&nbsp;customized loss functions for projs
* projs:  
&nbsp;&nbsp;&nbsp;&nbsp;a complete proj needs to implement followings:
    * Dataset
    * Network
    * Trainer
    * Evaluator
    * Predictor

## Work Note:

the online working space must contain following directories:  
* `model`: consisting directory named by the `proj_name` -- save trained params
* `logs`: consisting directory named by the `proj_name`  -- save logs
* `autodl`: `git clone https://github.com/Linhengyang/autodl.git`
---
    model
    ├── transformer
    logs
    ├── transformer
    ├── Code
    │   ├── Base
    │   │   ├── MetaFrames
    │   │   │   ├── Architectures.py
    │   │   │   └── __init__.py
    │   │   ├── RootLayers
    │   │   │   ├── AttentionPools.py
    │   │   │   └── PositionalEncodings.py
    │   │   └── SubModules
    │   │       └── AddLNorm.py
    │   ├── Compute
    │   │   ├── EvaluateTools.py
    │   │   ├── PredictTools.py
    │   │   ├── Trainers.py
    │   │   └── VisualizeTools.py
    │   ├── Loss
    │   │   └── MaskedCELoss.py
    │   ├── Modules
    │   │   └── _transformer.py
    │   ├── Utils
    │   │   ├── Common
    │   │   │   ├── DataAssemble.py
    │   │   │   └── SeqOperation.py
    │   │   └── Text
    │   │       └── TextPreprocess.py
    │   └── projs
    │       ├── mlp
    │       └── transformer
    │           ├── Dataset.py
    │           ├── Evaluator.py
    │           ├── Network.py
    │           ├── Predictor.py
    │           ├── Trainer.py
    │           ├── note.txt
    │           └── settings.py
    ├── Config
    │   ├── __init__.py
    │   └── params.py
    ├── README.md
    ├── main.py
    └── test.py
---