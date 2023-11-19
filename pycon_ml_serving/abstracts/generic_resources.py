import json
import falcon

class GenericFalconResources:

    def __init__(self, http_function_map: dict):
        """
        http_function_map will define which function to call 
        for a particular HTTP Method
        sample: 
            http_function_map = {
                "POST": <predictor.iris.IrisPredictor.predict>
                "GET": <predictor.iris.IrisPredictor.get_historical_data>
            }
        """
        self.http_function_map = http_function_map

    def on_post(self, req, resp):
        _body =  json.loads(req.stream.read().decode('utf-8'))
        prediction = self.http_function_map["POST"](_body)
        json_data = json.dumps(prediction)

        # Set response headers
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200

        # Set response body
        resp.body = json_data
    
