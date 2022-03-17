import json

import requests
from rest_framework import generics
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from ml.models import *

from .models import UserRequest
from .serializers import ModelSerializer
from datetime import datetime

# Logging
import logging
import traceback
logger = logging.getLogger(_name_)
f_handler = logging.FileHandler("logs/debug.log")
logger.addHandler(f_handler)

def count_api_call(user_model, count):
    """user_model is object of MlModels to which user is making call and
    Count is number of requests made by user"""

    user_api_requests = UserRequest.objects.filter(model = user_model)

    # If Instance of model already exists in UsersRequest then add count to previous api count
    if user_api_requests.exists():
        user_api_requests = user_api_requests[0]
        api_count = user_api_requests.api_requests
        user_api_requests.api_requests = api_count + count
        user_api_requests.save()
    else:
        first_api_request = UserRequest.objects.create(
            model = user_model,
            User = user_model.user,
            api_requests = count
        )
        first_api_request.save()


class CustomAccessPermission(BasePermission):
    """Giving access if User is authenticated or apikey is valid"""

    """request is call made by User, and it checks that if user or apikey is authentic"""
    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return True

        # request can be made by Restframework, python requests and curl
        # Based on all three type of requests "api_key" is found
        apikey = request.POST.get("api_key", None)
        if request.data and apikey == None:
            apikey = request.data.get("api_key", None)
            if apikey == None:
                apikey =request.POST.get("data")
                apikey = json.loads(request.POST.get("data"))["api_key"]

        # if apikey id valid
        if apikey:
            key = MlModels.objects.filter(api_key = apikey)
            if key.exists():
                return True
        return False


class ModelView(generics.ListCreateAPIView):
    serializer_class = ModelSerializer
    permission_classes = [CustomAccessPermission]

    def get_queryset(self):
        pass

    """ POST method takes all data of user and returns JSON data either exception 
        message or processed data from model """
    def post(self, request):
        user_model = None
        input_type = None
        recieved_code_list = None
        files_list = []

        files = request.FILES.getlist("files", None)
        text  = request.POST.get("text", None)
        if request.data and text == None:
            text  = request.data.get("text", None)
        
        # If user sends both (files, text)
        if files  and text:
            return Response({
                "error":"Add one, file or text"
            })

        # request can be made by Restframework, python requests and curl
        # Based on all three type of requests "api_key" is found
        apikey = request.POST.get("api_key", None)
        if apikey == None:
            apikey = request.data.get("api_key", None)
            if apikey == None:
                apikey =request.POST.get("data")
                apikey = json.loads(request.POST.get("data"))["api_key"]

        model = MlModels.objects.filter(api_key = apikey)

        # if model is found then set some variables which are used
        # to verify User's request and make requests to Backend Model
        if model.exists():
            user_model = model[0]
            model_ip_address =  model[0].model_ip_address

            # BASE_URL/output is BackendModel Endpoint to recieve Processed data of model
            output_link = model_ip_address + "output"
            input_type = model[0].model_input_format
            output_type = model[0].model_output_format
        else:
            return Response({
                "error":"Incorrect Apikey"
            })



        # If user has sent some files then match format of files to format of model
        if files:
            for file in files:
                files_list.append(("file", (file)))
                file_type = file.content_type

                if file_type:
                    this_file_type = file_type.split("/")
                    if this_file_type[0] != input_type:
                        return Response({
                            "error":"incorrect file type"
                        })
                    elif this_file_type[0] == input_type  and this_file_type[0] == "text" and this_file_type[1] != "plain":
                        return Response({
                            "error":"incorrect file type"
                        })

            #if User has send some image files
            if input_type == "image" and files_list != []:
                try:
                    # Sending Data to Backend Model
                    data = requests.post(model_ip_address, files=files_list)
                except Exception as e:
                    logger.error("\n" + str("="*30) + str("\napi/views.py line 144")
                                    + "\nTimeStamp:" + str(datetime.now()) + "\n" + str(e)
                                    + "\nTraceBack:" + traceback.format_exc())
                    return Response({
                        "error":"Model not connected"
                    },status=404)
                recieved_code_list = data.json()["code_list"]

            elif input_type == "text":

                text = file.read()
                try:
                    text = text.decode("utf-8")
                except Exception as e:
                    logger.error("\n" + str("="*30) + str("\napi/views.py line 157") 
                                + "\nTimeStamp:" + str(datetime.now()) + "\n" + str(e)
                                + "\nTraceBack:" + traceback.format_exc())
                    return Response({
                            "error":"incorrect file type"
                        })
                input_data = {"text":text}
                data = requests.post(model_ip_address, json = input_data)

                # Backend Model will take data and insert data inside a Queue and sends their ids as "code_list"
                # This code_list is used to get processed data from model
                recieved_code_list = data.json()["code_list"]
            if recieved_code_list:
                input_data = {"code_list":[recieved_code_list[0]]}
                try:
                    data = requests.post(output_link, json = input_data)
                except Exception as e:
                    logger.error("\n" + str("="*30) + str("\napi/views.py line 173") 
                                + "\nTimeStamp:" + str(datetime.now()) + "\n" + str(e)
                                + "\nTraceBack:" + traceback.format_exc())
                    return Response({
                        "error":"Model not connected"
                    },status=404)
                count_api_call(user_model, len(recieved_code_list))

                # Processed data from model
                return Response({
                    "type":output_type,
                    "output":data.json()["result_list"][0]["image"]
                })

        elif text and input_type == "text":
            input_data = {"text":text}
            try:
                data = requests.post(model_ip_address, json = input_data)
            except Exception as e:
                logger.error("\n" + str("="*30) + str("\napi/views.py line 192") 
                            + "\nTimeStamp:" + str(datetime.now()) + "\n" + str(e)
                            + "\nTraceBack:" + traceback.format_exc())
                return Response({
                    "error":"Model not connected"
                },status=404)
            recieved_code_list = data.json()["code_list"]

            if recieved_code_list:
                input_data = {"code_list":[recieved_code_list[0]]}
                try:
                    data = requests.post(output_link, json = input_data)
                except Exception as e:
                    logger.error("\n" + str("="*30) + str("\napi/views.py line 204") 
                            + "\nTimeStamp:" + str(datetime.now()) + "\n" + str(e)
                            + "\nTraceBack:" + traceback.format_exc())
                    return Response({
                        "error":"Model not connected"
                    },status=404)
                count_api_call(user_model, len(recieved_code_list))
                return Response({
                    "type":output_type,
                    "output":data.json()["result_list"][0]["image"]
                })

        # if Backend model did not returned any response
        if recieved_code_list == None:
            return Response({
                    "error":"Model not connected"
                },status=404)
        return Response({
                    "error":"Incorrect Data"
                },status=404)