{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.6.6","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kaggle":{"accelerator":"none","dataSources":[{"sourceId":196650875,"sourceType":"kernelVersion"},{"sourceId":198180640,"sourceType":"kernelVersion"},{"sourceId":198108206,"sourceType":"kernelVersion"}],"dockerImageVersionId":29860,"isInternetEnabled":false,"language":"python","sourceType":"script","isGpuEnabled":false}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [code]\n# This Python 3 environment comes with many helpful analytics libraries installed\n# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python\n# -*- coding: utf-8 -*-\n\"\"\"\nCreated on Fri Mar 20 10:29:31 2020\n\n@author: YannCLAUDEL\n\nThe function ipynbtopy(input_dir) convert all files *.ipynb to *.py \nThe targets files *.py are created in a directory pysrc\n\"\"\"\n\nimport json\nimport os\n\ndef ipynbtopyParse(fileIn,fileOut):\n\n    with open(fileIn) as json_file:\n        data = json.load(json_file)\n    \n    out = open(fileOut,\"w\")\n    \n    for cell in data['cells']:    \n        if (cell.get('cell_type')!=None and cell.get('cell_type')=='markdown'):\n            lines = cell.get('source')\n            if len(lines)>0:\n                out.write(\"# \"+str(lines[0]).replace(\"#\", ''))\n                out.write(\"\\n\")\n        if (cell.get('cell_type')!=None and cell.get('cell_type')=='code'):\n            for line in cell.get('source'):\n                out.write(line)\n            out.write(\"\\n\\n\")\n        # out.write(\"\\n\")\n            \n    out.close()\n\n\ndef ipynbtopy(input_dir):\n    for dirname, dirnames, filenames in os.walk(input_dir):\n        # print path to all subdirectories first.\n        # for subdirname in dirnames:\n        #     print(os.path.join(dirname, subdirname))\n    \n        # print path to all filenames.\n        for filename in filenames:\n            if filename.endswith(\".ipynb\"):\n                newfilename = filename[:-6]+\".py\"\n                newdirname = dirname+r\"\\pysrc\"\n                if not os.path.exists(newdirname):\n                    os.mkdir(newdirname)\n                ipynbtopyParse(os.path.join(dirname, filename),os.path.join(newdirname, newfilename))\n                \n        # Advanced usage:\n        # editing the 'dirnames' list will stop os.walk() from recursing into there.\n        if '.git' in dirnames:\n            # don't go into any .git directories.\n            dirnames.remove('.git')\n        if '.ipynb_checkpoints' in dirnames:\n            # don't go into any .git directories.\n            dirnames.remove('.ipynb_checkpoints')\n\ninput_dir=\"/kaggle/input/notebooked5ecf376b\"\nipynbtopy(input_dir)","metadata":{"_uuid":"f15687e5-ebd5-4eb7-908f-45980fc4d28b","_cell_guid":"0d0ce1d2-2ea1-43ba-ada3-d93bd7607af9","collapsed":false,"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2024-09-25T10:53:40.761109Z","iopub.execute_input":"2024-09-25T10:53:40.761571Z","iopub.status.idle":"2024-09-25T10:53:40.766962Z","shell.execute_reply.started":"2024-09-25T10:53:40.761512Z","shell.execute_reply":"2024-09-25T10:53:40.765592Z"},"trusted":true},"execution_count":1,"outputs":[]}]}