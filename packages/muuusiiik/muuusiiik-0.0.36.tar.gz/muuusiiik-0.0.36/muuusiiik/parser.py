def json_update(data, input_value, output_value, parent_node='', parents=['']):
    """
    input parameters
    data:dict = dict type variable.
    input_value:dict = dict key and value that you want to check matching.
    output:dict = dict key and value that you want to upate value.
    parent_node:str = parents key, leave it blank if you need to update only 1st level of dict.
    
    example:
    ----------------------
    data = {'botname': 'apollo',
     'linetoken': 'nXexNPQNE/7GU+TuUITd3eOI3xFKupMgs4l2GBr3s9WpOPFCtLGMa1',
     'webhook': 'https://abdul.in.th/lite/wh/komyo/1dafdacbdc9a8fd434928ad2bb8d0b14.php',
     'apikey': 'xxx',
     'botid': '1dafdacbdc9a8fd434928ad2bb8d0b14',
     'ownerid': 'komyo',
     'category': '',
     'objective': '',
     'knowledge': [{'name': 'Conversation',
       'id': '1Crt9HIHzXG1Wv_wDD48QGoj400NLUBuU0YQiIAG2OXs',
       'type': 'cu'},
      {'name': 'FAQ',
       'id': '1Crt9HIHzXG1Wv_wDD48QGoj400NLUBuU0YQiIAG2OXs',
       'type': 'faq'}],
     'idea': {'ownerid': 'komyo',
      'type': 'cu',
      'more_idea': {'type': 'cu', 'types': ['sam', 'cu', 2]}}}
      
    input_value = {'ownerid': 'komyo'}
    
    output_value = {'type': 'sam'}
    parent_node = 'idea' 
    
    
    output :
    ----------------------
    {'botname': 'apollo',
     'linetoken': 'nXexNPQNE/7GU+TuUITd3eOI3xFKupMgs4l2GBr3s9WpOPFCtLGMa1',
     'webhook': 'https://abdul.in.th/lite/wh/komyo/1dafdacbdc9a8fd434928ad2bb8d0b14.php',
     'apikey': 'xxx',
     'botid': '1dafdacbdc9a8fd434928ad2bb8d0b14',
     'ownerid': 'komyo',
     'category': '',
     'objective': '',
     'knowledge': [{'name': 'Conversation',
       'id': '1Crt9HIHzXG1Wv_wDD48QGoj400NLUBuU0YQiIAG2OXs',
       'type': 'cu'},
      {'name': 'FAQ',
       'id': '1Crt9HIHzXG1Wv_wDD48QGoj400NLUBuU0YQiIAG2OXs',
       'type': 'faq'}],
     'idea': [{'ownerid': 'komyo',
       'type': 'sam',
       'more_idea': {'type': 'cu', 'types': ['sam', 'cu', 2]}}]}
    """
    output_key = list(output_value.keys())[0]
    input_key = list(input_value.keys())[0]
    
    for key, value in data.items():
        # check key is equal to input key 
        if key == input_key and value == input_value[input_key] and \
                output_key in data.keys() and parent_node in parents:
            #
            data[output_key] = output_value[output_key]

        elif isinstance(value, list):
            for idx, item in enumerate(value):
                # check type dict
                if isinstance(item, dict):
                    json_update(item, input_value, output_value, parent_node, list(data.keys()))
                    
    return data
