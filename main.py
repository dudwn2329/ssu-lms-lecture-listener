import asyncio
import logging
import os

from dotenv import load_dotenv
from playwright.async_api import async_playwright
from playwright._impl._api_types import Error as PlaywrightError
from service.auth import authorization, LoginProps
from service.course import get_uncompleted_course_components
import pyautogui
import tkinter as tk

load_dotenv()

logging.basicConfig(level=logging.INFO)


def on_submit():
    global playList
    playList = [lecture for lecture, chk in zip(lectures, checkboxes) if chk.var.get() == 1]
    print("선택된 강의")
    printSelected = lambda i: [print(lecture.title) for lecture in i]
    printSelected(playList)
    root.destroy()


# Tkinter 윈도우 초기화
root = tk.Tk()
root.title("재생할 강의 선택")
root.wm_attributes("-topmost", 1)

# 체크박스 및 변수 초기화
checkboxes = []
lectures = []
playList = []


async def play(context, component):
    page = await context.new_page()

    await page.goto(component.viewer_url, wait_until="domcontentloaded")
    await page.click('.vc-front-screen-play-btn', timeout=60000)

    # 음소거
    try:
        await page.wait_for_selector('.vc-pctrl-volume-btn', timeout=7000)
        await page.click('.vc-pctrl-volume-btn')

    except PlaywrightError:
        print("mute button did not appear, continuing without clicking...")

    # 이어보기 확인용
    try:
        await page.wait_for_selector('.confirm-ok-btn', timeout=7000)
        await page.click('.confirm-ok-btn')
    except PlaywrightError:
        print("Confirm button did not appear, continuing without clicking...")

    # 진도체크 확인용
    try:
        await page.wait_for_selector('.confirm-ok-btn', timeout=7000)
        await page.click('.confirm-ok-btn')

    except PlaywrightError:
        print("Confirm button did not appear, continuing without clicking...")

    duration = component.item_content_data['duration'] - component.attendance_data['progress']
    await asyncio.sleep(duration)  # use asyncio.sleep for async function
    await page.close()
    await asyncio.sleep(1)


async def bootstrap():
    print("🚀 온라인 강의 자동 이어듣기 시작!\n")

    async with async_playwright() as p:
        browser = await p.firefox.launch(
            # True로 설정 시 창 표시 안함
            headless=False

        )
        context = await browser.new_context(
            locale="ko-KR",
        )
        try:
            _id = os.getenv("SSU_ID")
            password = os.getenv("SSU_PASSWORD")

            if not (_id and password):
                print("📝 로그인 정보를 입력하세요.")

                _id = pyautogui.prompt('lms 아이디(학번) 입력')
                password = pyautogui.password('비밀번호')

            print("⏳ 로그인 중입니다 ...")

            me = await authorization(context, LoginProps(_id, password))
            print(me)
            print("⏳ 강의 정보를 불러오는 중입니다 ...")

            uncompleted_components = get_uncompleted_course_components(me)
            global lectures, checkboxes
            print(f"👀 총 {len(uncompleted_components)}개의 미수강 현재 주차 강의가 있습니다.")
            for lecture in uncompleted_components:
                print(lecture.title)
                checkVar = tk.IntVar()
                chk = tk.Checkbutton(root, text=lecture.title, variable=checkVar)
                chk.var = checkVar
                chk.pack(anchor="w")
                checkboxes.append(chk)
                lectures.append(lecture)
            # 제출 버튼
            submit_button = tk.Button(root, text="Submit", command=on_submit)
            submit_button.pack()
            root.update()
            root.deiconify()
            root.lift()
            root.mainloop()
            if playList:
                print("\n")

                for component in playList:
                    print(f'[{component.title}] 재생')
                    await play(context, component)
                    print(f'[{component.title}] 종료')

            print("\n✋ 다음에 또 봐요!")

        except Exception as e:
            print(e)
        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(bootstrap())
