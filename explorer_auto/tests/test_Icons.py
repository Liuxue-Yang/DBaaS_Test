import time
import random
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class Testicons:
    @pytest.mark.icons
    def test_icons_group(self):
        # 创建图标组
        global QA_random
        QA_random = random.randint(1,100000000)
        icons_group = [
            {"name":"test","type":"svg"},
            {"name":"test测试!@#$%!@^!&@&#@%@#","type":"svg"},
            {"name":"test测试!@#$%!@^!&@&#@%@#1234567_超出限制","type":"svg"},
            {"name":"test","type":"svg"}
            ]
        for data in icons_group:
            code = InterfaceExplorer.add_Icon_Group(data).json()["code"]
            assert 0 == code

        # 获取图标组 判断所添加的组
        json_data = InterfaceExplorer.get_Icon_Group().json()
        assert 'test' == json_data["data"]["items"][0]["name"]
        assert 'test测试!@#$%!@^!&@&#@%@#' == json_data["data"]["items"][1]["name"]
        assert 'test测试!@#$%!@^!&@&#@%@#1234567_超出限制' == json_data["data"]["items"][2]["name"]
        assert 'test' == json_data["data"]["items"][3]["name"]

        # 更新不存在的组
        icon_id_Group  = '6666666'
        name = {"name":"QA"}
        code = InterfaceExplorer.put_Icon_Group(icon_id_Group,data).json()["code"]
        assert 50004001 == code

        # 循环更新 超出名称限制、正常的组名称
        icon_id_Group = json_data["data"]["items"][-1]["id"]
        name = [
            {"name":"test测试!@#$%!@^!&@&#@%@#1234567_超出限制"},
            {"name":"QA"}
        ]
        for data in name:
            code = InterfaceExplorer.put_Icon_Group(icon_id_Group,data).json()["code"]
            assert 0 == code

        # 循环添加正确图标、大于2k的图标、重复图标
        icons = [
            {"name":"icon-canvas-search.svg","icon":"<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M10.1384 10.4522C9.16786 11.3471 7.87123 11.8938 6.44691 11.8938C3.43867 11.8938 1 9.45516 1 6.44691C1 3.43867 3.43867 1 6.44691 1C9.45516 1 11.8938 3.43867 11.8938 6.44691C11.8938 7.81306 11.3909 9.06173 10.5601 10.0179L15 14.4578L14.572 14.8858L10.1384 10.4522ZM11.2886 6.44691C11.2886 3.77292 9.12091 1.60521 6.44691 1.60521C3.77292 1.60521 1.60521 3.77292 1.60521 6.44691C1.60521 9.12091 3.77292 11.2886 6.44691 11.2886C9.12091 11.2886 11.2886 9.12091 11.2886 6.44691Z\" fill=\"black\"/>\n</svg>\n"},
            {"name":"icon-canvas-search.svg","icon":"<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M10.1384 10.4522C9.16786 11.3471 7.87123 11.8938 6.44691 11.8938C3.43867 11.8938 1 9.45516 1 6.44691C1 3.43867 3.43867 1 6.44691 1C9.45516 1 11.8938 3.43867 11.8938 6.44691C11.8938 7.81306 11.3909 9.06173 10.5601 10.0179L15 14.4578L14.572 14.8858L10.1384 10.4522ZM11.2886 6.44691C11.2886 3.77292 9.12091 1.60521 6.44691 1.60521C3.77292 1.60521 1.60521 3.77292 1.60521 6.44691C1.60521 9.12091 3.77292 11.2886 6.44691 11.2886C9.12091 11.2886 11.2886 9.12091 11.2886 6.44691Z\" fill=\"black\"/>\n</svg>\n"},
            {"name":"icon-console-export.svg","icon":"<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M8 2.57574L4.78787 5.78787L5.21213 6.21213L7.7 3.72426V10.5H8.3V3.72426L10.7879 6.21213L11.2121 5.78787L8 2.57574Z\" fill=\"black\"/>\n<path d=\"M3.3 9V12.7H12.7V9H13.3V13.3H2.7V9H3.3Z\" fill=\"black\"/>\n</svg>\n"},
            {"name":"icon-console-import.svg","icon":"<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M8 10.9243L11.2121 7.71213L10.7879 7.28787L8.3 9.77574L8.3 3H7.7L7.7 9.77574L5.21213 7.28787L4.78787 7.71213L8 10.9243Z\" fill=\"black\"/>\n<path d=\"M3.3 9V12.7H12.7V9H13.3V13.3H2.7V9H3.3Z\" fill=\"black\"/>\n</svg>\n"},
            {"name":"icon-Duplicate.svg","icon":"<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M6.73683 1.26318C6.03921 1.26318 5.47367 1.82872 5.47367 2.52634V4.21055L4.21052 4.21055C3.28035 4.21055 2.52631 4.9646 2.52631 5.89476V12.6316C2.52631 13.5618 3.28035 14.3158 4.21052 14.3158H9.26315C10.1933 14.3158 10.9474 13.5618 10.9474 12.6316V12.2106H12.6316C13.3292 12.2106 13.8947 11.645 13.8947 10.9474V2.52634C13.8947 1.82872 13.3292 1.26318 12.6316 1.26318H6.73683ZM10.9474 11.3684V5.89476C10.9474 4.9646 10.1933 4.21055 9.26315 4.21055L6.31578 4.21055V2.52634C6.31578 2.2938 6.50429 2.10529 6.73683 2.10529H12.6316C12.8641 2.10529 13.0526 2.2938 13.0526 2.52634V10.9474C13.0526 11.1799 12.8641 11.3684 12.6316 11.3684H10.9474ZM3.36841 5.89476C3.36841 5.42968 3.74543 5.05266 4.21052 5.05266H9.26315C9.72823 5.05266 10.1053 5.42968 10.1053 5.89476V12.6316C10.1053 13.0967 9.72823 13.4737 9.26315 13.4737H4.21052C3.74543 13.4737 3.36841 13.0967 3.36841 12.6316V5.89476Z\" fill=\"black\"/>\n</svg>\n"},
            {"name":"icon-image-icon5.svg","icon":"<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d='M1 8C1 4.13438 4.13438 1 8 1C11.8656 1 15 4.13438 15 8C15 11.8656 11.8656 15 8 15C4.13438 15 1 11.8656 1 8ZM4.5 6.57812C4.5 6.16391 4.83579 5.82812 5.25 5.82812C5.66421 5.82812 6 6.16391 6 6.57812C6 6.99234 5.66421 7.32812 5.25 7.32812C4.83579 7.32812 4.5 6.99234 4.5 6.57812ZM10 6.57812C10 6.16391 10.3358 5.82812 10.75 5.82812C11.1642 5.82812 11.5 6.16391 11.5 6.57812C11.5 6.99234 11.1642 7.32812 10.75 7.32812C10.3358 7.32812 10 6.99234 10 6.57812ZM12.1094 12.1094C12.6438 11.5766 13.0641 10.9547 13.3562 10.2625C13.6594 9.54688 13.8125 8.78594 13.8125 8C13.8125 7.21406 13.6594 6.45312 13.3578 5.73906C13.0641 5.04688 12.6453 4.425 12.1109 3.89062C11.5766 3.35625 10.9547 2.93594 10.2625 2.64375C9.54688 2.34063 8.78594 2.1875 8 2.1875C7.21406 2.1875 6.45312 2.34063 5.73906 2.64219C5.04688 2.93594 4.425 3.35469 3.89062 3.88906C3.35625 4.42344 2.93594 5.04531 2.64375 5.7375C2.34063 6.45312 2.1875 7.21406 2.1875 8C2.1875 8.78594 2.34063 9.54688 2.64219 10.2609C2.93594 10.9531 3.35469 11.575 3.88906 12.1094C4.42344 12.6438 5.04531 13.0641 5.7375 13.3562C6.45312 13.6594 7.21406 13.8125 8 13.8125C8.78594 13.8125 9.54688 13.6594 10.2609 13.3562C10.9531 13.0625 11.575 12.6438 12.1094 12.1094ZM9.62344 8.32812C9.55781 8.32812 9.50156 8.37813 9.49688 8.44375C9.4375 9.21719 8.78906 9.82812 8 9.82812C7.21094 9.82812 6.56094 9.21719 6.50313 8.44375C6.49844 8.37813 6.44219 8.32812 6.37656 8.32812H5.625C5.55313 8.32812 5.49688 8.3875 5.5 8.45937C5.56875 9.77656 6.66406 10.8281 8 10.8281C9.33594 10.8281 10.4312 9.77656 10.5 8.45937C10.5031 8.3875 10.4469 8.32812 10.375 8.32812H9.62344Z' fill=\"black\"/>\n</svg>\n"},
        ]
        for data in icons:
            code = InterfaceExplorer.add_Icon(icon_id_Group,data).json()["code"]
            assert 0 == code

        # 获取图标组内详情通过id 判断添加成功
        icons = InterfaceExplorer.get_Icon(icon_id_Group).json()
        assert 'icon-canvas-search.svg' == icons["data"]["items"][0]["name"]
        assert 'icon-canvas-search.svg' == icons["data"]["items"][1]["name"]
        assert 'icon-console-export.svg' == icons["data"]["items"][2]["name"]
        assert 'icon-console-import.svg' == icons["data"]["items"][3]["name"]
        assert 'icon-Duplicate.svg' == icons["data"]["items"][4]["name"]
        assert 'icon-image-icon5.svg' == icons["data"]["items"][5]["name"]

        # 循环删除正确图标、不存在、已删除的图标
        id = [1,2,3,4,5,6,123,1]
        for icon_id in id:
            code = InterfaceExplorer.delete_Icon(icon_id_Group,icon_id).json()["code"]
            assert 0 == code

        # 删除组
        id = [
            json_data["data"]["items"][0]["id"],
            json_data["data"]["items"][1]["id"],
            json_data["data"]["items"][2]["id"],
            json_data["data"]["items"][3]["id"],
            '123456788'
            ]
        for icon_id_Group in id:
            code = InterfaceExplorer.delete_Icon_Group(icon_id_Group).json()["code"]
            assert 0 == code

        # 循环创建200个图标组并删除
        for i in range(200):
            data = {"name":"QA" + str(QA_random),"type":"svg"}
            json_data = InterfaceExplorer.add_Icon_Group(data).json()
            assert 0 == json_data["code"]
            icon_id_Group = json_data["data"]["id"]
            code = InterfaceExplorer.delete_Icon_Group(icon_id_Group).json()["code"]
            assert 0 == code
