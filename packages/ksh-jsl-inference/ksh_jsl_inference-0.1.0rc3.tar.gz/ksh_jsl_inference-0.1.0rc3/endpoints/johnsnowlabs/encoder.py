from johnsnowlabs.nlp import Annotation
import json


class AnnotationEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Annotation):

            return {
                "begin": o.begin,
                "end": o.end,
                "result": o.result,
            }
        return json.JSONEncoder.default(self, o)
