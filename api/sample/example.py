import logging

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from api.response import NamedServer_Response
from django import forms

from PIL import Image
import pandas as pd

logger = logging.getLogger(__name__)


class JsonAPI(APIView):
    """ Postman 을 활용해서 테스트를 진행할 경우, Request 전송방식을 raw(type=json) 으로 지정해줘야 합니다 """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        :action:
            application/json (raw) 형식으로 parameter 를 입력받아 내용을 파싱한 후, json 포맷으로 동일하게 응답합니다.
            Django 에서 json Request 와 그 처리를 위한 예시 API 입니다.

        :param: request parameter
            "param0": (bool)
            "param1": (int)
            "param2": (float)
            "param3": (str)
            "param4": (dict)
            "param5": (list)
            "session": (str) 선택 파라미터 - default: "test_session"

            Test Json Raw
            {
                "param0": false,
                "param1": 5,
                "param2": 2.4,
                "param3": "flask",
                "param4": {
                    "arg1": 1,
                    "arg2": 2
                },
                "param5": [9, 8.8, {"s": 7}],
                "session": "test_session"
            }

        :return: response payload
            request parameter 와 동일한 값을 동일하게 응답합니다.
            "param0": (bool)
            "param1": (int)
            "param2": (float)
            "param3": (str)
            "param4": (dict)
            "param5": (list)
            "session": (str) 선택 파라미터 - default: "test_session"
        """
        args = dict()
        args["param0"] = request.data.get("param0")
        args["param1"] = request.data.get("param1")
        args["param2"] = request.data.get("param2")
        args["param3"] = request.data.get("param3")
        args["param4"] = request.data.get("param4")
        args["param5"] = request.data.get("param5")
        args["session"] = request.data.get("session", "test_session")

        # 필수 Parameter Check
        required_parameters = ['param0', 'param1', 'param2', 'param3', 'param4', 'param5']
        if any(args[rq] is None for rq in required_parameters):
            logger.error(args)
            return NamedServer_Response(
                400,
                "파라미터가 존재하지 않습니다",
                {}
            )

        # 최종 정상 응답
        return NamedServer_Response(
            200,
            "파라미터를 정상적으로 파싱하였습니다.",
            {"args": args}
        )


class UploadFileForm(forms.Form):
    """
    데이터를 어떠한 필드로 받을지 지정합니다.
    해당 필드에 적합한 데이터가 존재하는 경우, class 의 내부 변수 self.is_valid = True 로 호출될 수 있습니다
    각 필드의 데이터 존재 여부에 대해 And 형식으로 동작하므로 이곳에서 언급한 모든 필드의 데이터가 존재 해야
    self.is_valid = True 로 나타납니다
    아무 필드도 지정하지 않는 경우 (설령 입력되는 파일이 없더라도) self.is_valid 의 Default 값인 True 가 출력됩니다
    """
    # title = forms.CharField()
    image = forms.FileField()
    dataframe = forms.FileField()


class FormDataAPI(APIView):
    """ Postman 을 활용해서 테스트를 진행할 경우, Request 전송방식을 form-data 로 지정해줘야 합니다
        text 를 받는 경우, key(type=text) , File 이 입력되는 경우 key(type=file) 로 지정해줘야 합니다
        테스트용 Image & CSV 파일 처리를 위해, Pillow, Pandas 라이브러리가 필요합니다 """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        :action:
            form-data 형식으로 parameter 와 file 을 입력받아, 업로드 된 file 의 내부 정보를 응답합니다.
            Django 에서 파일 Request 와 그 처리를 위한 예시 API 입니다.

        :param: request parameter
            "is_save": (int) 업로드 된 파일의 저장 여부. 0 or 1
                        ! 주의 ! : form-data 형식의 경우, 모든 파라미터는 str 타입으로 파싱합니다.
            "image": (file) Image File
            "dataframe": (file) CSV File

        :return: response payload
            "is_save": (bool) 업로드 된 파일의 저장 여부
            "image": {
                "width": (int) 업로드 된 이미지의 가로 픽셀
                "height": (int) 업로드 된 이미지의 세로 픽셀
            },
            "dataframe": {
                "columns": (list) 업로드 된 dataframe 의 columns
                "length": (int) 업로드 된 csv dataframe 의 전체 데이터 길이
        """
        args = dict()
        args["is_save"] = request.data.get("is_save", "0")  # Save True=1 / False=0
        args["image"] = request.data.get("image")
        args["dataframe"] = request.data.get("dataframe")

        # 필수 Parameter Check
        required_parameters = ["image", "dataframe"]
        if any(args[rq] is None for rq in required_parameters):
            logger.error(args)
            return NamedServer_Response(
                400,
                "파라미터가 존재하지 않습니다",
                {}
            )

        # 'is_save' Parameter Type Check
        if args['is_save'] == "0" or args['is_save'] == "1":
            args['is_save'] = bool(int(args['is_save']))
        else:
            return NamedServer_Response(
                400,
                f"Boolean 처리 할 수 없는 파라미터 입니다. 0 또는 1 값이여야 합니다. input: {args['is_save']}",
                {}
            )

        # Get Uploaded File
        form = UploadFileForm(request.POST, request.FILES)
        args["image"] = request.FILES["image"]
        args["dataframe"] = request.FILES["dataframe"]

        """
        # File Form 에 대한 사용 가이드
        print(">" * 30)
        print(form)
        print(form.files)

        print("=" * 10)
        print(args["image"])  # 파일 이름 출력
        print(args["image"].file.read())
        # 파일의 BytesIO 정보 출력 - read() 실행 시 커서가 파일의 맨 마지막으로 이동하므로 이에 주의

        print(args["image"].size)  # 파일 용량 (Byte)
        print(args["image"].content_type)  # 파일의 타입
        print("<" * 30)
        """

        if form.is_valid():
            # Read Files
            image = Image.open(args['image'])  # type : PIL.Image
            dataframe = pd.read_csv(args['dataframe'])  # type : pandas.DataFrame
        else:
            return NamedServer_Response(
                400,
                "처리 할 수 없는 형식의 파일이 포함되어 있습니다.",
                {}
            )

        if args['is_save']:
            image.save("save.png")
            dataframe.to_csv("save.csv")
            logger.info("Save Files")

        # 최종 정상 응답
        return NamedServer_Response(
            200,
            "파일과 파라미터를 정상적으로 처리하였습니다.",
            {
                "is_save": args['is_save'],
                "image": {
                    "width": image.size[0],
                    "height": image.size[1]
                },
                "dataframe": {
                    "columns": dataframe.columns.tolist(),
                    "length": len(dataframe)
                }
            }
        )
