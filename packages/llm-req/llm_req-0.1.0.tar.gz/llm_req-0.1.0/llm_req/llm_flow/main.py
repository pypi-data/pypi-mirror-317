## write a flask
""" from flask import Flask"""
import tempfile
from flask import  Flask, render_template, request, redirect, url_for, session, flash, jsonify,send_from_directory
import os
import pandas as pd
import json
from llm_req import ExcelDataAgent, JsonAgent, Agent
from llm_req import list_agent, load_agent
from loguru import logger

current_path = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)
app.secret_key = 'mysecretkey'
# config static folder in ./dist
# config map static uri /assets to ./dist/assets
app.template_folder = os.path.join(current_path ,'dist' )
# 配置静态文件路径
app.config['STATIC_FOLDER'] = os.path.join(current_path,'dist','assets')
app.config['STATIC_URL_PATH'] = os.path.join(current_path,'dist','assets')

# 提供静态文件
@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

@app.route('/')
def index():
    return render_template('index.html')

# write a file upload
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # allow only txt md excel files
        if file.filename.endswith('.txt') or file.filename.endswith('.md') or file.filename.endswith('.xlsx')or  file.filename.endswith('.csv'):
            # save file to temp file
            temp_dir = tempfile.gettempdir()
            file.save(os.path.join(temp_dir, file.filename))
            if file.filename.endswith('.xlsx'):
                reply_data = []
                for no,i in enumerate(pd.read_excel(os.path.join(temp_dir, file.filename)).fillna('').iloc):
                    item = i.to_dict()
                    item["id"] = no
                    reply_data.append(item)
                return jsonify({
                    "data":reply_data,
                    "name":file.filename,
                })
            elif file.filename.endswith('.csv'):
                reply_data = [ ]
                for no,i in enumerate(pd.read_csv(os.path.join(temp_dir, file.filename)).fillna('').iloc):
                    item = i.to_dict()
                    item["id"] = no
                    reply_data.append(item)

                # reply json

                return jsonify({
                    "data":reply_data,
                    "name":file.filename,
                })
            else:
                with open(os.path.join(temp_dir, file.filename), 'r') as f:
                    reply_data = f.read()
                    # reply json
                    return jsonify({
                        "data":reply_data,
                        "name":file.filename,
                    })
        else:
            return jsonify({
                "error":"file type not supported"
            })
    else:
        return jsonify({
            "error":"no file uploaded"
        })

@app.route('/list_agent', methods=['POST'])
def post_list_agent():
    if request.method == 'POST':
        # get target, points , example from request in json type
        return jsonify(list_agent())
    else:
        return jsonify({
            "error":"no file uploaded"
        })

@app.route('/get_batch', methods=['POST'])
def post_get_batch():
    if request.method == 'POST':
        # get target, points , example from request in json type
        data = request.json
        # logger.info(data)
        target = data.get('target','')
        points = data.get('points',[])
        example = data.get('example','')
        useJson = data.get('useJson', False)
        name = data.get('name','')
        dataitems = data.get("data", [])
        model = data.get('model','')
        model_api = data.get('model_api','')
        batch_size = data.get('batch_size', 10)
        threads = data.get('threads', 1)
        
        if name.strip() == '':
            return jsonify({
                "error":"no name provided"
            })
        if useJson:
            ag = JsonAgent(*points,target=target)
        else:
            ag = Agent(*points,target=target)
        if example.strip() != "":
            ag.set_example(example)
        ag.batch_size = int(batch_size)
        ag.threads = threads
        ag._data = dataitems

        batchs = []
        
        for pre in ag.output(batch_size = ag.batch_size):
            # logger.info(pre)
            batchs.append(pre)
        logger.success(f"data:{len(dataitems)} batch size: {ag.batch_size} data: {len(batchs)}")
        
        # logger.success(ag)
        return jsonify({
            "data":batchs   
        })
    else:
        return jsonify({
            "error":"no file uploaded"
        })
    
@app.route('/get_preview', methods=['POST'])
def post_get_preview():
    if request.method == 'POST':
        # get target, points , example from request in json type
        data = request.json
        logger.info(data)
        target = data.get('target','')
        points = data.get('points',[])
        example = data.get('example','')
        useJson = data.get('useJson', False)
        name = data.get('name','')
        dataitems = data.get("data", [])
        model = data.get('model','')
        model_api = data.get('model_api','')
        
        if name.strip() == '':
            return jsonify({
                "error":"no name provided"
            })
        items = data.get('data',[])
        if useJson:
            ag = JsonAgent(*points,target=target)
        else:
            ag = Agent(*points,target=target)
        # ag.set_target(target)
        if len(items) > 0:
            ag |= items
        # if len(points) > 0:
        #     ag.set_point(*points)
        
        if example.strip() != "":
            ag.set_example(example)
        ag |= dataitems
        logger.success(ag)
        ag.set_llm(model, model_api)
        return jsonify({
            "data": str(ag),
        })
    else:
        return jsonify({
            "error":"not post method"
        })
                # reply json

@app.route('/load_agent', methods=['POST'])
def post_load_agent():
    if request.method == 'POST':
        # get target, points , example from request in json type
        data = request.json
        name = data.get('name', '')
        if name != "" and name in list_agent():
            logger.info(f"load {name} ....")
            oo = load_agent(name)
            dd = oo.to_dict()
            dd["name"] = name
            if isinstance(oo, JsonAgent):
                dd["useJson"] = True
            logger.info(f"load agent {name} success")
            return jsonify(dd)
        else:
            return jsonify({
                "error":"no name provided"
            })
        
@app.route('/save_agent', methods=['POST'])
def post_make_agent():
    if request.method == 'POST':
        # get target, points , example from request in json type
        data = request.json
        logger.info(data)
        target = data.get('target','')
        points = data.get('points',[])
        example = data.get('example','')
        useJson = data.get('useJson', False)
        name = data.get('name','')
        model = data.get('model','')
        model_api = data.get('model_api','')
        batch_size = data.get('batch_size', 10)
        threads = data.get('threads', 1)
        
        if name.strip() == '':
            return jsonify({
                "error":"no name provided"
            })
        items = data.get('data',[])
        if useJson:
            ag = JsonAgent(*points,target=target)
        else:
            ag = Agent(*points,target=target)
        # ag.set_target(target)
        if len(items) > 0:
            ag |= items
        ag.batch_size = batch_size
        ag.threads = threads
        # if len(points) > 0:
        #     ag.set_point(*points)
        if example.strip() != "":
            ag.set_example(example)
        logger.success(ag)
        ag.set_llm(model, model_api)
        ag.save(name)
        
        return jsonify({
            "data":str(ag),
            "pre": ag.__repr__(),
        })
    else:
        return jsonify({
            "error":"no data provided"
        })





def main():
    import argparse
    parser = argparse.ArgumentParser(description='LLM Flow')
    parser.add_argument('--port', type=int, default=5000, help='port to run the server on')
    args = parser.parse_args()

    if args.port > 0:
        # run threading
        # app.run(debug=True, port=args.port)
        logger.info(f"Starting server on port {args.port}")
        app.run(debug=True, port=args.port, threaded=True)
    
if __name__ == '__main__':
    main()