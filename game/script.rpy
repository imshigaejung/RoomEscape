init python:
    class Item:
        # Item 객체의 요소들 - 이름, 설명, 사진, 사용함수, 사용 가능여부, 사용 여부
        def __init__(self, name, description, image=None, use_func=None, usable=False, used=False):
            self.name = name
            self.description = description
            self.image = image
            self.usable = usable
            self.used = used
            self.use_func = use_func
        # 아이템 사용 시 각자의 사용 함수를 호출
        def use(self):
            if self.usable and self.use_func:
                def say_sequence():
                    renpy.show_screen("inventory")
                    self.use_func(self)
                    self.used=True
                # 인터렉션 충돌을 막기 위한 조치
                renpy.invoke_in_new_context(say_sequence)


# 사용 함수 모음

    # 열쇠 사용 함수
    def use_key(item):
            renpy.store.items.remove(item_data["key"])
            renpy.say(None, "열쇠를 이용해 잠긴 서랍을 열었다.")
            renpy.store.items.append(item_data["bulb"])
            renpy.say(None, "예비용 전구를 얻었다. 일반 전구와 다르게 생겼다.")
            renpy.store.is_locked = False
            renpy.jump("drawer")

    # 의자 사용 함수
    def use_chair(item):
        #def say_sequence():
        renpy.store.chair_set = True
        renpy.say(None, "의자가 놓였다. 이제 높은 곳까지 손이 닿을 것 같다.")
        item_data["bulb"].usable = True
        renpy.store.items.remove(item_data["chair"])
        renpy.jump("start")

    # 전구 사용 함수
    def use_bulb(item):
        renpy.say(None, "전구를 갈아끼웠다. 이상한 색의 빛이 방을 가득 메운다.")
        renpy.store.bulb_set = True
        renpy.store.items.remove(item_data["bulb"])
        renpy.jump("start")


default items = []
#설명 모음
default descriptions = {
    "key": "녹슨 열쇠. 어디를 열 수 있을까?",
    "chair": "의자치고는 높이가 낮다. 앉는 용도는 아닌듯 하다.",
    "note": """<전등 교체 순서>
            1. 기존 전등을 시계 반대방향으로 돌린다.
            2. 새 전등을 홈에 맞게 끼우고, 시계방향으로 돌린다. 
            ※주의. 3번이상 돌려야 고정 가능""",
    "bulb": "일반 전구와 미묘하게 색이 다른 전구다."
}
#아이템 데이터 모음 -> 설명 모음, 사용 함수 모음에서 참조
default item_data = {
    "key": Item("열쇠",descriptions["key"], "image_key.png", use_func=use_key),
    "chair": Item("의자", descriptions["chair"], "image_chair.png", use_func=use_chair),
    "note": Item("쪽지", descriptions["note"]),
    "bulb": Item("전구", descriptions["bulb"], "image_bulb.png", use_func=use_bulb)
}


init: 
    # 우측 상단에 제공되는 인벤토리 화면
    screen inventory:
        frame:
            align (0.95, 0.05)
            vbox:
                text "인벤토리"
                for item in items:
                    if not item.used:
                        # 사용 가능하다면 사용 함수 호출
                        if item.usable:
                            textbutton item.name action Function(item.use)
                        # 사용 가능하지 않다면 설명 출력
                        else:
                            textbutton item.name action Show("item_description", item=item)

    # 아이템 설명 출력 화면
    screen item_description(item):
        frame:
            align (0.5, 0.5)
            vbox:
                if item.image:
                    add item.image zoom 0.25 xpos 100 ypos 0
                text item.description
                textbutton "닫기" action Hide("item_description")


# image 문을 사용해 이미지를 정의합니다.
image darkroom = "Darkroom.png"
image drawer = "drawer.png"
image closet = "closet.png"
image sofa = "sofa.png"
image door = "door.png"
image darkroom_chairset = "Darkroom_chairset.png"
image darkroom_bulbset = "Darkroom_bulbset.png"
image drawer_bulbset = "drawer_bulbset.png"
image closet_bulbset = "closet_bulbset.png"
image sofa_bulbset = "sofa_bulbset.png"
image door_bulbset = "door_bulbset.png"

# 게임에서 사용할 전역변수
define sys = Character('', color="#c8ffc8")
default is_locked = True
default is_key = True
default is_chair = True
default chair_set = False
default bulb_set = False
define password = 2813

# 여기에서부터 게임이 시작합니다.
label start:
    $ item_data["chair"].usable=True
    show screen inventory
    #아이템 사용에 따른 방 배경 설정
    if bulb_set:
        scene darkroom_bulbset
    elif chair_set:
        scene darkroom_chairset 
    else:
        scene darkroom
    sys "무엇을 할까?"
    menu:
        "서랍장을 살핀다":
            $ item_data["chair"].usable=False
            jump drawer

        "옷장을 살핀다":
            $ item_data["chair"].usable=False
            jump closet
        
        "소파를 살핀다":
            $ item_data["chair"].usable=False
            jump sofa
        "문을 살핀다":
            $ item_data["chair"].usable=False
            jump door

        "전등을 살핀다":
            if chair_set:
                if bulb_set:
                    sys "강렬한 보라색 빛이 비춰지고 있다. 일반적인 용도는 아닌 것 같다."
                    jump start
                else:
                    sys "전구만 있다면 갈아끼울 수 있을 것 같다."
                    jump start
            else:
                sys "전구가 높이 있어 손이 닿지 않는다."
                jump start
    return  

label drawer:
    # 배경 설정
    if bulb_set:
        scene drawer_bulbset
    else:
        scene drawer
    # 대사 엔트리
    sys "서랍 3개가 보인다."
    menu:
        "위를 연다":
            if is_locked:
                $ item_data["key"].usable=True
                sys "잠겨있는듯 하다."
                window hide
                $ item_data["key"].usable=False
                jump drawer
            else:
                sys "안에 무언가가 더 보이지는 않는다."
            jump drawer

        "중간을 연다":
            sys "비어있다."
            jump drawer
            
        "아래를 연다":
            sys "전등 교체 방법이 적힌 쪽지가 있다."
            $ items.append(item_data["note"])
            jump drawer
        
        "뒤로 간다":
            jump start
    
label closet:
    if bulb_set:
        scene closet_bulbset
    else:
        scene closet
    sys "허름한 옷장이 보인다."
    menu:
        "옷장 안을 살핀다":
            if is_chair:
                sys "옷장 안에서 의자를 찾았다!"
                $ is_chair = False
                $ items.append(item_data["chair"])
            else:
                sys "안에 더 들어있는 것은 없는 듯하다."
            jump closet

        "뒤로 간다":
            jump start

label sofa:
    if bulb_set:
        scene sofa_bulbset
    else:
        scene sofa
    sys "낡은 소파가 보인다."
    menu:
        "소파 주변을 살핀다":
            if is_key:
                sys "소파 틈 사이에서 열쇠를 찾았다!"
                $ is_key = False
                $ items.append(item_data["key"])
            else:
                sys "주변에 무언가가 더 보이지는 않는다."
            jump sofa

        "뒤로 간다":
            jump start

label door:
    if bulb_set:
        scene door_bulbset
    else:
        scene door
    sys "자물쇠로 잠긴 문이다."
    menu:
        "자물쇠를 푼다":
            $ result = renpy.input("비밀번호 : ")
            $ number = int(result) if result.isdigit() else 0
            if number == password:
                sys "문이 열렸다!"
            else:
                sys "자물쇠는 풀리지 않았다."
                jump door
        "뒤로 간다":
            jump start